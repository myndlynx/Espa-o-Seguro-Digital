from flask import Blueprint, session, render_template, redirect, url_for, request, flash
from banco import lista_campi, consultas_db
from datetime import datetime, timedelta

aluno_bp = Blueprint('aluno', __file__)

def _atualizar_consultas_concluidas():
    agora = datetime.utcnow() - timedelta(hours=3)
    for c in consultas_db:
        if c.get('status') == 'Agendado':
            try:
                data_hora_consulta = datetime.strptime(
                    f"{c['data']} {c['horario']}",
                    "%d/%m/%Y %H:%M"
                )
                if data_hora_consulta <= agora:
                    c['status'] = 'Concluída'
            except ValueError:
                pass

@aluno_bp.route('/agendar-horarios', methods=['POST'])
def agendar_horarios():
    if session.get('tipo') != 'aluno':
        return redirect(url_for('auth.login'))

    modalidade = request.form.get('modalidade')
    psicologo_nome = request.form.get('psicologo')

    agora = datetime.utcnow() - timedelta(hours=3)
    horarios_livres = []

    for c in consultas_db:
        if (
            c['psicologo_nome'] == psicologo_nome
            and c['modalidade'] == modalidade
            and c['status'] == 'Livre'
        ):
            try:
                data_hora_consulta = datetime.strptime(
                    f"{c['data']} {c['horario']}",
                    "%d/%m/%Y %H:%M"
                )
                
                if data_hora_consulta > agora:
                    horarios_livres.append(c)

            except ValueError:
                pass

    return render_template(
        'agendar_horarios.html',
        psicologo_nome=psicologo_nome,
        modalidade=modalidade,
        horarios=horarios_livres
    )



def _proximo_id():
    lista_de_ids = []
    for c in consultas_db:
        lista_de_ids.append(c['id'])
    return max(lista_de_ids) + 1


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


@aluno_bp.route('/consultas/historico', methods=['GET'])
def historico():
    if session.get('tipo') != 'aluno':
        return redirect(url_for('auth.login'))

    _atualizar_consultas_concluidas()

    meu_historico = []

    for c in consultas_db:
        if (
            c.get('aluno_matricula') == session['usuario']
            and c.get('status') in [
                'Concluída',
                'concluida',
                'Cancelada',
                'cancelada'
            ]
        ):
            meu_historico.append(c)

    return render_template(
        'historico.html',
        historico=meu_historico
    )
@aluno_bp.route('/agenda/cancelar', methods=['POST'])
def cancelar_consulta_aluno():
    if session.get('tipo') != 'aluno': return redirect(url_for('auth.login'))

    id_consulta = int(request.form.get('id_consulta'))

    for c in consultas_db:
        if c['id'] == id_consulta and c.get('aluno_matricula') == session['usuario']:
            consultas_db.append({
                'id': _proximo_id(),
                'psicologo_matricula': c['psicologo_matricula'],
                'psicologo_nome': c['psicologo_nome'],
                'campus': c['campus'],
                'data': c['data'],
                'horario': c['horario'],
                'modalidade': c['modalidade'],
                'status': 'Livre',
                'aluno_matricula': None,
                'aluno_nome': None
            })

            c['status'] = 'Cancelada'
            c['cancelado_em'] = (datetime.utcnow() - timedelta(hours=3)).strftime('%d/%m/%Y %H:%M')
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