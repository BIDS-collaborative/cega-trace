import csv
import os
import re


current_path = os.getcwd() + "/output.csv"
file_name = 'parce_sample.txt'
csv_columns = ['name', 'date', 'article']
par_file = "paragraph_parce.txt"


def parseTxtFile(file_name):
	citation = []
	with open(file_name, 'r') as txt_file:
		txt = txt_file.readlines()
	for line in txt:
		strings = line.split('.')
		citation.append(dict([("name", strings[0]), ("date", int(strings[1][1:])), ("article", strings[2][2:])]))
	return citation

def writeDictToCSV(csv_file, csv_columns, dict_data):
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = csv_columns)
        writer.writeheader()
        for data in dict_data:
            writer.writerow(data)
    return 

def parseLeftAndRight(par_file):
	left,right = [],[]
	with open(par_file) as f:
		data = f.readlines()
	for line in data:
		index = line.find('  ')
		if index == -1:
			left.append(line)
		else:
			left.append(line[:index])
			right.append(line[index:])
	return left, right

def concate(lines):
    str1 = ""
    L = []
    for line in lines:
        if line[-1] != ".":
            str1 = str1 + " " + line
        else:
            str1 = str1 + " " + line
            L.append(str1)
            str1 = ''
    return L


left, right = parseLeftAndRight(par_file)
l = concate(left)

txt = open("parce_sample.txt", "w")
for a in l:
    txt.write(a[1:] + "\n")
txt.close()

writeDictToCSV(current_path, csv_columns, parseTxtFile(file_name))

