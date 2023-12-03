from flask import Flask, render_template, jsonify, request
# from optimize import get_interactive_graph_data
from optimize_final import run, get_interactive_graph_data
import pandas as pd
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

    # put data into variables
    summer = int(data.get('summer'))
    minHours = int(data.get('minHours'))
    maxHours = int(data.get('maxHours'))
    course_list = data.get('course_list')
    prereqs = data.get('prereqs')

    # DO WE NEED THIS ANYMORE?
    df = pd.read_csv('data/ISYE_SAMPLE.csv')
    
    # check if returning error
    running = run(course_list, minHours, maxHours, summer=summer, pr=prereqs)
    
    if running=="ERROR":
        result = {"opt_log": "ERROR"}
        return jsonify(result)
    
    # if not returning error, then save the results
    opt_log, df_graph = run(course_list, minHours, maxHours, summer=summer, pr=prereqs)

    # get gpas
    gpa_dict, semester_by_course, prereqs_by_course, prof_dict = get_interactive_graph_data(opt_log, df_graph )

    # print opt_log
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