import re

par_file = "target.txt"

one_set = []
with open(par_file) as f:
    data = f.readlines()
for line in data:
    line = line.lstrip()
    if len(line) <= 5 or (line[0] != " " and line[1] == " ") or line[0] == "\n":
        continue
    one_set.append(line)

txt = open("after_parce.txt","w")
for line in one_set:
    txt.write(line)
txt.close()

def concate(lines):
    str1 = ""
    L=[]
    for line in lines:
        if line[-2] != ".":
            line = line.strip("\n")
            str1 = str1 + line
        else:
            str1=str1 + " " + line
            L.append(str1)
            str1=''
    return L

# with open("References.txt") as f:
#     data = f.readlines()
l = concate(one_set)
l[0] = l[0][13:]    #eliminate first "Reference"

txt = open("abc.txt","w")
for a in l:
    txt.write(a)
txt.close()
