from flask import Flask
from flask import jsonify
from datetime import datetime
from waitress import serve
from data_manager import *

"""
Sets up flask server for returning JSON result of GetData([location list])
"""

locations = ["Middlewich, UK", "Colorado Springs, Colorado", "Tokyo, Japan", "Melbourne, Australia", "Cupertino, California", "Mumbai, India", "New York City, New York", "Wilmington, Delaware"]

app = Flask(__name__)

@app.route("/")
def home():
    data = GetData(locations)
    return data

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080) #WAITRESS!