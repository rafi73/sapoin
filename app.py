import os
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient
from bson.json_util import dumps
import json

app = Flask("DockerTutorial")

# To change accordingly 
# print(os.environ)
client = MongoClient(os.environ["DB_PORT_27017_TCP_ADDR"], 27017)
db = client.appdb

@app.route("/")
def index():
    _items = db.appdb.find()
    items = [items for items in _items]

    return render_template("index.html", items=items)


@app.route("/new", methods=["POST"])
def new():
    data = {
        "helloworld": request.form["helloworld"]
    }

    db.appdb.insert_one(data)

    return redirect(url_for("index"))




@app.route("/logs", methods = ['POST'])
def add_contact():
    try:
        data = json.loads(request.data)
        # status = db.Contacts.insert_one(data)
        status = db.Contacts.insert(data)
        return dumps({'message' : 'SUCCESS'})
    except Exception as e:
        return dumps({'error' : str(e)})

@app.route("/logs", methods = ['GET'])
def get_all_contact():
    try:
        contacts = db.Contacts.find()
        return dumps(contacts)
    except Exception as e:
        return dumps({'error' : str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)