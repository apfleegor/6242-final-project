from flask import Flask, render_template, jsonify, request
from optimize import fill_pre, fill_preds, optimize
import pandas as pd
import numpy as np
import random
import copy
import pulp as pp
import math
import sys
pd.options.mode.chained_assignment = None

# create instance of Flask
app = Flask(__name__)

# create root route
@app.route('/')
def home():
    # note: can send data to index.html through this function
    return render_template("index.html")

@app.route('/run_optimization', methods=['POST'])
def run_optimization():
    
    # Get parameters from the request (assuming they are in JSON format)
    data = request.get_json()
    # print('Received data:', data)
    semesters = int(data.get('semesters'))
    minHours = int(data.get('minHours'))
    maxHours = int(data.get('maxHours'))
    # print(semesters, minHours, maxHours)

    df = pd.read_csv('data/ISYE_SAMPLE.csv')
    # print(df)
    df_fill=fill_preds(fill_pre(df))
    # get opt log, a string (for now, some kind of dict later?)
    opt_log = optimize(semesters, minHours, maxHours, df_fill)
    # we can change this so that we can retrieve {sem1: {...}} or more creative 
    # formats to customize retrieval
    return jsonify({"opt_log":opt_log})

if __name__ == "__main__":
    app.run(debug=True)