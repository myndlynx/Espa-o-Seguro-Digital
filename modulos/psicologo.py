from flask import Blueprint, request, render_template, session, redirect, url_for, flash
from datetime import date, timedelta, datetime
from banco import consultas_db, proximo_id

psicologo_bp = Blueprint('psicologo', __file__)

@psicologo_bp.route('/psicologo/agendamentos', methods=['GET', 'POST'])
def psicologo_agendamentos():
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

        agora = datetime.utcnow() - timedelta(hours=3)
        try:
            data_hora_cadastro = datetime.strptime(f"{data_formatada} {horario_form}", "%d/%m/%Y %H:%M")
            horario_passado = data_hora_cadastro < agora
        except ValueError:
            horario_passado = False

        if horario_passado:
            erro = "Erro: Não é possível cadastrar um horário que já passou."
        else:
            horario_duplicado = False
            for c in consultas_db:
                if c['psicologo_matricula'] == session['usuario'] and c['data'] == data_formatada and c['horario'] == horario_form:
                    horario_duplicado = True
                    break

            if horario_duplicado:
                erro = "Você já possui um horário cadastrado para esta data e hora!"
            else:
                nova_disponibilidade = {
                    "id": proximo_id(),
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
                flash("Horário cadastrado com sucesso!", "sucesso")
                return redirect(url_for('psicologo.psicologo_agendamentos'))
        
    minha_agenda = [
        c for c in consultas_db 
        if c['psicologo_matricula'] == session['usuario'] 
        and c.get('status') not in ['Concluída', 'concluida', 'Cancelada', 'cancelada']
    ]
    
    hoje = (datetime.utcnow() - timedelta(hours=3)).strftime('%Y-%m-%d')
    limite = ((datetime.utcnow() - timedelta(hours=3)) + timedelta(days=365)).strftime('%Y-%m-%d')
    
    return render_template('psicologo_agendamentos.html', minha_agenda=minha_agenda, hoje=hoje, limite=limite, erro=erro)

@psicologo_bp.route('/psicologo/cancelar-horario', methods=['POST'])
def cancelar_horario():
    if session.get('tipo') != 'psicologo': return redirect(url_for('auth.login'))

    id_consulta = int(request.form.get('id_consulta'))

    for i, c in enumerate(consultas_db):
        if c['id'] == id_consulta:
            del consultas_db[i]
            break

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