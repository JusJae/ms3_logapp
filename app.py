import os
from flask import Flask, render_template, url_for, request, redirect, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)
mongo.db = mongo.cx[app.config["MONGO_DBNAME"]]
db = mongo.db
products = db.products


@app.route("/")
def index():
    return render_template("base.html")


@app.route("/products")
def products():
    products = mongo.db.products.find()  # type: ignore
    return render_template("products.html", products=products)


@app.route("/register", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
@app.route("/logout")
@app.route("/profile")
@app.route("/search")
@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    # Your code here
    pass


@app.route("/edit_product/<product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    # Your code here
    pass


@app.route("/delete_product/<product_id>")
def delete_product(product_id):
    # Your code here
    pass


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True)
