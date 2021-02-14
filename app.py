# Import dependencies 
from flask import Flask, render_template, request, redirect
from flask_pymongo import PyMongo
import scraping

# Set up Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection 
app.config["MONGO_URI"] = 'mongodb://localhost:27017/mars_app' #URI we'll be using to connect out Mongo app
mongo = PyMongo(app) 

# Set up out flask routes 
# @app.route("/") tells Flask what to display when we're looking at the home page, index.html
# when we visit our web app's HTML page, we will see the home page
@app.route("/")
def index():
    # uses PyMongo to find the "mars" collection in our database, which
    #we will create when we convert our Jupyter scraping code to Python
    mars = mongo.db.mars.find_one()
    # tells Flast to run an HTML template using an index.html file 
    # mars=mars tells Python to use the "mars" collection in MongoDB
    return render_template("index.html", mars=mars)

# Function that will set up our scraping route. 
# This route will be the "button" of the web application that will scrape updated data 

# defines the route that Flask will be using
@app.route("/scrape")
def scrape():
    # assign a new variable that points to our Mongo database
    mars = mongo.db.mars
    # create a new variable to hold the newly scraped data
    mars_data = scraping.scrape_all()
    # after gathering data, we need to update the database using .update()
    # .update(query_parameter, data, options "upsert=True" means that we create a new document)
    mars.update({}, mars_data, upsert=True)
    #add a redirect after successfully scraping the data, navigate our page back to /
    #return "Scraping Sucessful!"
    return redirect('/', code=302)

# Tell Flask to run
if __name__ == "__main__":
    app.run()






