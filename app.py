from flask import Flask, request, redirect, session, render_template, url_for
from datetime import timedelta

app = Flask(__name__)

# Chave secreta necessária para assinar os cookies de sessão
app.secret_key = 'chave_secreta_projeto_seguro'

# Configura o tempo de vida da sessão (inatividade) para 4 horas
app.permanent_session_lifetime = timedelta(hours=4)

# --- LISTA PYTHON DOS 17 CAMPI DO IFPB ---
lista_campi = [
    {'nome': 'Areia'},
    {'nome': 'Cabedelo'},
    {'nome': 'Cajazeiras'},
    {'nome': 'Campina Grande'},
    {'nome': 'Catolé do Rocha'},
    {'nome': 'Esperança'},
    {'nome': 'Guarabira'},
    {'nome': 'Itabaiana'},
    {'nome': 'Itaporanga'},
    {'nome': 'João Pessoa'},
    {'nome': 'Mangabeira (João Pessoa)'},
    {'nome': 'Monteiro'},
    {'nome': 'Patos'},
    {'nome': 'Pedras de Fogo'},
    {'nome': 'Picuí'},
    {'nome': 'Princesa Isabel'},
    {'nome': 'Santa Rita'}
]

# --- BANCO DE DADOS LOCAL (Usuários) ---
usuarios = [
    {"matricula": "202414610001", "senha": "12345a", "tipo": "aluno"},
    {"matricula": "202414610002", "senha": "12345p", "tipo": "psicologo"}
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

            # Redireciona para a tela de escolher o campus
            return redirect(url_for('selecionar_campus'))
        
        # Caso o login falhe, define a mensagem que aparecerá no HTML
        erro = "Matrícula ou senha incorretos."

    return render_template('login.html', erro=erro)

# --- ROTAS DE SELEÇÃO DE CAMPUS ---

@app.route('/selecionar-campus')
def selecionar_campus():
    # Segurança: Se tentar acessar essa tela sem estar logado, volta pro login
    if 'usuario' not in session:
        return redirect(url_for('login'))
        
    # Renderiza a tela enviando a lista de campi para o HTML gerar os botões
    return render_template('selecionar_campus.html', campi=lista_campi)

@app.route('/salvar-campus', methods=['POST'])
def salvar_campus():
    if 'usuario' not in session:
        return redirect(url_for('login'))
        
    # Pega o valor do campus que o usuário selecionou na tela
    escolha = request.form.get('campus_nome')
    session['campus'] = escolha 
    
    # Direciona para o painel correto com base no perfil (Trancamento de Rotas)
    if session['tipo'] == 'psicologo':
        return redirect(url_for('area_psicologo'))
    elif session['tipo'] == 'aluno':
        return redirect(url_for('area_aluno'))
        
    return redirect(url_for('login'))

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

# --- SISTEMA E TRATAMENTO DE ERROS ---

@app.route('/logout')
def logout():
    """Limpa a sessão e desloga o usuário."""
    session.clear()
    return redirect(url_for('login'))

@app.route('/status')
def status():
    """Verifica se o servidor está rodando."""
    return "Servidor funcionando perfeitamente!"

@app.errorhandler(404)
def pagina_nao_encontrada(error):
    """Página personalizada para quando o usuário digita um endereço que não existe."""
    return "Página não encontrada no servidor", 404

@app.errorhandler(500)
def erro_servidor(error):
    """Página personalizada para erros internos do código."""
    return "Erro interno no servidor", 500

if __name__ == '__main__':
    # Roda o app em modo debug (reinicia sozinho ao salvar alterações)
    app.run(debug=True)