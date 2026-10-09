from flask import Blueprint, request, render_template, session, redirect, url_for, flash
from datetime import date, timedelta, datetime
from banco import consultas_db, proximo_id, atualizar_consultas_concluidas, dicas_db, proximo_id_dica

psicologo_bp = Blueprint('psicologo', __file__)

@psicologo_bp.route('/psicologo/agendamentos', methods=['GET', 'POST'])
def psicologo_agendamentos():
    if session.get('tipo') != 'psicologo': return redirect(url_for('auth.login'))

    atualizar_consultas_concluidas()
    
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
        
    agora = datetime.utcnow() - timedelta(hours=3)

    minha_agenda = []
    for c in consultas_db:
        if c['psicologo_matricula'] != session['usuario']:
            continue
        if c.get('status') in ['Concluída', 'concluida', 'Cancelada', 'cancelada']:
            continue

        if c.get('status') == 'Livre':
            try:
                data_hora = datetime.strptime(f"{c['data']} {c['horario']}", "%d/%m/%Y %H:%M")
                if data_hora <= agora:
                    continue
            except ValueError:
                pass

        minha_agenda.append(c)
    
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
    
    agora = datetime.utcnow() - timedelta(hours=3)
    consultas_concluidas = []
    
    for c in consultas_db:
        if (
            c['psicologo_matricula'] == session['usuario']
            and c['aluno_matricula'] is not None
            and c.get('status') not in ['Cancelada', 'cancelada']
        ):
            try:
                data_hora_agendamento = datetime.strptime(f"{c['data']} {c['horario']}", "%d/%m/%Y %H:%M")
            except ValueError:
                try:
                     data_hora_agendamento = datetime.strptime(f"{c['data']} {c['horario']}", "%Y-%m-%d %H:%M")
                except ValueError:
                    continue

            if data_hora_agendamento < agora:
                consultas_concluidas.append({
                    'data': c['data'],
                    'horario': c['horario'],
                    'aluno_nome': c['aluno_nome'],
                    'modalidade': c['modalidade']
                })
    
    consultas_concluidas.sort(key=lambda x: f"{x['data'][6:10]}{x['data'][3:5]}{x['data'][0:2]} {x['horario']}", reverse=True)

    return render_template('psicologo_historico.html', consultas=consultas_concluidas)

@psicologo_bp.route('/psicologo/dicas')
def psicologo_dicas():
    if session.get('tipo') != 'psicologo': return redirect(url_for('auth.login'))

    dicas_ordenadas = sorted(dicas_db, key=lambda d: d['id'], reverse=True)
    return render_template('psicologo_dicas.html', dicas=dicas_ordenadas)

@psicologo_bp.route('/psicologo/dicas/salvar', methods=['POST'])
def salvar_dica():
    if session.get('tipo') != 'psicologo': return redirect(url_for('auth.login'))

    id_dica = request.form.get('id_dica', '').strip()
    titulo = request.form.get('titulo', '').strip()
    texto = request.form.get('texto', '').strip()

    if not titulo or not texto:
        flash("Preencha o título e o texto da dica.", "erro")
        return redirect(url_for('psicologo.psicologo_dicas'))

    if id_dica:
        dica = next((d for d in dicas_db if str(d['id']) == id_dica), None)

        if not dica or dica.get('psicologo_matricula') != session['usuario']:
            flash("Você não tem permissão para editar esta dica.", "erro")
            return redirect(url_for('psicologo.psicologo_dicas'))

        dica['titulo'] = titulo
        dica['texto'] = texto
        flash("Dica atualizada com sucesso!", "sucesso")
    else:
        dicas_db.append({
            "id": proximo_id_dica(),
            "titulo": titulo,
            "texto": texto,
            "data": (datetime.utcnow() - timedelta(hours=3)).strftime('%d/%m/%Y'),
            "autor": session['nome'],
            "psicologo_matricula": session['usuario']
        })
        flash("Dica publicada com sucesso!", "sucesso")

    return redirect(url_for('psicologo.psicologo_dicas'))

@psicologo_bp.route('/psicologo/dicas/cancelar', methods=['POST'])
def cancelar_dica():
    if session.get('tipo') != 'psicologo': return redirect(url_for('auth.login'))

    id_dica = request.form.get('id_dica', '').strip()
    dica = next((d for d in dicas_db if str(d['id']) == id_dica), None)

    if not dica:
        flash("Dica não encontrada.", "erro")
        return redirect(url_for('psicologo.psicologo_dicas'))

    if dica.get('psicologo_matricula') != session['usuario']:
        flash("Você não tem permissão para cancelar esta dica.", "erro")
        return redirect(url_for('psicologo.psicologo_dicas'))

    dicas_db.remove(dica)
    flash("Dica cancelada com sucesso!", "sucesso")

    return redirect(url_for('psicologo.psicologo_dicas'))
