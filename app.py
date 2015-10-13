from flask import Flask, render_template, jsonify, request, redirect, url_for
import os
import operator
import json
app = Flask(__name__)



@app.route("/data")
def data():
    with open("csvtojson.json") as data_file:
        data = json.load(data_file)

    return jsonify({"data":data})


@app.route('/pref')
def pref():

    name = request.args.get('name',"fed")

    with open(name+".json") as data_file:
        data = json.load(data_file)
    with open(name+"cityGraph.json") as data_file:
        cityGraph = json.load(data_file)

    data[0] = cityGraph

    return jsonify({"data":data})

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/rend")
def rend():

    return render_template("pro.html")
@app.route("/mos")
def mos():

    return render_template("mos.html")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)
