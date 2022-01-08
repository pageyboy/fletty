from flask import Flask
from datetime import datetime
from waitress import serve

app = Flask(__name__)

locations = []

@app.route("/")
def main():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080) #WAITRESS!