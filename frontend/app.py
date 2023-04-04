from flask import Flask, jsonify, request, flash, url_for
from flask import render_template, redirect, make_response
import requests
import json
from model import Cafeteria
#这段代码是一个Python Flask应用程序的入口文件，它首先导入了一些必要的依赖库：
# Flask：是一个轻量级的Web应用框架，提供了构建Web应用所需的基本功能。
# jsonify：将数据转换为JSON格式的工具。
# request：处理HTTP请求的工具。
# flash、url_for、render_template、redirect、make_response：用于渲染HTML模板和处理HTTP响应的工具。
# requests：用于处理HTTP请求的Python库。
# json：用于处理JSON数据的Python库。
# Cafeteria：自定义的模型类，用于表示餐厅。
# 接下来，代码创建了一个Flask应用实例，其名称由__name__变量确定。此应用程序是Python Flask Web应用程序的基础。此应用程序的功能在后续的代码中定义和实现。
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
    # 发送 HTTP GET 请求，验证登录令牌和餐厅 ID 的有效性
    response = requests.get(url=proxy+"/verify?token="+token+"&id="+str(cafe_id))
    # 如果验证失败，则清除登录令牌并显示拒绝访问页面
    if response.status_code != 200:
        token = ""
        return make_response(render_template('denied.html'))
    # 加载所有餐厅数据
    cafeterias = create_object()
    # 查找当前餐厅 ID 对应的餐厅数据
    selected_cafe = None
    for cafeteria in cafeterias:
        if int(cafeteria.id) == int(cafe_id):
            selected_cafe = cafeteria
    # 如果找不到当前餐厅 ID 对应的餐厅数据，则返回 403 错误
    if not selected_cafe:
        return make_response("Invalid cafeteria id.", 403)
    # 渲染工作页面，并传递当前餐厅数据和代理服务器的 URL 参数
    return make_response(render_template("worker.html", cafeteria=selected_cafe, proxy=proxy))
#该路由函数通过 Flask 的装饰器语法 @app.route("/home/<cafe_id>") 来定义了一个 URL，
# 其中 <cafe_id> 是一个 URL 变量，用于接收在 URL 中传递的参数。
# 当请求该 URL 时，Flask 将会调用该路由函数，并将 URL 变量 cafe_id 的值作为参数传递给函数。
#在函数内部，首先发送一个 HTTP GET 请求到代理服务器的 /verify 接口，以验证登录令牌和餐厅 ID 的有效性。
# 如果验证失败，则清除登录令牌并显示拒绝访问页面。
#如果验证通过，则加载所有餐厅数据，并查找当前餐厅 ID 对应的餐厅数据。
# 如果找不到当前餐厅 ID 对应的餐厅数据，则返回 403 错误。
#最后，该函数使用 Flask 的 render_template 函数渲染工作页面，并将当前餐厅数据和代理服务器的 URL 参数传递给该页面。

# 员工界面
# 工作页面将通过传递一些查询字符串来调用此 API
@app.route("/location/<cafe_id>",methods=['GET'])
def update(cafe_id):
    # 调用 create_object() 函数创建 cafeterias 列表
    cafeterias = create_object()
    # 初始化变量 changed_cafe，后面会被用来存储找到的咖啡店对象
    changed_cafe = None
    # 检查 cafe_id 是否有效
    for cafeteria in cafeterias:
        # 如果找到一个 id 属性与传入的 cafe_id 相等的咖啡店对象，将其赋值给 changed_cafe
        if cafeteria.id == int(cafe_id):
            changed_cafe = cafeteria
    # 如果 changed_cafe 为空，则表示传入的 cafe_id 无效，返回 403 状态码和错误消息
    if not changed_cafe:
        return make_response("Invalid cafeteria id.", 403)
    # 如果 changed_cafe 不为空，则将 wait_dict 字典中的等待时间字符串映射到真实的等待时间值
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
#代码中首先根据请求参数更新咖啡馆的状态和等待时间信息。
# 如果请求中没有包含状态或等待时间，则使用咖啡馆对象中原有的状态和等待时间。
# 之后，将更新后的咖啡馆信息转化为JSON格式，并发送PUT请求到后端。
# 请求中包括了咖啡馆的ID和token信息，以及JSON格式的更新数据。
# 最后，返回一个字符串表示更新完成。
#在发送PUT请求之前，代码中使用了requests库来设置请求头部信息，
# 包括Accept和Content-Type。Accept头部指定客户端可以接受的响应内容类型，
# 这里设置为application/json。Content-Type头部指定发送的数据类型，
# 这里也设置为application/json。
# 之后，使用requests库的put方法将请求发送到指定的URL。
#由于后端没有给出有效的响应，因此代码中不返回响应内容。


