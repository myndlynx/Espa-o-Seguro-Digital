from flask import Flask, request, redirect, session, render_template, url_for
from datetime import timedelta, date

app = Flask(__name__)
app.secret_key = 'chave_secreta_projeto_seguro'
app.permanent_session_lifetime = timedelta(hours=4)

lista_campi = [
    {'nome': 'Areia'}, {'nome': 'Cabedelo'}, {'nome': 'Cajazeiras'},
    {'nome': 'Campina Grande'}, {'nome': 'Catolé do Rocha'}, {'nome': 'Esperança'},
    {'nome': 'Guarabira'}, {'nome': 'Itabaiana'}, {'nome': 'Itaporanga'},
    {'nome': 'João Pessoa'}, {'nome': 'Mangabeira (João Pessoa)'}, {'nome': 'Monteiro'},
    {'nome': 'Patos'}, {'nome': 'Pedras de Fogo'}, {'nome': 'Picuí'},
    {'nome': 'Princesa Isabel'}, {'nome': 'Santa Rita'}
]

usuarios = [
    {"matricula": "202414610001", "senha": "12345a", "nome": "João Aluno", "tipo": "aluno"},
    {"matricula": "202414610003", "senha": "12345b", "nome": "Maria Aluna", "tipo": "aluno"},
    {"matricula": "202414610002", "senha": "12345p", "nome": "Dra. Ana Costa", "tipo": "psicologo", "campus": "Santa Rita"}
]

consultas_db = []
id_consulta_atual = 1

def autenticar(matricula, senha):
    for u in usuarios:
        if u["matricula"] == matricula and u["senha"] == senha: return u
    return None

@app.route('/')
def index(): return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
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
                return redirect(url_for('area_psicologo'))
            return redirect(url_for('selecionar_campus'))
        erro = "Matrícula ou senha incorretos."
    return render_template('login.html', erro=erro)

@app.route('/selecionar-campus')
def selecionar_campus():
    if session.get('tipo') != 'aluno': return redirect(url_for('login'))
    return render_template('selecionar_campus.html', campi=lista_campi)

@app.route('/salvar-campus', methods=['POST'])
def salvar_campus():
    if session.get('tipo') != 'aluno': return redirect(url_for('login'))
    session['campus'] = request.form.get('campus_nome')
    return redirect(url_for('area_aluno'))

@app.route('/aluno')
def area_aluno():
    if session.get('tipo') != 'aluno': return redirect(url_for('login'))
    return render_template('aluno.html')

@app.route('/agenda')
def agenda():
    if session.get('tipo') != 'aluno': return redirect(url_for('login'))
    meus_agendamentos = [c for c in consultas_db if c.get('aluno_matricula') == session['usuario'] and c['status'] == 'Agendado']
    return render_template('agenda.html', meus_agendamentos=meus_agendamentos)

@app.route('/agendar', methods=['GET'])
def agendar():
    if session.get('tipo') != 'aluno': return redirect(url_for('login'))
    psicologos_com_horario = list(set([c['psicologo_nome'] for c in consultas_db if c['status'] == 'Livre']))
    return render_template('agendar.html', psicologos=psicologos_com_horario)

@app.route('/agendar-horarios', methods=['POST'])
def agendar_horarios():
    if session.get('tipo') != 'aluno': return redirect(url_for('login'))
    modalidade = request.form.get('modalidade')
    psicologo_nome = request.form.get('psicologo')
    horarios_livres = [c for c in consultas_db if c['psicologo_nome'] == psicologo_nome and c['modalidade'] == modalidade and c['status'] == 'Livre']
    return render_template('agendar_horarios.html', psicologo_nome=psicologo_nome, modalidade=modalidade, horarios=horarios_livres)

@app.route('/salvar-agendamento', methods=['POST'])
def salvar_agendamento():
    if session.get('tipo') != 'aluno': return redirect(url_for('login'))
    
    id_consulta = int(request.form.get('id_consulta'))
    
    for c in consultas_db:
        if c['id'] == id_consulta:
            if c['status'] == 'Agendado':
                return "Erro: Este horário acabou de ser preenchido por outro aluno."
            
            c['status'] = 'Agendado'
            c['aluno_matricula'] = session['usuario']
            c['aluno_nome'] = session['nome']
            break
            
    return redirect(url_for('agenda'))

@app.route('/psicologo')
def area_psicologo():
    if session.get('tipo') != 'psicologo': return redirect(url_for('login'))
    return render_template('psicologo.html')

@app.route('/psicologo/agendamentos', methods=['GET', 'POST'])
def psicologo_agendamentos():
    global id_consulta_atual
    if session.get('tipo') != 'psicologo': return redirect(url_for('login'))
    
    if request.method == 'POST':
        data_raw = request.form.get('data')
        
        if '-' in data_raw:
            ano, mes, dia = data_raw.split('-')
            data_formatada = f"{dia}/{mes}/{ano}"
        else:
            data_formatada = data_raw

        nova_disponibilidade = {
            "id": id_consulta_atual,
            "psicologo_matricula": session['usuario'],
            "psicologo_nome": session['nome'],
            "campus": session['campus'],
            "data": data_formatada,
            "horario": request.form.get('horario'),
            "modalidade": request.form.get('modalidade'),
            "status": "Livre",
            "aluno_matricula": None,
            "aluno_nome": None
        }
        consultas_db.append(nova_disponibilidade)
        id_consulta_atual += 1
        return redirect(url_for('psicologo_agendamentos'))
        
    minha_agenda = [c for c in consultas_db if c['psicologo_matricula'] == session['usuario']]
    
    hoje = date.today().strftime('%Y-%m-%d')
    limite = (date.today() + timedelta(days=365)).strftime('%Y-%m-%d')
    
    return render_template('psicologo_agendamentos.html', minha_agenda=minha_agenda, hoje=hoje, limite=limite)

@app.route('/psicologo/cancelar-horario', methods=['POST'])
def cancelar_horario():
    if session.get('tipo') != 'psicologo': return redirect(url_for('login'))
    
    id_consulta = int(request.form.get('id_consulta'))
    global consultas_db
    
    # Filtra a lista, mantendo apenas as consultas que NÃO possuem o ID que acabamos de cancelar
    consultas_db = [c for c in consultas_db if c['id'] != id_consulta]
    
    return redirect(url_for('psicologo_agendamentos'))

@app.route('/psicologo/historico')
def psicologo_historico():
    if session.get('tipo') != 'psicologo': return redirect(url_for('login'))
    consultas_marcadas = [c for c in consultas_db if c['psicologo_matricula'] == session['usuario'] and c['status'] == 'Agendado']
    return render_template('psicologo_historico.html', consultas=consultas_marcadas)

@app.route('/psicologo/dicas')
def psicologo_dicas():
    if session.get('tipo') != 'psicologo': return redirect(url_for('login'))
    return render_template('psicologo_dicas.html')

@app.route('/dicas')
def dicas(): return render_template('dicas.html')

@app.route('/ajuda')
def ajuda(): return render_template('ajuda.html')

@app.route('/objetivo')
def objetivo(): return render_template('objetivo.html')

@app.route('/consultas')
def consultas(): return render_template('consulta.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)