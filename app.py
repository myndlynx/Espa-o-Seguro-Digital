from flask import Flask, render_template

app = Flask(__name__)

@app.route('/discente/login')
def login():
    return render_template('login_dis.html')

if __name__ == "__main__":
    app.run(debug=True)