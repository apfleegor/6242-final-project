import pandas as pd
import numpy as np
import random
import copy
import pulp as pp
import math
#list off all courses is the courses that the user wants to take, min and max hours are the inut params, summer is 0 if no summer and 1 if summer, and df is the overall df. I used my edited one casue its slightly better than feyzi's but anythign is up to u.
#also added a pr term that if you want to input pre req you can. It would have to be in the format of list of lists::
#where its in the same order as the list of courses and each list is the prereqs for that course
#ex: [[""],["MATH 1554"],[""],[""]]  with list of courses being ["MATH 1554","CS 1331","CS 1332","CS 2050"]
# woudl mean that math is pre req to cs 1331 and the rest have no prereqs
#every time you run the function it creates its own prereqs so if you want to keep the same prereqs you have to input them
def run( list_of_courses, min_hours, max_hours, summer=0, pr=None, df=pd.read_csv('data/all_predictions_with_nonans_edited_by_goatshu.csv')):
    print(list_of_courses)
    pd.options.mode.chained_assignment = None
    df = df[df['Course'].isin(list_of_courses)]
    df = df.reset_index(drop=True)
    # this part creates the inputs needed from the user
    #min_hours = int(input("What are minimum hours you want to take?")) #used 12 for testing
    #max_hours = int(input("What are maximum hours you want to take?")) #used 18 for testing
    min_sem=math.ceil(sum(df['Cred_hours'])/max_hours)
    max_sem=math.ceil(sum(df['Cred_hours'])/min_hours)
    breaker=0
    while True:
        #fill the df with prereqs
        if pr==None:
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
                    df1['Pre-req'][i] = random.randint(0,16)
                    if df1['Pre-req'][i] == 1 or df1['Pre-req'][i] == 6 or df1['Pre-req'][i] == 7 or df1['Pre-req'][i] == 8:
                        df1['Pre-req'][i] = random.sample(available_courses,1)
                    elif df1['Pre-req'][i] == 2:
                        df1['Pre-req'][i] = random.sample(available_courses,2)
                    elif df1['Pre-req'][i] == 3:
                        df1['Pre-req'][i] = random.sample(available_courses,3)
                    else:
                        df1['Pre-req'][i] = ['']
        else:
            df1=copy.deepcopy(df)
            df1['Pre-req'] = pr
        df_fill=df1
        df_preds = df_fill[["Course","Pred_1","Pred_2","Pred_3","Pred_4","Pred_5","Pred_6","Pred_7","Pred_8"]]
        df_preds = df_preds.set_index("Course")
        df_precs = df_fill[["Course","Pre-req"]]
        df_precs = df_precs.set_index("Course")
        df_hours = df_fill[["Course","Cred_hours"]]
        df_hours = df_hours.set_index("Course")
        for semesters in range(min_sem,max_sem+1):
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
            if model.status == pp.LpStatusOptimal and summer==0:
                output=[[] for _ in range(3)]
                empty_lists = [[] for _ in range(semesters)]
                for i in range(semesters):                            
                    if i%2==0:
                        print(f"Fall Semester {math.floor(i/2)+1}:")
                    else:
                        print(f"Spring Semester {math.floor(i/2)+1}:")
                    for j in df_fill["Course"]:
                        if when[(i,j)].value() == 1:
                            print(f"{j}: {df_preds.loc[j].iloc[i]} {df_hours.loc[j].iloc[0]} ")
                            empty_lists[i].append((j,df_preds.loc[j].iloc[i]))
                output[0]=model.objective.value()
                output[1]=semesters
                output[2]=empty_lists
                print(f"objective: {model.objective.value()}")
                print(f"Number of Semesters:{semesters}")
                print(df_precs)
                print(empty_lists)
                breaker=10000
                return output
                break
            elif model.status == pp.LpStatusOptimal and summer==1:
                output=[[] for _ in range(3)]
                empty_lists = [[] for _ in range(semesters)]
                for i in range(semesters):
                    if i%3==0:
                        print(f"Fall Semester {math.floor(i/3)+1}:")
                    elif i%3==1:
                        print(f"Spring Semester {math.floor(i/3)+1}:")
                    else:
                        print(f"Summer Semester {math.floor(i/3)+1}:")
                    for j in df_fill["Course"]:
                        if when[(i,j)].value() == 1:
                            print(f"{j}: {df_preds.loc[j].iloc[i]} {df_hours.loc[j].iloc[0]} ")
                            empty_lists[i].append((j,df_preds.loc[j].iloc[i]))
                output[0]=model.objective.value()
                output[1]=semesters
                output[2]=empty_lists
                print(f"objective: {model.objective.value()}")
                print(f"Number of Semesters:{semesters}")
                print(df_precs)
                print(empty_lists)
                breaker=10000
                return output
                break
        breaker+=1
        if breaker==10001:
            break
        elif breaker>=100:
            print(breaker)
            print("This configuration is not possible please change parameters")
            break
