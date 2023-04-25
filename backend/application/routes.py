from flask import redirect, request, jsonify, make_response
from application import app, session, db_engine, Base
from application.model import Cafeteria
from functools import wraps
import requests, json, jwt, datetime

# decorator加在需要特定权限的API之前
# 使用该decorator的方法必须在url参数中传入token，否则视为token无效，不执行方法
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        # decode token可以获得Cafeteria的id，如果token无效会返回403
        id = int(request.args.get('id'))
        if not token:
            return make_response('Token is missing!', 403)
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'],"HS256")
            cafeteria = session.query(Cafeteria).filter(Cafeteria.id == data['id']).first()
        except:
            return make_response('Token is invalid', 403)
        return f(cafeteria, *args, **kwargs)
    return decorated

@app.route('/verify')
@token_required
def verify(cafeteria):
    return make_response("Token is valid", 200)

@app.route('/location')
def location():
    # sqlite 查询
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
#这段代码定义了一个路由函数
# 当访问 "/location" 路径时，将会执行这个函数。
# 具体实现中，它从 SQLite 数据库中查询所有的自助餐厅信息，将每个自助餐厅的信息封装为一个字典，并将这些字典组成一个列表返回。
# 最后，使用 Flask 中的 make_response() 和 jsonify() 函数将这个列表转换为 JSON 格式，并将其作为响应返回给客户端。
@app.route('/login',methods=['POST'])
def login():
    data = request.json
    id = data['id']
    password = data['password']
    cafeteria = session.query(Cafeteria).filter(Cafeteria.id == int(id)).first()
    if cafeteria and cafeteria.password == password:
        token = jwt.encode({'id': cafeteria.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'],algorithm='HS256')
        return make_response(jsonify(
            {
                'token' : token,
                'message' : "Login successfully."
            }
        ), 200)
    return make_response(jsonify(
            {
                'message' : "Login Failed."
            }
        ), 403)
#这段代码定义了一个路由函数
# 当客户端通过 POST 方法访问 "/login" 路径时，将会执行这个函数。
# 具体实现中，它首先从请求的 JSON 数据中获取到登录信息，包括用户 ID 和密码。
# 使用 SQLAlchemy 进行查询，判断这个用户是否存在，以及密码是否匹配。
# 如果匹配成功，使用 jwt.encode() 函数生成一个 JSON Web Token，并将其作为响应返回给客户端。
# 如果匹配失败，则返回一个状态码为 403 的响应，并在其中包含一条消息说明登录失败。
    

# 定义一个API路由函数，允许HTTP方法为PUT请求
@app.route('/update', methods=["PUT"])
# 在路由函数之前定义的装饰器，用于对函数进行认证和授权
@token_required
# 传入餐厅对象，用于更新
def update_cafeteria(cafeteria):
    # 从请求中获取JSON数据并解析成Python对象
    updated_info = json.loads(request.json)
    # 更新餐厅对象的名称
    cafeteria.name = updated_info['name']
    # 更新餐厅对象的地址
    cafeteria.address = updated_info['address']
    # 更新餐厅对象的营业开始时间
    cafeteria.hours_open = updated_info['hours_open']
    # 更新餐厅对象的营业结束时间
    cafeteria.hours_closed = updated_info['hours_closed']
    # 更新餐厅对象的状态
    cafeteria.status = updated_info['status']
    # 更新餐厅对象的等待时间
    cafeteria.wait_times = updated_info['wait_times']
    # 更新餐厅对象的纬度
    cafeteria.coords_lat = updated_info['coords_lat']
    # 更新餐厅对象的经度
    cafeteria.coords_lon = updated_info['coords_lon']
    # 更新餐厅对象的类型
    cafeteria.type = updated_info['type']
    cafeteria.tele = updated_info['tele']
    # 试图提交更改到数据库中
    try:
        session.commit()
    # 如果提交更改失败，则返回错误的HTTP响应状态码
    except:
        return make_response(jsonify({'message': "Update failed."}), 403)
    # 如果提交更改成功，则返回成功的HTTP响应状态码
    return make_response(jsonify({'message': "Update successfully."}), 201)
#这段代码是一个 Flask 应用中的路由函数，处理的是客户端对 /update 路径发起的 PUT 请求
# 这个路由函数使用了装饰器 @token_required，用于对客户端的请求进行身份验证。
# 如果客户端传来的 token 无效，则返回一个 HTTP 状态码为 401 的错误响应。
#如果客户端的 token 通过了身份验证，那么路由函数就会从请求中读取 JSON 格式的数据，并将其解析为 Python 字典对象 updated_info。
# 接下来，路由函数会根据客户端传来的数据更新一个指定的自助餐厅对象 cafeteria 的属性。
# 这里的 cafeteria 参数实际上是 @token_required 装饰器从客户端传来的 token 中解码出的自助餐厅对象。
#更新完自助餐厅对象的属性之后，路由函数会将其写回到数据库中，并返回一个 HTTP 状态码为 201 的响应，表示更新成功。
# 如果写入数据库失败，则返回一个 HTTP 状态码为 403 的错误响应，表示更新失败。
# 最终，客户端会收到一个 JSON 格式的响应，包含一个键为 message 的字段，用于指示更新操作的结果。


@app.route('/plus', methods=["POST"])
# 在路由函数之前定义的装饰器，用于对函数进行认证和授权
def Plus():
    new_cafeteria= None
    # 从请求中获取JSON数据并解析成Python对象
    new_info = json.loads(request.json)
    # 创建新的餐厅对象并赋值
    new_cafeteria = Cafeteria(
        name=new_info['name'],
        address=new_info['address'],
        hours_open=new_info['hours_open'],
        hours_closed=new_info['hours_closed'],
        status=new_info['status'],
        wait_times=new_info['wait_times'],
        coords_lat=new_info['coords_lat'],
        coords_lon=new_info['coords_lon'],
        type=new_info['type'],
        tele=new_info['tele'],
    )
    # 将新的餐厅对象添加到数据库中
    session.add(new_cafeteria)
    # 试图提交更改到数据库中
    try:
        session.commit()
    # 如果提交更改失败，则返回错误的HTTP响应状态码
    except:
        return make_response(jsonify({'message': "Database execution failed."}), 403)
    # 如果提交更改成功，则返回成功的HTTP响应状态码
    return make_response(jsonify({'message': "Succeed."}), 201)
 