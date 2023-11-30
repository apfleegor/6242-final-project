# A .PY OF DSHU'S FIRST OPT NOTEBOOK 
# INCLUDES NO MAIN METHOD, OPTIMIZE RETURNS A STRING

import pandas as pd
import numpy as np
import random
import copy
import pulp as pp
import math
import sys
pd.options.mode.chained_assignment = None

#BOTH ARE FILLING FUNCTIONS SUPER SIMPLE RANDOM SHIT
def fill_pre(df):
    df1=copy.deepcopy(df)
    df1['Pre-req'] = df1['Pre-req'].fillna(0)
    for i in range(len(df1)):
        if df1['Pre-req'][i] == 0:
            current_course = df1['Course'][i]
            available_courses = list(df1['Course'])
            for ac in available_courses:
                if df1.loc[df1['Course'] == ac, 'Pre-req'].values[0]!=0:
                    if current_course in df1.loc[df1['Course'] == ac, 'Pre-req'].values[0]:
                        available_courses.remove(ac)
            df1['Pre-req'][i] = random.randint(0,8)
            if df1['Pre-req'][i] == 1 or df1['Pre-req'][i] == 6:
                df1['Pre-req'][i] = random.sample(available_courses,1)
            #elif df1['Pre-req'][i] == 2:
                #df1['Pre-req'][i] = random.sample(available_courses,2)
            #elif df1['Pre-req'][i] == 3:
                #df1['Pre-req'][i] = random.sample(available_courses,3)
            else:
                df1['Pre-req'][i] = ['']
    return df1

def fill_preds(df):
    df1=copy.deepcopy(df)
    for i in range(len(df1)):
        df1['Pred_1'][i] = random.uniform(2,4)
        df1['Pred_2'][i] = random.uniform(2,4)
        df1['Pred_3'][i] = random.uniform(2,4)
        df1['Pred_4'][i] = random.uniform(2,4)
        df1['Pred_5'][i] = random.uniform(2,4)
        df1['Pred_6'][i] = random.uniform(2,4)
        df1['Pred_7'][i] = random.uniform(2,4)
        df1['Pred_8'][i] = random.uniform(2,4)
    return df1

def optimize(semesters, min_hours, max_hours, df_fill):
    # this part creates the inputs needed from the user
    df_fill = df_fill
    semesters = semesters
    min_hours = min_hours
    max_hours = max_hours

    #These three are used in the opt funct
    df_preds = df_fill[["Course","Pred_1","Pred_2","Pred_3","Pred_4","Pred_5","Pred_6","Pred_7","Pred_8"]]
    df_preds = df_preds.set_index("Course")
    df_precs = df_fill[["Course","Pre-req"]]
    df_precs = df_precs.set_index("Course")
    df_hours = df_fill[["Course","Cred_hours"]]
    df_hours = df_hours.set_index("Course")

    # semesters = int(input("How many semesters do you want to take?")) #used 4 for testing
    # min_hours = int(input("What are minimum hours you want to take?")) #used 12 for testing
    # max_hours = int(input("What are maximum hours you want to take?")) #used 18 for testing
    # this part creates the model
    
    model = pp.LpProblem(name="Schedule", sense=pp.LpMaximize)
    # this part creates the variables cpecifically when a course is taken and if it is before another course
    when = pp.LpVariable.dicts("when", ((i,j) for i in range(semesters) for j in df_fill["Course"]), cat='Binary')
    # last variable that is the number of hours taken per semester
    hours = pp.LpVariable.dicts("hours", (i for i in range(semesters)), cat='Integer')
    # this part creates the objective function that summations the predicted gpa stuff. the other line after is something imma add later
    model += pp.lpSum(df_preds.loc[j].iloc[i]*when[(i,j)] for i in range(semesters) for j in df_fill["Course"])/len(df_fill["Course"]) 
    #- prop*pp.lpSum((hours[i]-math.mean(hours))**2 for i in range(semesters))
    
    # Constraints
    # the first one is mkaing sure that each course is only taken once
    for j in df_fill["Course"]:
        model += pp.lpSum(when[(i,j)] for i in range(semesters)) == 1
    # the next two are making sure that the hours are between the min and max
    for i in range(semesters):
        model += pp.lpSum(df_hours.loc[j]*when[(i,j)] for j in df_fill["Course"]) >= min_hours
    for i in range(semesters):
        model += pp.lpSum(df_hours.loc[j]*when[(i,j)] for j in df_fill["Course"]) <= max_hours
    # this one is making sure that the hours are equal to the hours variable
    for i in range(semesters):
        model += hours[i] == pp.lpSum(df_hours.loc[j]*when[(i,j)] for j in df_fill["Course"])
    # this one is making sure that the courses are taken in order
    for i in df_fill["Course"]:
        if df_precs["Pre-req"][i] != ['']:
            for j in df_precs["Pre-req"][i]:
                    model += pp.lpSum(when[(k,i)]*(k+1) for k in range(semesters)) >= pp.lpSum(when[(k,j)]*(k+1) for k in range(semesters)) + 1
    model.solve()
    #for var in model.variables():
    #    print(f"{var.name}: {var.value()}")


    # result string to return (for now)
    result = ""

    for i in range(semesters):
        # print(f"Semester {i+1}:")
        result += f"Semester {i+1}:\n"
        for j in df_fill["Course"]:
            if when[(i,j)].value() == 1:
                result += f"{j}: {df_preds.loc[j].iloc[i]} {df_hours.loc[j].iloc[0]}\n"
                # print(f"{j}: {df_preds.loc[j].iloc[i]} {df_hours.loc[j].iloc[0]}")
    # print(f"objective: {model.objective.value()}")
    result += f"objective: {model.objective.value()}"

    return result

