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
###########################################
#导入必要的依赖库，包括Flask、json、requests等。
# 创建一个Flask应用实例，该应用实例是Python Flask Web应用程序的基础。
# 初始化应用的密钥，用于加密会话数据。
# 设置centerIndex变量为-1，代表以山东工商学院为中心。
# 设置后端API的地址为http://127.0.0.1:8080，代理用于处理与后端的通信。
# 定义一个create_object()函数，用于从后端获取数据，并创建自助餐厅对象列表。
# 在create_object()函数中，首先使用requests库发送一个GET请求到后端API的地址，获取自助餐厅信息的响应。如果获取失败，则返回一个空列表。
# 将JSON字符串解析为字典列表，遍历字典列表，根据字典创建自助餐厅对象，并添加到列表中。
# 返回餐厅对象列表。
# 运行逻辑为：当Flask应用程序启动后，会调用create_object()函数从后端API获取自助餐厅信息，并创建自助餐厅对象列表。然后，应用程序会根据请求的URL，调用相应的函数，渲染HTML模板或返回JSON数据。在此过程中，应用程序还可以处理HTTP请求和响应，以及与后端API进行通信。
############################################
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
#

############################################
#这段代码定义了一个函数create_object()，
# 它的作用是从后端API获取自助餐厅信息，
# 将信息转换为字典列表，并创建自助餐厅对象列表。
#首先，在try-except语句块中，
# 发送一个GET请求到后端API地址（proxy+"/location"），
# 获取自助餐厅信息的响应。如果请求失败，则返回一个空列表"[]"。
#接着，将JSON字符串解析为字典列表，
# 使用json.loads()方法将response转换为字典列表dict_list。
#然后，创建一个空列表cafeterias，
# 用于存储创建的自助餐厅对象。
# 使用for循环遍历字典列表dict_list，
# 对于每个字典，创建一个Cafeteria对象，将其添加到cafeterias列表中。
#最后，输出打印cafeterias列表，并将其作为函数的返回值。
#该函数的运行逻辑为：当该函数被调用时，它将从后端API获取自助餐厅信息，
# 将其转换为字典列表，创建自助餐厅对象列表，并输出打印该列表。
# 最后，将自助餐厅对象列表作为函数的返回值，供其他函数使用。
# 如果无法从后端API获取自助餐厅信息，则返回一个空列表。
############################################

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
############################################
#这段代码定义了两个路由函数，分别为 "/" 和 "/map"，具体运行逻辑如下：
# "/" 路由函数：该函数通过 redirect 函数将请求重定向到 "/map" 路由函数处理。
# "/map" 路由函数：该函数处理地图页面的请求。
# 如果收到 POST 请求，则返回包含在请求中的参数（如表单数据）；
# 否则，返回地图页面的 HTML 模板。
# 在处理 GET 请求时，函数首先通过 request.args.get() 获取 URL 中的 highlight 参数，
# 并将其转换为整数。如果 highlight 参数不存在或无效，
# 则将 centerIndex 的值设置为 -1。
# 接下来，函数使用 render_template() 渲染地图页面的 HTML 模板，并将其返回。
# 在返回之前，函数使用 make_response() 函数将 HTML 模板包装成一个响应对象，
# 该响应对象包含 "Access-Control-Allow-Origin" 响应头，以允许跨域访问。
# 总之，该函数主要的功能是渲染地图页面的 HTML 模板，
# 并将其作为响应对象返回给客户端。
# 如果请求中包含参数，则将其作为响应的一部分返回。
############################################

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

############################################
#这段代码定义了一个Flask路由，用于在页面上呈现自助餐厅数据的dashboard。
# 首先，代码调用create_object()函数，
# 该函数从后端API获取自助餐厅信息并返回一个自助餐厅对象列表。
# 然后，代码对自助餐厅对象列表进行分类，
# 将咖啡厅、食堂和快餐店分别存储到列表cafes、dinings和fasts中。
# 接下来，代码创建一个字典type_dict，将分类结果存储到其中，以便在页面上呈现数据。
# 最后，代码使用Flask的render_template()方法将type_dict作为参数传递给dashboard.html文件，该文件用于呈现自助餐厅数据的表格。
# 代码最终使用Flask的make_response()方法将渲染后的HTML页面作为响应返回。
############################################


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
############################################
#这段代码定义了一个路由，当访问 "/home/<cafe_id>" 时会执行对应的函数 "home(cafe_id)"，其中 "<cafe_id>" 是一个动态参数，表示餐厅的 ID。函数的主要逻辑如下：

