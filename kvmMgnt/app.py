# -*- coding:utf-8 -*-
from flask import Flask, jsonify,render_template, request ,session ,url_for,redirect
import module
import json
app = Flask(__name__, static_url_path='')
# @app.before_request
# def check_login():
#     if 'type' in session.keys():
#         if session['type'] == 'login':
#             pass
#         else:
#             return redirect(url_for('login'))
#     else:
#         return redirect(url_for('login'))

@app.route('/', methods=['GET','POST'])
@app.route('/login', methods=['GET','POST'])
def login():
    return render_template('login.html')
@app.route('/logout')
def logout():
    try:
        del session['username']
        del session['password']
        del session['type']
        return redirect(url_for('login'))
    except Exception,msg:
        return redirect(url_for('error'))

@app.route("/error")
def error():
    return render_template("loginError.html")
@app.route('/index',methods=['POST'])
def index():
    try:
        username = str(request.form['username'])
        password = str(request.form['password'])
        if module.crontrol().userAuth(username=username,password=password)['code'] == 200:
            session['username'] = username
            session['password'] = password
            session['type'] = 'login'
            data = {
                "user" : session['username'],
            }
            return render_template("index.html",data=data)
        else:
            return redirect(url_for('error'))
    except:
        return redirect(url_for('error'))

@app.route('/instanceMangnt')
def instanceMangnt():
    try:
        if session['username']:
            recode = module.crontrol().instanceMangnt()
            return render_template("DomainMgnt.html",data=recode)
        else:
            return redirect(url_for('login'))
    except Exception,msg:
        return redirect(url_for('error'))
@app.route('/diskMangnt')
def diskMangnt():
    try:
        #if session['username']:
        recode = module.crontrol().diskMangnt()
        return render_template("DiskMgnt.html",data=recode)
        #else:
        #    return redirect(url_for('login'))
    except Exception,msg:
        print(msg)
        return redirect(url_for('error'))

@app.route('/clusterMangnt')
def clusterMangnt():
    try:
        recode = module.crontrol().clusterMangnt()
        return render_template("ClusterNode.html",data=recode)
    except Exception,msg:
        return redirect(url_for('error'))
@app.route('/createDomain')
def create():
    try:
        rcode = module.crontrol().getCreateDomainInfo()
        return render_template("DomainCreate.html",data=rcode)
    except Exception,msg:
        return redirect(url_for('error'))
@app.route('/consoleTop')
def consoleTop():
    try:
        return render_template('tabletop.html')
    except Exception,msg:
        return redirect(url_for('error'))
@app.route('/ejectImage/<UUID>/<ACTION>',methods=['GET'])
def ejectImage(UUID,ACTION):
    try:
        return render_template('ejectCdrom.html',UUID=UUID)
    except Exception,msg:
        return redirect(url_for('error'))

@app.route('/test')
def test():

    return render_template("resourceInformation.html")

@app.route('/userInterface')
def userInterface():
    rcode = module.crontrol().userShow()
    return render_template('userInterface.html',data=rcode)

@app.route('/clusterNodeAdd')
def clusterNodeAdd():
    return render_template("CreateHostNode.html")

@app.route('/clusterNodeResourceInformation/<UUID>')
def clusterNodeResourceInformation(UUID):
    return render_template("resourceInformation.html")

app.secret_key = 'wangwenjiezhendefeichangshuaiya'
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True,port=8089)
