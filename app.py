from flask import Flask, render_template
app = Flask (__name__)

@app.route('/discente/login')
def login ():
  return render_template('login_dis.html')

app.run()