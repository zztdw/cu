from flask import redirect, request, jsonify, make_response
from application import app, session, db_engine, Base
from application.model import Cafeteria
from functools import wraps
import requests, json, jwt

# decorator加在需要特定权限的API之前
# 使用该decorator的方法必须在url参数中传入token，否则视为token无效，不执行方法
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        # decode token可以获得Cafeteria的id，如果token无效会返回403
        if not token:
            return make_response('Token is missing!')
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'],"HS256")
        except:
            return make_response('Token is invalid', 403)
        return f(*args, **kwargs)
    return decorated

@app.route('/location')
def location():
    # sqlite query
    cafeterias = session.query(Cafeteria)
    return_list = []
    # 迭代所有cafeteria
    for cafeteria in cafeterias:
        current_dict = {}
        # 迭代所有cafeteria的所有属性(人为定义的)加入current_dict
        for key in cafeteria.__dict__:
            if key != '_sa_instance_state':
                current_dict[key] = cafeteria.__dict__[key]
        return_list.append(current_dict)
    # 返回json化的字典列表
    return make_response(jsonify(return_list))