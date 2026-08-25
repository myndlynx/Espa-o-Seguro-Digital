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




@app.route('/')
def index(): return redirect(url_for('auth.login'))


@app.route('/dicas')
def dicas(): return render_template('dicas.html')

@app.route('/ajuda')
def ajuda(): return render_template('ajuda.html')

@app.route('/objetivo')
def objetivo(): return render_template('objetivo.html')

if __name__ == '__main__':
    app.run(debug=True)