# if __name__ == "main":
    #Currently randomly fills the table because we dont ahve forecasts. replaced later
# df = pd.read_csv('ISYE_SAMPLE.csv')
# df_fill=fill_preds(fill_pre(df))
# df_fill
# x = optimize(4, 10, 12, df_fill)
# print(x)



"""
# Use this function to get all the required data for the interactive graph

# Need to return the following
GPA_by_course= { course1: [gpa1, gpa2, gpa3, ...], course2: [gpa1, gpa2, gpa3, ...], ... }
Semester_by_course = { course1: semester, course2: semester, ... } - the semester chosen to take the course
Pre_reqs_by_course = { course1: [pre_req1, pre_req2, ...], course2: [pre_req1, pre_req2, ...], ... } -- prereqs for each course - may be empty
professors_by_course_by_semester = { course1: { semester1: professor, semester2: professor, ... }, course2: { semester1: professor, semester2: professor, ... }, ... }
"""

 
def get_interactive_graph_data(opt_log, df):

    # check if opt_log is a float
    if isinstance(opt_log, float):
        print("opt_log is a float - returning None")
        return None, None, None, None

    else:
        # get gpas
        df_gpa = df[["Course", "Pred_1", "Pred_2", "Pred_3", "Pred_4","Pred_5", "Pred_6","Pred_7", "Pred_8"]]
        gpa_list = []

        for index,row in df_gpa.iterrows():
            gpa_list.append(row.tolist())

        gpa_dict = {k[0]:[k[1:]] for k in gpa_list}

        # get professors
        df_prof = df[["Course", "Instructor_1", "Instructor_2", "Instructor_3", "Instructor_4","Instructor_5", "Instructor_6","Instructor_7", "Instructor_8"]]
        prof_list = []

        for index,row in df_prof.iterrows():
            prof_list.append(row.tolist())

        prof_dict = {k[0]:k[1:] for k in prof_list}

        # get chosen semesters
        opt_log = opt_log[2]

        semester_by_course = {}
        for i in range(len(opt_log)):
            for j in range(len(opt_log[i])):
                semester_by_course[opt_log[i][j][0]] = i+1

        # get prereqs
        df['Pre-req'] = df['Pre-req'].astype(str)

        df_prereqs = df[["Course", "Pre-req"]]
        

        pre_reqs_list =[]
        for index,row in df_prereqs.iterrows():
            pre_reqs_list.append(row.tolist())

        prereqs_by_course = {k[0]:k[1].strip("[]").replace("'", "").split(",") if k[1] != "['']" else [] for k in pre_reqs_list}


        return gpa_dict, semester_by_course, prereqs_by_course, prof_dict
