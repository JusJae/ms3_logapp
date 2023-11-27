from werkzeug.security import check_password_hash
import os
from flask import (Flask, flash, render_template,
                   url_for, request, redirect, session)
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
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


# User Authentication from CI Walkthrough Project
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # checks if username exists in db
        entered_username = request.form.get("username").lower()
        entered_password = request.form.get("password")

        existing_user = mongo.db.users.find_one({"username": entered_username})

        if existing_user and check_password_hash(existing_user["password"], entered_password):
            # Valid username and password
            session["user"] = entered_username
            flash("Welcome, {}".format(entered_username.capitalize()))
            return redirect(url_for("profile", username=session["user"]))
        else:
            # Invalid username or password
            flash("Incorrect Username and/or Password")

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    if session["user"]:
        return render_template("profile.html", username=username)
    else:
        flash("You must be logged in to view your profile")
    return redirect(url_for("login"))


@app.route("/profile/edit/<username>", methods=["GET", "POST"])
def edit_profile(username):
    current_username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"] and session["user"] == username:
        user_data = mongo.db.users.find_one({"username": current_username})
        # Retrieve the hashed password
        current_password = user_data["password"]

        if request.method == "POST":
            new_username = request.form.get("username").lower()
            new_password = request.form.get("password")
            current_password_input = request.form.get("current_password")

            # Check if the new username already exists in the database
            existing_user = mongo.db.users.find_one(
                {"username": new_username})
            if existing_user and new_username != current_username:
                flash("Username already exists")
                return redirect(url_for("edit_profile", username=username))

            # Check if the current password matches the one in the database
            if check_password_hash(current_password, current_password_input):
                # Update the profile details
                submit = {
                    "username": new_username,
                }

                # Update the password only if it's provided and different
                if new_password and new_password != current_password:
                    submit["password"] = generate_password_hash(new_password)

                mongo.db.users.update_one(
                    {"username": current_username}, {"$set": submit})
                flash("Profile successfully updated")
                return redirect(url_for("profile", username=new_username))
            else:
                flash("Incorrect current password")
                return redirect(url_for("edit_profile", username=username))

        return render_template("edit_profile.html", username=current_username, password=current_password)

    else:
        flash("You must be logged in to view your profile")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out")
    return redirect(url_for("home"))


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get('query') or ''
    user = session.get('user', '')

    if not user:
        flash("You must be logged in to search products")
        return redirect(url_for("login"))
    else:
        products = list(mongo.db.products.find(
            {"$and": [{"created_by": user}, {"$text": {"$search": query}}]}))
        return render_template("products.html", products=products)


@app.route("/products")
def products():
    if session['user'] == '':
        flash("You must be logged in to view products")
        return redirect(url_for("login"))
    else:
        user = session['user']
        products = list(mongo.db.products.find({"created_by": user}))
    return render_template("products.html", products=products)


@app.route("/products/<product_id>")
def product(product_id):
    product = mongo.db.products.find_one({"_id": ObjectId(product_id)})
    return render_template("product.html", product=product)


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
            "date_added": date_added,
            "created_by": session.get('user', '')
        }

        mongo.db.products.insert_one(product)
        flash("Product successfully added")
        return redirect(url_for("products"))

    product_categories = mongo.db.categories.find().sort("product_category_name", 1)
    return render_template("add_product.html", product_categories=product_categories)


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
            "date_added": date_added,
            "created_by": session['user']
        }

        mongo.db.products.update_one({"_id": ObjectId(product_id)}, {
            "$set": submit})
        flash("Product successfully updated")
        product_categories = mongo.db.categories.find().sort("product_category_name", 1)
    return render_template("edit_product.html", product=product, product_categories=product_categories)


@app.route("/delete_product/<product_id>")
def delete_product(product_id):
    mongo.db.products.delete_one({"_id": ObjectId(product_id)})
    flash("Product successfully deleted")
    return redirect(url_for("products"))


@app.route("/categories")
def categories():
    product_categories = list(
        mongo.db.categories.find().sort("product_category_name", 1))
    return render_template("product_categories.html", product_categories=product_categories)


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        product_category_name = request.form.get('product_category_name')
        product_category_description = request.form.get(
            'product_category_description')
        category = {
            "product_category_name": product_category_name,
            "product_category_description": product_category_description
        }
        mongo.db.categories.insert_one(category)
        flash("Product Category successfully added")
        return redirect(url_for("categories"))
    return render_template("add_category.html")


@app.route("/edit_category/<category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    if request.method == "POST":
        product_category_name = request.form.get('product_category_name')
        product_category_description = request.form.get(
            'product_category_description')
        submit = {
            "product_category_name": product_category_name,
            "product_category_description": product_category_description
        }
        mongo.db.categories.update_one({"_id": ObjectId(category_id)}, {
            "$set": submit})
        flash("Product category successfully updated")
        return redirect(url_for("categories"))

    product_category = mongo.db.categories.find_one(
        {"_id": ObjectId(category_id)})
    return render_template("edit_category.html", product_category=product_category)


@app.route("/delete_category/<category_id>")
def delete_category(category_id):
    mongo.db.categories.delete_one({"_id": ObjectId(category_id)})
    return redirect(url_for("categories"))

# Error Handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500



if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True)
