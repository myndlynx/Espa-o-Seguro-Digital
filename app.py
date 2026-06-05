from flask import Flask, request, redirect, session, render_template, url_for
from datetime import timedelta

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
    {"matricula": "202414610001", "senha": "12345a", "tipo": "aluno"},
    {"matricula": "202414610002", "senha": "12345p", "tipo": "psicologo", "campus": "Santa Rita"}
]

def autenticar(matricula, senha):
    if not matricula or not senha:
        return None
    for usuario in usuarios:
        if usuario["matricula"] == matricula and usuario["senha"] == senha:
            return usuario
    return None

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        matricula = request.form.get('matricula')
        senha = request.form.get('senha')
        usuario = autenticar(matricula, senha)
        if usuario:
            session.permanent = True
            session['usuario'] = usuario['matricula']
            session['tipo'] = usuario['tipo']
            if session['tipo'] == 'psicologo':
                session['campus'] = usuario['campus']
                return redirect(url_for('area_psicologo'))
            elif session['tipo'] == 'aluno':
                return redirect(url_for('selecionar_campus'))
        erro = "Matrícula ou senha incorretos."
    return render_template('login.html', erro=erro)

@app.route('/selecionar-campus')
def selecionar_campus():
    if 'tipo' not in session or session['tipo'] != 'aluno':
        return redirect(url_for('login'))
    return render_template('selecionar_campus.html', campi=lista_campi)

@app.route('/salvar-campus', methods=['POST'])
def salvar_campus():
    if 'tipo' not in session or session['tipo'] != 'aluno':
        return redirect(url_for('login'))
    escolha = request.form.get('campus_nome')
    session['campus'] = escolha 
    return redirect(url_for('area_aluno'))

@app.route('/aluno')
def area_aluno():
    if 'tipo' not in session or session['tipo'] != 'aluno':
        return redirect(url_for('login'))
    return render_template('aluno.html')


@app.route('/agenda')
def agenda():
    if 'tipo' not in session or session['tipo'] != 'aluno':
        return redirect(url_for('login'))
    return render_template('agenda.html')

@app.route('/consultas')
def consultas():
    if 'tipo' not in session or session['tipo'] != 'aluno':
        return redirect(url_for('login'))
    return render_template('consulta.html')

@app.route('/dicas')
def dicas():
    if 'tipo' not in session or session['tipo'] != 'aluno':
        return redirect(url_for('login'))
    return render_template('dicas.html')

@app.route('/ajuda')
def ajuda():
    if 'tipo' not in session or session['tipo'] != 'aluno':
        return redirect(url_for('login'))
    return render_template('ajuda.html')

@app.route('/objetivo')
def objetivo():
    if 'tipo' not in session or session['tipo'] != 'aluno':
        return redirect(url_for('login'))
    return render_template('objetivo.html')

@app.route('/psicologo')
def area_psicologo():
    if 'tipo' not in session or session['tipo'] != 'psicologo':
        return redirect(url_for('login'))
    return render_template('psicologo.html')

# --- SISTEMA ---

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/status')
def status():
    return "Servidor funcionando perfeitamente!"

@app.errorhandler(404)
def pagina_nao_encontrada(error):
    return "Página não encontrada no servidor", 404

@app.errorhandler(500)
def erro_servidor(error):
    return "Erro interno no servidor", 500

if __name__ == '__main__':
    app.run(debug=True)