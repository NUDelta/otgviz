import json

from flask import Flask, redirect, url_for, session, request, render_template, jsonify

from werkzeug import secure_filename

from pymongo import MongoClient

import pandas as pd

app = Flask(__name__, static_url_path='/static')

app.debug = True

@app.route('/', methods = ['GET', 'POST'])
def index():
    """
    example coordinates json
    {
        "routeCoordinates": [[0,1],[0,1]]
    }
    """
    if request.method == 'POST':
        f = request.files['file']
        # f.save(secure_filename(f.filename))

        data = json.load(f)

        data["filename"] = f.filename

        return render_template('index.html', data = data)
    else:
        data = {"coordinates": [], "filename": ""}
        return render_template('index.html', data = data)

@app.route('/helpviz')
def helpViz():
    """
    this is for YK field deployment help viz
    """
    df = pd.read_json('data/helpFinal.json')
    df = df.fillna(0)

    # param = ['didHelp', 'helpCoordinate', 'helpDistance', 'helpIndex','helpTime', 'locX', 'locY',
    #         'notiCoordinate', 'notiDistance', 'notiIndex', 'notiTime', 'routeAccuracy', 'routeCoordinates',
    #         'routeSpeed', 'routeTimestamps', 'user', 'localTime', 'weekday', 'hour', 'condition']

    dfUser = pd.read_csv("data/user.csv")

    data = {}
    for key in df.keys():
        # if key in param:
        if key == "didHelp":
            data[key] = ["True" if x == True else "False" for x in list(df[key])]
        else:
            data[key] = list(df[key])

    data["key"] = []
    for i in range(0, len(data["didHelp"])):
        data["key"].append(str(i) + ". " + str(data["user"][i]) + " " + str(data["condition"][i]) + " " + str(data["didHelp"][i]))

    return render_template('help.html', data=data)


# @app.route('/uploader', methods = ['GET', 'POST'])
# def upload_file():
#    if request.method == 'POST':
#       f = request.files['file']

#       data = json.load(f)
#       print data
#       # return redirect('/', data=data)
#       return render_template('index.html', data = data)
#       # df = pd.read_json(f)
#       # print df
#       # return 'file uploaded successfully'

if __name__ == "__main__":
    app.run()
