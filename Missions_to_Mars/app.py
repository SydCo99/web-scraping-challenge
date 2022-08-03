from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)


app.config["MONGO_URI"] = "mongodb://localhost:27017/marshome"
mongo = PyMongo(app)
# Use flask_pymongo to set up mongo connection
# conn = "mongodb://localhost:27017/mars"
# client = pymongo.MongoClient(conn)
# db = client.mars

@app.route("/")
def index():
    # find one document from our mongo db and return it.
    marshome = mongo.db.marshome.find_one()
    # pass that listing to render_template
    return render_template("index.html", marshome=marshome)

@app.route("/scrape")
def scraper():
    marshome = mongo.db.marshome
    mars_data = scrape_mars.scrape()
    #marshome.update({}, mars_data, upsert=True)
    print(mars_data)
    marshome.update_one({}, {"$set": mars_data}, upsert=True) 
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)

