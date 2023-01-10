# This is a tiny flask app to test the RESTful API for Map.


from flask import Flask, jsonify, request
from flask import render_template, redirect, make_response
import requests
import json
from model import Cafeteria, sett, gordon, capital
app = Flask(__name__)
centerIndex = -1 # the center of map, it's ID of cafeteria, map will center on this cafeteria, if it's -1, center on Madison
proxy = "http://127.0.0.1:8080" # backend API route

# fetch data from backend, create a list of cafeteria object from it
# return: list of Cafeteria object
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

# redirect to map
@app.route("/")
def index():
    return redirect("/map")

# render the map page
@app.route("/map", methods=['GET', 'POST'])
def map():
    # get centerIndex to see if need to center at certain cafeteria
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
        "咖啡厅"      : cafes,
        "食堂":dinings
    }
    return make_response(render_template("dashboard.html", type_dict = type_dict))

# render worker page from cafeteria's ID
@app.route("/home/<cafe_id>",methods=['GET','POST'])
def method_name(cafe_id):
    cafeterias = create_object()
    selected_cafe = None
    for cafeteria in cafeterias:
        if int(cafeteria.id) == int(cafe_id):
            selected_cafe = cafeteria
    if not selected_cafe:
        return make_response("Invalid cafeteria id.", 403)
    return make_response(render_template("worker.html", cafeteria = selected_cafe, proxy = proxy))

# This is API which will be called by worker page
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
    # map from url string to string sent to backend
    wait_dict = {
        "lt5min" : "< 5 min",
        "5-15min"  : "5 - 15 min",
        "gt20min" : "> 20 min",
        "< 5 min" : "< 5 min",
        "5 - 15 min" : "5 - 15 min",
        "> 20 min" : "> 20 min"
    }
    # if arg contain status, use that one, if not, use old one
    changed_cafe.status = request.args.get("status", changed_cafe.status)
    # same as status, but one more pipeline mapped by wait_dict
    changed_cafe.wait_times = wait_dict[request.args.get("wait_times", changed_cafe.wait_times)]
    # convert dict to json
    to_update = json.dumps(changed_cafe.getAttr())
    url = proxy+"/location/"+cafe_id
    # send json to backend with put method
    response = requests.put(url=url,data=to_update)
    # don't return response because backend side didn't give a valid response
    return "Done"

# This will called by dashboard page to assign the center of map
@app.route("/highlight", methods = ['GET','POST'])
def highlight():
    global centerIndex
    response = json.dumps([centerIndex])
    # Change it back to -1 because center at cafeteria is not default behavior
    centerIndex = -1
    return response
    

# This API will be called by map script to give a json file of cafeterias
@app.route("/locations", methods = ['GET','POST'])
def locations():
    cafeterias = create_object()
    dict_list = []
    # get list of dict of cafeteria attr
    for c in cafeterias:
        dict_list.append(c.getAttr())
    # jsonify and return
    return jsonify(dict_list)

if __name__ == '__main__':
    app.run(debug=True)