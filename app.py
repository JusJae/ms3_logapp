import os
from flask import Flask, flash, render_template, url_for, request, redirect
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env

UPLOAD_FOLDER = 'static/images/uploaded_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg', 'webp', 'heic'}


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mongo = PyMongo(app)
mongo.db = mongo.cx[app.config["MONGO_DBNAME"]]


@app.route("/")
@app.route("/home")
def home():
    products = mongo.db.products.find()  # type: ignore
    return render_template("home.html", products=products)


@app.route("/products")
def products():
    products = mongo.db.products.find()  # type: ignore
    return render_template("products.html", products=products)


@app.route("/product_list")
def product_list():
    products = mongo.db.products.find()  # type: ignore
    return render_template("product_list.html", products=products)


@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        product_name = request.form.get('product_name')
        product_category = request.form.get('product_category')
        product_notes = request.form.get('product_notes')
        date_added = request.form.get('date_added')

        # Handle the image file
        image_file = request.files.get('image_url')
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(file_path)
            # URL to access the image
            image_url = f'/static/images/uploaded_images/{filename}'
        else:
            image_url = ''  # No image uploaded

        product = {
            "product_name": product_name,
            "product_category": product_category,
            "product_notes": product_notes,
            "image_url": image_url,
            "date_added": date_added
        }

        mongo.db.products.insert_one(product)
        # Return the product data in the response
        flash("Product successfully added")
        return redirect(url_for("home"))

    return render_template("add_product.html")


@app.route("/edit_product/<product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    product = mongo.db.products.find_one({"_id": ObjectId(product_id)})
    if request.method == "POST":
        product_name = request.form.get('product_name')
        product_category = request.form.get('product_category')
        product_notes = request.form.get('product_notes')
        date_added = request.form.get('date_added')

        # Handle the image file
        image_file = request.files.get('image_url')
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(file_path)
            # URL to access the image
            image_url = f'/static/images/uploaded_images/{filename}'
        else:
            image_url = ''  # No image uploaded

        submit = {
            "product_name": product_name,
            "product_category": product_category,
            "product_notes": product_notes,
            "image_url": image_url,
            "date_added": date_added
        }

        mongo.db.products.update_one({"_id": ObjectId(product_id)}, {
            "$set": submit})
        flash("Product successfully updated")
        return redirect(url_for("home"))
    return render_template("edit_product.html", product=product)


@app.route("/delete_product/<product_id>")
def delete_product(product_id):
    # Your code here
    pass


@app.route("/register", methods=["GET", "POST"])
def register():
    # Your code here
    pass


@app.route("/login", methods=["GET", "POST"])
def login():

    pass


@app.route("/logout")
def logout():

    pass


@app.route("/profile")
def profile():

    pass


@app.route("/search")
def search():

    pass


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True)