#发送 HTTP GET 请求到代理服务器，验证登录令牌和餐厅 ID 的有效性。
#如果验证失败，则清除登录令牌并显示拒绝访问页面。
#加载所有餐厅数据。
#查找当前餐厅 ID 对应的餐厅数据。
#如果找不到当前餐厅 ID 对应的餐厅数据，则返回 403 错误。
#渲染工作页面，并传递当前餐厅数据和代理服务器的 URL 参数。
#具体来说，第 1 步中发送的请求是带有验证信息的 GET 请求，其中 token 是登录令牌，cafe_id 是餐厅 ID。
# 代理服务器会根据这些信息判断用户是否有权限访问指定的餐厅。
# 如果验证失败，服务器会返回一个非 200 的状态码，此时程序会清除登录令牌并显示拒绝访问页面。
# 如果验证成功，则继续执行后面的逻辑。
#第 2 步中加载所有餐厅数据的操作与之前的代码逻辑相同。
#第 3 步中查找当前餐厅 ID 对应的餐厅数据，需要遍历所有的餐厅对象，找到与 cafe_id 相等的对象，并将其保存在 selected_cafe 变量中。
#第 4 步中检查 selected_cafe 是否为 None，如果是则表示没有找到对应的餐厅数据，此时返回 403 错误。
#第 5 步中渲染工作页面，并将当前餐厅数据和代理服务器的 URL 参数传递给模板，用于在页面上显示。
############################################
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


#################################################
#这段代码定义了一个 update 路由函数，其作用是接受来自前端的 GET 请求并更新餐厅的状态信息。该函数的执行逻辑如下：
#调用 create_object() 函数创建 cafeterias 列表，用于存储所有的餐厅对象。
#遍历 cafeterias 列表，查找与传入的 cafe_id 相等的餐厅对象，并将其赋值给变量 changed_cafe。
#如果 changed_cafe 为空，则表示传入的 cafe_id 无效，返回 HTTP 状态码 403 和错误消息。
#如果 changed_cafe 不为空，则使用字典 wait_dict 将前端传入的等待时间字符串映射到真实的等待时间值，并将其赋值给 changed_cafe.wait_times 属性。
#同样地，将前端传入的状态字符串赋值给 changed_cafe.status 属性。
#将 changed_cafe 对象转化为 JSON 格式，并使用 HTTP PUT 请求将其发送到后端服务器。
#返回字符串 "Done"，表示更新已完成。
#注意，该函数使用了全局变量 token 和 proxy，因此在函数执行之前需要先设置它们的值。另外，该函数只能处理 GET 请求，如果收到 POST 请求或其他类型的请求，则会抛出 HTTP 405 错误。
#################################################


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

###################################
#这段代码定义了一个名为 "highlight" 的路由，可以处理 GET 和 POST 请求。
# 它首先使用全局变量 centerIndex 创建一个 JSON 响应，然后将 centerIndex 设置为默认值 -1。
# 这个全局变量用于标记当前突出显示的餐厅在列表中的位置。
# 这段代码的作用是将当前选定的餐厅重新设置为默认值，以便在下一次请求时重新选择要突出显示的餐厅。
###################################




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

###########################
#这段代码实现了一个登录功能。
# 当接收到POST请求并且路由与'/login'匹配时，调用login()函数进行处理。
# login()函数首先从请求对象中获取JSON格式的请求体，存储到变量body中。
# 然后构造请求头，定义了客户端接受的响应类型是JSON，客户端发送的请求类型是JSON。
# 接着，使用requests库发送POST请求到后端的/login路由，并传递请求体和请求头，返回响应对象response。
# 如果响应状态码不是200，构造响应对象，返回HTTP 404响应，包含错误信息"Login Failed."。
# 如果响应状态码是200，则从响应体中获取token并存储到全局变量token中。
# 最后，构造响应对象，返回HTTP 200响应，包含成功信息"Login Successfully."。
###########################





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

##################
#这段代码定义了一个名为 logout() 的函数，并将其绑定到路由 /logout 上，当接收到 HTTP GET 请求并且路由与 /logout 匹配时，调用该函数进行处理。
#该函数将全局变量 token 的值置为空字符串，表示当前用户已经退出登录。
# 然后构造一个 JSON 格式的响应消息，包含键名为 'message'，键值为退出成功的消息。
# 最后将该响应消息封装到 HTTP 200 响应对象中，并返回给客户端。
# API路由，以提供自助餐厅位置的JSON文件
##################

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
#########################
#这段代码实现了一个用于获取自助餐厅属性的API接口。
# 当客户端发送GET请求到路径"/locations"时，会触发locations()函数的执行。l
# ocations()函数首先调用create_object()函数创建一个自助餐厅对象列表，然后遍历这个列表，获取每个自助餐厅对象的属性字典，并将这些字典添加到一个列表中。
# 最后，locations()函数将这个列表转换为JSON格式并返回给客户端。
#如果客户端发送了POST请求到路径"/locations"，则会执行相同的逻辑，并返回JSON格式的自助餐厅属性列表。
#########################



if __name__ == '__main__':
    app.run(debug=True)