from flask import Blueprint, request, url_for, redirect, render_template, session
from banco import usuarios, consultas_db
from datetime import datetime

auth_bp = Blueprint('auth',__file__)

def autenticar(matricula, senha):
    for u in usuarios:
        if u["matricula"] == matricula and u["senha"] == senha: return u
    return None

def chave_data_horario(c):
    try:
        return datetime.strptime(f"{c['data']} {c['horario']}", '%d/%m/%Y %H:%M')
    except (ValueError, KeyError):
        return datetime.max

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        usuario = autenticar(request.form.get('matricula'), request.form.get('senha'))
        if usuario:
            session.permanent = True
            session['usuario'] = usuario['matricula']
            session['nome'] = usuario['nome']
            session['tipo'] = usuario['tipo']
            if session['tipo'] == 'psicologo':
                session['campus'] = usuario['campus']
                return redirect(url_for('auth.area_psicologo'))
            return redirect(url_for('aluno.selecionar_campus'))
        erro = "Matrícula ou senha incorretos."
    return render_template('login.html', erro=erro)
 
@auth_bp.route('/agenda')      # precisou vir para cá, mas é a agenda do ALUNO
def agenda():
    if session.get('tipo') != 'aluno': return redirect(url_for('login'))
    meus_agendamentos = [c for c in consultas_db if c.get('aluno_matricula') == session['usuario'] and c['status'] == 'Agendado']
    meus_agendamentos.sort(key=chave_data_horario)
    return render_template('agenda.html', meus_agendamentos=meus_agendamentos)

@auth_bp.route('/psicologo')
def area_psicologo():
    if session.get('tipo') != 'psicologo': return redirect(url_for('auth.login'))
    return render_template('psicologo.html')

@auth_bp.route('/aluno')
def area_aluno():
    if session.get('tipo') != 'aluno': return redirect(url_for('auth.login'))
    return render_template('aluno.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
