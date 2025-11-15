# Flask server 
from flask import Flask, jsonify, request

# create Flask app and run
app = Flask(__name__)
@app.route('/')
def home():
    return "Welcome to the Flask server!"