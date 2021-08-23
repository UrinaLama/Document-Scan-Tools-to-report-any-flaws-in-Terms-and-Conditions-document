from flask import Flask, jsonify, request, render_template

import os
from flask import Flask,jsonify, request
from script.scrape import get_important_lines
from script.model import get_classified_lines
import json

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def get_d():
    if request.method == 'GET':
        return render_template('home.html', data = None)
    else:
        url = request.form['url']
        important_lines = get_important_lines(url)
        classified_lines = get_classified_lines(important_lines)
        return render_template('home.html', data = classified_lines)

