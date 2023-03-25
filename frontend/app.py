from flask import Flask, jsonify, request, flash, url_for
from flask import render_template, redirect, make_response
import requests
import json
from model import Cafeteria
# 初始化 Flask 应用
app = Flask(__name__)
# 设置应用的密钥，用于加密会话数据
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba250'

# centerIndex 为地图中心的索引值，默认为 -1，表示以山东工商学院为中心
centerIndex = -1

# 后端 API 的地址，代理用于处理与后端的通信
proxy = "http://127.0.0.1:8080"

# 存储登录的 token
token = ""
# 从后端获取数据，从中创建自助餐厅对象列表 
 # return：餐厅对象列表 
# 从后端获取数据，创建自助餐厅对象列表
# 返回值：餐厅对象列表
def create_object():
    try:
        # 获取自助餐厅信息的响应
        response = requests.get(proxy+"/location").text
    except:
        # 如果获取失败，返回一个空列表
        response = "[]"
    # 将 JSON 字符串解析为字典列表
    dict_list = json.loads(response)
    cafeterias = []
    # 根据字典创建自助餐厅对象，并添加到列表中
    for c_dict in dict_list: 
        cafeterias.append(Cafeteria(c_dict))
    # 打印餐厅列表
    print(cafeterias)
    return cafeterias

# 重定向到地图页面
@app.route("/")
def index():
    return redirect("/map") 

# 渲染地图页面
@app.route("/map", methods=['GET', 'POST'])
def map():
    # 获取 centerIndex，查看是否需要在某个自助餐厅居中
    global centerIndex
    centerIndex = int(request.args.get("highlight","-1"))
    response = make_response(render_template("map.html"))
    # 允许跨域访问
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# 处理餐厅对象列表，将它们分类成 dict，然后用 dict 渲染 dashboard 页面
@app.route("/dashboard",methods=['GET','POST'])
def table():
    # 创建餐厅对象列表
    cafeterias = create_object()
    # 分类
    cafes = []
    dinings = []
    fasts = []
    for c in cafeterias:
        if c.type == "Cafe":
            cafes.append(c)
        elif c.type == "Dining":
            dinings.append(c)
        elif c.type == "Fast Food":
            fasts.append(c)
    # 将分类结果存储到字典中，用于在页面上渲染
    type_dict = {
        "快餐" : fasts,
        "咖啡厅" : cafes,
        "食堂":dinings
    }
    return make_response(render_template("dashboard.html", type_dict = type_dict))

# 从餐厅的 ID 渲染工作页面
@app.route("/home/<cafe_id>")
def home(cafe_id):
    global token
    response = requests.get(url=proxy+"/verify?token="+token+"&id="+str(cafe_id))
    if response.status_code != 200:
        token = ""
        return make_response(render_template('denied.html'))
    cafeterias = create_object()
    selected_cafe = None
    for cafeteria in cafeterias:
        if int(cafeteria.id) == int(cafe_id):
            selected_cafe = cafeteria
    if not selected_cafe:
        return make_response("Invalid cafeteria id.", 403)
    return make_response(render_template("worker.html", cafeteria = selected_cafe, proxy = proxy))

# 员工界面
# 工作页面将通过传递一些查询字符串来调用此 API
@app.route("/location/<cafe_id>",methods=['GET'])
def update(cafe_id):
    cafeterias = create_object()
    changed_cafe = None
    # 检查 cafe_id 是否有效
    for cafeteria in cafeterias:
        if cafeteria.id == int(cafe_id):
            changed_cafe = cafeteria
    if not changed_cafe:
        return make_response("Invalid cafeteria id.", 403)
    # 将数据发送到后端
    wait_dict = {
        "lt5min" : "< 5 min",
        "5-15min"  : "5 - 15 min",
        "gt20min" : "> 20 min",
        "< 5 min" : "< 5 min",
        "5 - 15 min" : "5 - 15 min",
        "> 20 min" : "> 20 min"
    }
    # 如果arg包含状态，则使用该状态，如果不包含，则使用旧状态
    changed_cafe.status = request.args.get("status", changed_cafe.status)
    # same as status, but one more pipeline mapped by wait_dict
    #与状态相同，但wait_div映射了另一个管道
    changed_cafe.wait_times = wait_dict[request.args.get("wait_times", changed_cafe.wait_times)]
    # convert dict to json
    to_update = json.dumps(changed_cafe.getAttr())
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
        }
    url = proxy+"/update?id="+cafe_id+"&token="+token
    # 使用put方法将json发送到后端
    response = requests.put(url=url,headers=headers,json=to_update)
    # 不返回响应，因为后端没有给出有效响应
    return "Done"

# 这将由dashboard页面调用以分配地图中心
@app.route("/highlight", methods = ['GET','POST'])
def highlight():
    global centerIndex
    response = json.dumps([centerIndex])
    # 将其改回-1，因为自助餐厅中心不是默认行为
    centerIndex = -1
    return response
    

@app.route('/login',methods = ['POST'])
def login():
    global token
    body = request.json
    url = proxy+ "/login"
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
        }
    print(body)
    response = requests.post(url=url, headers=headers, json=body)
    if response.status_code != 200:
        return make_response(jsonify(
            {
                'message' : "Login Failed."
            }
        ), 404)
    token = response.json()['token']
    return make_response(jsonify(
            {
                'message' : "Login Successfully."
            }
        ), 200)

@app.route('/logout')
def logout():
    global token
    token = ""
    return make_response(jsonify(
            {
                'message' : "Logout Successfully."
            }
        ), 200)

# map脚本将调用此API，以提供自助餐厅的json文件
@app.route("/locations", methods = ['GET','POST'])
def locations():
    cafeterias = create_object()
    dict_list = []
    # 获取自助餐厅属性的dict列表
    for c in cafeterias:
        dict_list.append(c.getAttr())
    #  JSON化并返回
    return jsonify(dict_list)

if __name__ == '__main__':
    app.run(debug=True)