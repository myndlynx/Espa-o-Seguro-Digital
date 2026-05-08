from flask import Flask, request, redirect, session, render_template, url_for
from datetime import timedelta

app = Flask(__name__)

# Chave secreta necessária para assinar os cookies de sessão
app.secret_key = 'chave_secreta_do_projeto'

# 1. Configura o tempo de vida da sessão (inatividade) para 4 horas
app.permanent_session_lifetime = timedelta(hours=4)

# 2. Banco de dados local (Lista Python)
usuarios = [
    {"matricula": "202414610001", "senha": "12345a", "tipo": "aluno"},
    {"matricula": "202514610002", "senha": "12345p", "tipo": "psicologo"}
]

def autenticar(matricula, senha):
    """Função para validar se a matrícula e senha existem na lista."""
    if not matricula or not senha:
        return None
    for usuario in usuarios:
        if usuario["matricula"] == matricula and usuario["senha"] == senha:
            return usuario
    return None

# --- ROTAS PRINCIPAIS ---

@app.route('/')
def index():
    """Redireciona a raiz do site diretamente para a página de login."""
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    erro = None
    
    if request.method == 'POST':
        matricula = request.form.get('matricula')
        senha = request.form.get('senha')

        usuario = autenticar(matricula, senha)

        if usuario:
            # Ativa o tempo limite definido no permanent_session_lifetime
            session.permanent = True
            
            # Salva os dados básicos na sessão do navegador
            session['usuario'] = usuario['matricula']
            session['tipo'] = usuario['tipo']

            # Redireciona conforme o perfil (Trancamento de Rotas)
            if session['tipo'] == 'psicologo':
                return redirect(url_for('area_psicologo'))
            elif session['tipo'] == 'aluno':
                return redirect(url_for('area_aluno'))
        
        # Caso o login falhe, define a mensagem que aparecerá no HTML
        erro = "Matrícula ou senha incorretos."

    return render_template('login.html', erro=erro)

# --- ROTAS PROTEGIDAS (SÓ ACESSA QUEM ESTÁ LOGADO E TEM O PERFIL CERTO) ---

@app.route('/aluno')
def area_aluno():
    # Verifica se está logado E se o tipo é aluno
    if 'tipo' not in session or session['tipo'] != 'aluno':
        return redirect(url_for('login'))
        
    return render_template('aluno.html')

@app.route('/psicologo')
def area_psicologo():
    # Verifica se está logado E se o tipo é psicologo
    if 'tipo' not in session or session['tipo'] != 'psicologo':
        return redirect(url_for('login'))
        
    return render_template('psicologo.html')

# --- SISTEMA ---

@app.route('/logout')
def logout():
    """Limpa a sessão e desloga o usuário."""
    session.clear()
    return redirect(url_for('login'))

@app.route('/status')
def status():
    return "Servidor funcionando perfeitamente!"

# --- TRATAMENTO DE ERROS ---

@app.errorhandler(404)
def pagina_nao_encontrada(error):
    return "Página não encontrada no servidor", 404

@app.errorhandler(500)
def erro_servidor(error):
    return "Erro interno no servidor", 500

if __name__ == '__main__':
    # Roda o app em modo debug (reinicia sozinho ao salvar alterações)
    app.run(debug=True)