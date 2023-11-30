from flask import Flask, render_template, jsonify, request
from optimize import fill_pre, fill_preds, optimize, get_interactive_graph_data
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
    return render_template("index copy.html")

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
    # df_fill=fill_preds(fill_pre(df))

    # get opt log, a string (for now, some kind of dict later?)
    # opt_log = optimize(semesters, minHours, maxHours, df_fill)

    # check if returning error
    running = run(course_list, minHours, maxHours, summer=summer)
    print(running)
    # print(running)
    # print("--------------")
    # print(jsonify({"ERROR": "error"}))
    # print(jsonify("ERROR"))
    if running=="ERROR":
        result = {"opt_log": "ERROR"}
        return jsonify(result)
    
    opt_log, df_graph = run(course_list, minHours, maxHours, summer=summer)

    # df_graph.to_csv("df_graph.csv")
    
    # save opt log to a text file
    # with open("opt_log.txt", "w") as f:
    #     f.write(str(opt_log))

    # get gpas
    gpa_dict, semester_by_course, prereqs_by_course, prof_dict = get_interactive_graph_data(opt_log, df_graph )

    # opt_log = run(['ISYE 6501', 'ISYE 6414', 'CSE 6242', 'ISYE 6669', 'MGT 8803', 'CSE 6040'], 5, 12, summer=summer)
    # opt_log = [3.6551637842884044, 2, [[['ISYE 6414',3.499326780769436], ['MGT 8803', 3.8339323963212553], ['CSE 6040', 3.6196010600730615]], [['ISYE 6501', 3.6312633902786087], ['CSE 6242', 3.9702462718971048], ['ISYE 6669', 3.3766128063909586]]]]

    print("opt_log is: ")
    print(opt_log)



    # we can change this so that we can retrieve {sem1: {...}} or more creative 
    # formats to customize retrieval
    # return jsonify({"opt_log":opt_log})

    result = {
            "opt_log": opt_log,
            "gpas": gpa_dict,
            "semesters": semester_by_course,
            "prereqs": prereqs_by_course,
            "professors": prof_dict
        }
    
    return jsonify(result)

if __name__ == "__main__":
    app.run(port=8000,debug=True)