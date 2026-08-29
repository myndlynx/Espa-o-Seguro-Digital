from flask import Blueprint, session, render_template, redirect, url_for, request, flash
from banco import lista_campi, consultas_db


aluno_bp = Blueprint('aluno', __file__)


@aluno_bp.route('/selecionar-campus')
def selecionar_campus():
    if session.get('tipo') != 'aluno': return redirect(url_for('auth.login'))
    return render_template('selecionar_campus.html', campi=lista_campi)

@aluno_bp.route('/salvar-campus', methods=['POST'])
def salvar_campus():
    if session.get('tipo') != 'aluno': return redirect(url_for('auth.login'))
    session['campus'] = request.form.get('campus_nome')
    return redirect(url_for('auth.area_aluno'))


@aluno_bp.route('/agendar', methods=['GET'])
def agendar():
    if session.get('tipo') != 'aluno': return redirect(url_for('auth.login'))
    
    campus_aluno = session.get('campus')
    opcoes_psicologos = []

    for c in consultas_db:
        if c['status'] == 'Livre':
            
            if c['modalidade'] == 'Online':
                opcao = {'nome': c['psicologo_nome'], 'tipo': 'Online'}
                if opcao not in opcoes_psicologos:
                    opcoes_psicologos.append(opcao)
                    
            elif c['modalidade'] == 'Presencial' and c['campus'] == campus_aluno:
                opcao = {'nome': c['psicologo_nome'], 'tipo': 'Presencial'}
                if opcao not in opcoes_psicologos:
                    opcoes_psicologos.append(opcao)

    return render_template('agendar.html', psicologos=opcoes_psicologos)

@aluno_bp.route('/agendar-horarios', methods=['POST'])
def agendar_horarios():
    if session.get('tipo') != 'aluno': return redirect(url_for('auth.login'))
    modalidade = request.form.get('modalidade')
    psicologo_nome = request.form.get('psicologo')
    horarios_livres = [c for c in consultas_db if c['psicologo_nome'] == psicologo_nome and c['modalidade'] == modalidade and c['status'] == 'Livre']
    return render_template('agendar_horarios.html', psicologo_nome=psicologo_nome, modalidade=modalidade, horarios=horarios_livres)

@aluno_bp.route('/agenda/cancelar', methods=['POST'])
def cancelar_consulta_aluno():
    if session.get('tipo') != 'aluno': return redirect(url_for('auth.login'))

    id_consulta = int(request.form.get('id_consulta'))

    for c in consultas_db:
        if c['id'] == id_consulta and c.get('aluno_matricula') == session['usuario']:
            c['status'] = 'Livre'
            c['aluno_matricula'] = None
            c['aluno_nome'] = None
            flash("Consulta cancelada com sucesso!", "sucesso")
            break

    return redirect(url_for('auth.agenda'))

@aluno_bp.route('/salvar-agendamento', methods=['POST'])
def salvar_agendamento():
    if session.get('tipo') != 'aluno': return redirect(url_for('auth.login'))
    
    id_consulta = int(request.form.get('id_consulta'))
    
    consulta_desejada = next((c for c in consultas_db if c['id'] == id_consulta), None)
    
    if not consulta_desejada:
        flash("Erro: Horário não encontrado.", "erro")
        return redirect(url_for('auth.agenda'))

    if consulta_desejada['status'] == 'Agendado':
        flash("Erro: Este horário acabou de ser preenchido por outro aluno.", "erro")
        return redirect(url_for('auth.agenda'))
        
    ja_tem_consulta = False
    for c in consultas_db:
        if (c.get('aluno_matricula') == session['usuario'] and 
            c['status'] == 'Agendado' and 
            c['data'] == consulta_desejada['data'] and 
            c['horario'] == consulta_desejada['horario']):
            ja_tem_consulta = True
            break
            
    if ja_tem_consulta:
        flash("Erro: Você já possui uma consulta agendada para esta mesma data e horário!", "erro")
        return redirect(url_for('auth.agenda'))
    
    for c in consultas_db:
        if c['id'] == id_consulta:
            c['status'] = 'Agendado'
            c['aluno_matricula'] = session['usuario']
            c['aluno_nome'] = session['nome']
            flash("Consulta agendada com sucesso!", "sucesso")
            break
            
    return redirect(url_for('auth.agenda'))

@aluno_bp.route('/consultas', methods=['GET'])
def consultas():
    if session.get('tipo') != 'aluno': return redirect(url_for('auth.login'))
    
    campus_aluno = session.get('campus')
    opcoes_psicologos = []

    for c in consultas_db:
        if c['status'] == 'Livre':
            if c['modalidade'] == 'Online':
                opcao = {'nome': c['psicologo_nome'], 'tipo': 'Online'}
                if opcao not in opcoes_psicologos:
                    opcoes_psicologos.append(opcao)
                    
            elif c['modalidade'] == 'Presencial' and c['campus'] == campus_aluno:
                opcao = {'nome': c['psicologo_nome'], 'tipo': 'Presencial'}
                if opcao not in opcoes_psicologos:
                    opcoes_psicologos.append(opcao)

    return render_template('consulta.html', psicologos=opcoes_psicologos)


