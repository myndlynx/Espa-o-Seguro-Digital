from flask import Flask, request, redirect, session, render_template, url_for, flash
from datetime import timedelta, date, datetime
from banco import usuarios, lista_campi
from modulos.auth import auth_bp
from modulos.aluno import aluno_bp
from modulos.psicologo import psicologo_bp

app = Flask(__name__)
app.secret_key = 'chave_secreta_projeto_seguro'
app.register_blueprint(auth_bp)
app.register_blueprint(aluno_bp)
app.register_blueprint(psicologo_bp)
app.permanent_session_lifetime = timedelta(hours=4)

@app.after_request
def adicionar_headers_no_cache(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route('/')
def index(): return redirect(url_for('auth.login'))


@app.route('/dicas')
def dicas():
    if 'tipo' not in session: return redirect(url_for('auth.login'))
    return render_template('dicas.html')

@app.route('/ajuda')
def ajuda():
    if 'tipo' not in session: return redirect(url_for('auth.login'))
    return render_template('ajuda.html')

@app.route('/objetivo')
def objetivo():
    if 'tipo' not in session: return redirect(url_for('auth.login'))
    return render_template('objetivo.html')

if __name__ == '__main__':
    app.run(debug=True)