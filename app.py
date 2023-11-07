#!/usr/bin/env python

import pymongo
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
from flask_cors import CORS, cross_origin


# create instance of Flask app
app = Flask(__name__)


# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/scrape_mars"
mongo = PyMongo(app)
# or set inline
# mongo=PyMongo(app, uri="mongodb://localhost:27017/scrape_mars")

# _____________________________________________________________________


# create route that renders index.html template
@app.route("/", methods=["GET"])
def index():
    # store the entire image_url collection in a list
    mars_list = mongo.db.mars.find_one()
    return render_template("index.html", mars_hem_list=mars_list)


@app.route("/scrape", methods=["GET"])
def scrape():
    # connect to database
    mars = mongo.db.mars
    # now we scrape; scraped dictionary = scrape_mars.py file (.) def scrape_info()
    mars_data = scrape_mars.scrape_info()
    # this updates the mars database but does not dup info
    mars.update({}, mars_data, upsert=True)
    # instructing browser back to root route home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
