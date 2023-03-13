from flask import Flask, jsonify, request, flash, url_for
from flask import render_template, redirect, make_response
import requests
import json
from model import Cafeteria, sett, gordon, capital
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba250'
centerIndex = -1 # 地图的中心，是自助餐厅的ID，地图将以这家自助餐厅为中心，如果是-1，则以山东工商学院为中心
proxy = "http://127.0.0.1:8080" # backend API route
token = ""
# 从后端获取数据，从中创建自助餐厅对象列表
# return：自助餐厅对象列表 
def create_object():
    try:
        response = requests.get(proxy+"/location").text
    except:
        response = "[]"
    dict_list = json.loads(response)
    cafeterias = [sett, gordon, capital]
    for c_dict in dict_list:
        cafeterias.append(Cafeteria(c_dict))
    return cafeterias

#重定向到地图
@app.route("/")
def index():
    return redirect("/map")

# render the map page
@app.route("/map", methods=['GET', 'POST'])
def map():
    # 获取centerIndex，查看是否需要在某个自助餐厅居中
    global centerIndex
    centerIndex = int(request.args.get("highlight","-1"))
    response = make_response(render_template("map.html"))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Process list of cafeterias object, classify them into dict, then render dashboard page with dict
@app.route("/dashboard",methods=['GET','POST'])
def table():
    cafeterias = create_object()
    cafes = []
    dinings = []
    fasts = []
    # classify cafeteria according to their type
    for c in cafeterias:
        if c.type == "Cafe":
            cafes.append(c)
        elif c.type == "Dining":
            dinings.append(c)
        elif c.type == "Fast Food":
            fasts.append(c)
    type_dict = {
        "快餐" : fasts,
        "咖啡厅" : cafes,
        "食堂":dinings
    }
    return make_response(render_template("dashboard.html", type_dict = type_dict))

# render worker page from cafeteria's ID
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
# The worker page will call this API with passing some query string
@app.route("/location/<cafe_id>",methods=['GET'])
def update(cafe_id):
    cafeterias = create_object()
    changed_cafe = None
    # check if cafe_id valid
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
    # send json to backend with put method
    response = requests.put(url=url,headers=headers,json=to_update)
    # don't return response because backend side didn't give a valid response
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
    #  jsonify and return
    return jsonify(dict_list)

if __name__ == '__main__':
    app.run(debug=True)