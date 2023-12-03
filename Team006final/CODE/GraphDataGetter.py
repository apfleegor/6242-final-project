# A .PY OF DSHU'S FIRST OPT NOTEBOOK 
# INCLUDES NO MAIN METHOD, OPTIMIZE RETURNS A STRING

import pandas as pd
import random
import copy
import pulp as pp
pd.options.mode.chained_assignment = None

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

        length = opt_log[1] # number of semesters

        # get gpas
        df_gpa = df[["Course", "Pred_1", "Pred_2", "Pred_3", "Pred_4","Pred_5", "Pred_6","Pred_7", "Pred_8"]]
        gpa_list = []

        for index,row in df_gpa.iterrows():
            gpa_list.append(row.tolist())

        gpa_dict = {k[0]:[k[1:]] for k in gpa_list}
        gpa_dict = {k:[gpa_dict[k][0][:length]] for k in gpa_dict.keys()}

        # get professors
        df_prof = df[["Course", "Instructor_1", "Instructor_2", "Instructor_3", "Instructor_4","Instructor_5", "Instructor_6","Instructor_7", "Instructor_8"]]
        prof_list = []

        for index,row in df_prof.iterrows():
            prof_list.append(row.tolist())

        prof_dict = {k[0]:k[1:] for k in prof_list}
        prof_dict = {k:[prof_dict[k][:length]] for k in prof_dict.keys()}


        # get chosen semesters
        opt_log = opt_log[2]

        semester_by_course = {}
        for i in range(length):
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
