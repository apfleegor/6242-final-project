import json
import pandas as pd

with open("data/unique classes.txt") as f:
    lines = f.readlines()

temp = [line[:-1] for line in lines]
print(temp[0])

out_file = open("static/classes.json", "w")
json.dump(temp, out_file)
out_file.close()

# df = pd.read_csv("data/all_predictions_with_nonans_edited_by_goatshu.csv")
# print(len(df.index))
# df2 = pd.read_csv("data/all_predictions_with_nans.csv")
# print(len(df2.index))
# print(df.head())

# courses = list(df["Course"])

# out_file = open("static/classes.json", "w")
# json.dump(courses, out_file)
# out_file.close()
