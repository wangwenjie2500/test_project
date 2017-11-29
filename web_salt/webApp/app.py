# -*- coding:utf-8 -*-
from flask import Flask
from flask import render_template
from flask import request
from flask_cors import CORS

app = Flask(__name__, static_url_path='')
CORS(app=app)
@app.route('/')
@app.route('/login')
def UserLogin():
    try:
        return render_template('login.html')
    except Exception:
        pass

@app.route('/index',methods=['POST'])
def UserLoginAuth():
    try:
        user = request.form['username']
        password = request.form['password']
        from web_salt.user import User
        if User().UserAuth(user,password):
            data = {'user' : user}
            return render_template('index.html',data=data)
        else:
            return render_template('loginError.html')
    except Exception,msg:
        print msg
@app.route('/consoleTop')
def ClusterConsoleTop():
    try:
        return render_template('tabletop.html')
    except Exception,msg:
        pass


@app.route('/consoleUserTop')
def UserTop():
    try:
        from web_salt.user import User
        return render_template('userInterface.html')
    except Exception,msg:
        pass
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=9800)

