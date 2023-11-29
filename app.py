from flask import Flask, render_template, jsonify, request
from optimize import fill_pre, fill_preds, optimize
from optimize_final import run
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

    print("testing")
    
    # Get parameters from the request (assuming they are in JSON format)
    data = request.get_json()
    print('Received data:', data)
    summer = int(data.get('summer'))
    # print("----------------")
    # print(semesters)
    minHours = int(data.get('minHours'))
    # print(minHours)
    maxHours = int(data.get('maxHours'))
    # print(semesters, minHours, maxHours)
    course_list = data.get('course_list')

    df = pd.read_csv('data/ISYE_SAMPLE.csv')
    # print(df)
    df_fill=fill_preds(fill_pre(df))

    # get opt log, a string (for now, some kind of dict later?)
    # opt_log = optimize(semesters, minHours, maxHours, df_fill)
    opt_log = run(course_list, minHours, maxHours, summer=summer)

    print(course_list)

    # opt_log = run(['ISYE 6501', 'ISYE 6414', 'CSE 6242', 'ISYE 6669', 'MGT 8803', 'CSE 6040'], 5, 12, summer=summer)
    # opt_log = [3.6551637842884044, 2, [{'ISYE 6414':3.499326780769436, 'MGT 8803':3.8339323963212553, 'CSE 6040':3.6196010600730615}, {'ISYE 6501': 3.6312633902786087, 'CSE 6242':3.9702462718971048, 'ISYE 6669':3.3766128063909586}]]
    # opt_log = [3.6551637842884044, 2, [[['ISYE 6414',3.499326780769436], ['MGT 8803', 3.8339323963212553], ['CSE 6040', 3.6196010600730615]], [['ISYE 6501', 3.6312633902786087], ['CSE 6242', 3.9702462718971048], ['ISYE 6669', 3.3766128063909586]]]]

    # print(opt_log)

    # we can change this so that we can retrieve {sem1: {...}} or more creative 
    # formats to customize retrieval
    return jsonify({"opt_log":opt_log})

if __name__ == "__main__":
    app.run(debug=True)