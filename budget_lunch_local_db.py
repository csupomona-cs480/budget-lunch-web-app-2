from flask import Flask, render_template, send_from_directory, send_file, request
import os

app = Flask(__name__)

lunch_db = [
    {
        "name" : "pizza",
        "price" : 6.99,
        "imageurl" : "https://ooni.com/cdn/shop/articles/20220211142347-margherita-9920_ba86be55-674e-4f35-8094-2067ab41a671.jpg?v=1737104576&width=1080"
    },
    {
        "name" : "salad",
        "price" : 5.99,
        "imageurl" : "https://cdn.loveandlemons.com/wp-content/uploads/2021/04/green-salad.jpg"
    },
    {
        "name" : "soda",
        "price" : 1.99,
        "imageurl" : "https://i5.walmartimages.com/asr/bba96e0f-0444-4b2b-8e55-d90edf928e00.cf87606a804ac13e7807cd48dbd53792.jpeg"
    },    
    {
        "name" : "coffee",
        "price" : 2.99,
        "imageurl" : "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQO9TfIFqT5Np6d9CSiJB0QdXnOGE2NPaOXGQ&s"
    }
]

@app.route("/search/<price>")
def search_food_with_price(price):
    price = float(price)
    res = []
    for food in lunch_db:
        if food["price"] <= price:
            res.append(food)
    return res

@app.route("/add/<name>/<price>")
def add_food_item(name, price):
    price = float(price)
    imageurl = request.args.get('imageurl')
    lunch_db.append({
        "name" : name,
        "price" : price,
        "imageurl" : imageurl
    })
    return "OK"



@app.route("/")
def home():
    return send_file('index.html')

@app.route("/add.html")
def server_add_html():
    return send_file('add.html')


@app.route("/styles.css")
def serve_css():
    return send_file('styles.css', mimetype='text/css')

@app.route("/script.js")
def serve_js():
    return send_file('script.js', mimetype='application/javascript')

@app.route("/script_add.js")
def serve_js_add():
    return send_file('script_add.js', mimetype='application/javascript')


@app.route("/hello")
def show_hello_world():
    return "Welcome to CS4800 Software Engineering"


# app.run(host = "0.0.0.0", port = 5002)