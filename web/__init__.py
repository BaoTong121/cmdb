
from flask import Flask, make_response, request, render_template, jsonify
app = Flask(__name__)


@app.route('/ip')
def index():
    return "i am kone"