# -*- coding:utf-8 -*-
from flask import Flask,request,jsonify,make_response,Response
from flask_cors import CORS
import web_api_module
import json
from functools import wraps

app = Flask(__name__, static_url_path='')
CORS(app)
#

@app.route('/api/v0.1/crontrol',methods=['POST',"GET"])
def clusterCrontrol():
    try:
        if request.method == 'POST':
            data = json.loads(request.get_data())
            object = web_api_module.crontrol()
            setattr(object,"data",data)
            f = getattr(object,data['type'])() if data['type'] in dir(web_api_module.crontrol) else {'error' : 451}
            return jsonify(f)
    except Exception,msg:
        print(1,msg)
        return json.dumps({'error' : 451})



if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=8085)