# 这将由dashboard页面调用以分配地图中心
@app.route("/highlight", methods = ['GET','POST'])
def highlight():
    global centerIndex
    response = json.dumps([centerIndex])
    # 将其改回-1，因为自助餐厅中心不是默认行为
    centerIndex = -1
    return response
 #这是一个使用 Flask 构建的 Web 应用程序中的路由函数。
 # 该路由函数对应于 "/highlight" 路径，接受 GET 和 POST 请求。
 # 它的作用是将一个全局变量 centerIndex 的值转换成一个 JSON 格式的响应，
 # 并将 centerIndex 的值重置为 -1，以便下次请求时能够正常处理。
#具体来说，当收到 GET 或 POST 请求时，
# 该函数将 centerIndex 的值放入一个列表中，
# 并将其转换为 JSON 格式的字符串。
# 然后将 centerIndex 的值重置为 -1，以便下次请求时能够正常处理。
# 最后，将 JSON 格式的响应返回给客户端。   






#@app.route('/login',methods = ['POST'])是一个装饰器语法
# 用于将路由/login与login()函数绑定
# 当应用程序接收到POST请求并且路由与/login匹配时
# 就会调用login()函数进行处理。
@app.route('/login',methods = ['POST'])  # 将路由'/login'与login()函数绑定，当接收到POST请求并且路由与'/login'匹配时，调用login()函数进行处理。
def login():
    global token  # 定义全局变量token
    body = request.json  # 从请求对象中获取JSON格式的请求体，存储到变量body中
    url = proxy+ "/login"  # 拼接请求URL
    headers = {  # 定义请求头
        'Accept': 'application/json',  # 客户端接受的响应类型是JSON
        'Content-Type': 'application/json'  # 客户端发送的请求类型是JSON
        }
    print(body)  # 打印请求体
    response = requests.post(url=url, headers=headers, json=body)  # 发送POST请求
    if response.status_code != 200:  # 如果响应状态码不是200
        return make_response(jsonify(  # 构造响应对象，返回HTTP 404响应
            {
                'message' : "Login Failed."  # 错误信息
            }
        ), 404)
    token = response.json()['token']  # 从响应体中获取token并存储到全局变量token中
    return make_response(jsonify(  # 构造响应对象，返回HTTP 200响应
            {
                'message' : "Login Successfully."  # 成功信息
            }
        ), 200)

# 用于登出的API路由
@app.route('/logout')
def logout():
    global token
    token = ""
    return make_response(jsonify(
            {
                'message' : "退出成功。"
            }
        ), 200)

# API路由，以提供自助餐厅位置的JSON文件
@app.route("/locations", methods = ['GET','POST'])
def locations():
    # 创建一个自助餐厅对象列表
    cafeterias = create_object()
    dict_list = []
    # 获取自助餐厅属性的dict列表
    for c in cafeterias:
        dict_list.append(c.getAttr())
    # 将dict列表转换为JSON并返回
    return jsonify(dict_list)

if __name__ == '__main__':
    app.run(debug=True)