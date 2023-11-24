import json

with open("data/unique classes.txt") as f:
    lines = f.readlines()

temp = [line[:-1] for line in lines]
print(temp[0])

out_file = open("data/classes.json", "w")
json.dump(temp, out_file)
out_file.close()