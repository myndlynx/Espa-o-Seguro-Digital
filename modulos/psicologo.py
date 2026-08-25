from flask import Blueprint, request, render_template, session, redirect, url_for, flash
from datetime import date, timedelta
from banco import consultas_db, id_consulta_atual

psicologo_bp = Blueprint('psicologo', __file__)

@psicologo_bp.route('/psicologo/agendamentos', methods=['GET', 'POST'])
def psicologo_agendamentos():
    global id_consulta_atual
    if session.get('tipo') != 'psicologo': return redirect(url_for('auth.login'))
    
    erro = None
    
    if request.method == 'POST':
        data_raw = request.form.get('data')
        horario_form = request.form.get('horario')
        
        if '-' in data_raw:
            ano, mes, dia = data_raw.split('-')
            data_formatada = f"{dia}/{mes}/{ano}"
        else:
            data_formatada = data_raw

        horario_duplicado = False
        for c in consultas_db:
            if c['psicologo_matricula'] == session['usuario'] and c['data'] == data_formatada and c['horario'] == horario_form:
                horario_duplicado = True
                break

        if horario_duplicado:
            erro = "Você já possui um horário cadastrado para esta data e hora!"
        else:
            nova_disponibilidade = {
                "id": id_consulta_atual,
                "psicologo_matricula": session['usuario'],
                "psicologo_nome": session['nome'],
                "campus": session['campus'],
                "data": data_formatada,
                "horario": horario_form,
                "modalidade": request.form.get('modalidade'),
                "status": "Livre",
                "aluno_matricula": None,
                "aluno_nome": None
            }
            consultas_db.append(nova_disponibilidade)
            id_consulta_atual += 1
            flash("Horário cadastrado com sucesso!", "sucesso")
            return redirect(url_for('psicologo.psicologo_agendamentos'))
        
    minha_agenda = [c for c in consultas_db if c['psicologo_matricula'] == session['usuario']]
    
    hoje = date.today().strftime('%Y-%m-%d')
    limite = (date.today() + timedelta(days=365)).strftime('%Y-%m-%d')
    
    return render_template('psicologo_agendamentos.html', minha_agenda=minha_agenda, hoje=hoje, limite=limite, erro=erro)

@psicologo_bp.route('/psicologo/cancelar-horario', methods=['POST'])
def cancelar_horario():
    if session.get('tipo') != 'psicologo': return redirect(url_for('auth.login'))
    
    id_consulta = int(request.form.get('id_consulta'))
    global consultas_db
    
    consultas_db = [c for c in consultas_db if c['id'] != id_consulta]
    flash("Horário cancelado com sucesso!", "sucesso")
    
    return redirect(url_for('psicologo.psicologo_agendamentos'))

@psicologo_bp.route('/psicologo/historico')
def psicologo_historico():
    if session.get('tipo') != 'psicologo': return redirect(url_for('auth.login'))
    consultas_marcadas = [c for c in consultas_db if c['psicologo_matricula'] == session['usuario'] and c['status'] == 'Agendado']
    return render_template('psicologo_historico.html', consultas=consultas_marcadas)

@psicologo_bp.route('/psicologo/dicas')
def psicologo_dicas():
    if session.get('tipo') != 'psicologo': return redirect(url_for('auth.login'))
    return render_template('psicologo_dicas.html')
