import csv
import os
import re
import codecs
import scholar
import random
import time
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')


current_path = os.getcwd() + "/output.csv"
# csv_columns = ['title', 'url', 'year', 'num_citations', 'num_versions', 'cluster_id', 'url_pdf', 'url_citations', 'url_versions', 'url_citation', 'excerpt']
csv_columns = ['title,url,year,num_citations,num_versions,cluster_id,url_pdf,url_citations,url_versions,url_citation,excerpt']
parse_file = "target.txt"


def decode(parse_file):
    with codecs.open(parse_file, 'r+', encoding='utf-8') as txt_file:
        txt = txt_file.readlines()
    return txt

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

def concate2(lines):
    str1 = ""
    L = []
    for line in lines:
        if line[-3] != ".":
            line = line.strip("\n")
            line = line.strip("\r")
            str1 += line
        else:
            str1 += " " + line
            str1 = str1.strip("\n")
            str1 = str1.strip("\r")
            L.append(str1)
            str1 = ''
    return L

def parseTxtFile(lines):
    parse_txt = []

    for line in lines:
        line = line.lstrip()
        if not (len(line) <= 5 or (line[0] != " " and line[1] == " ") or line[0] == "\n"):
            parse_txt.append(line)

    l = concate2(parse_txt)
    l[0] = l[0][10:]
    # print(l[0])

    return l

    # txt = open("parce_sample.txt", "w")
    # for a in l:
    #     txt.write(a)
    # txt.close()

    # citation = []
    # for line in l:
    #     strings = line.split('.')
    #     citation.append(dict([("name", strings[0]), ("date", int(strings[1][1:])), ("article", strings[2][2:])]))
    # return citation

def writeDictToCSV(csv_file, csv_columns, dict_data):
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = csv_columns)
        writer.writeheader()
        for data in dict_data:
            writer.writerow(data)
    return dict_data

def parseLeftAndRight(txt):
	left,right = [], []
	for line in txt:
		index = line.find('  ')
		if index == -1:
			left.append(line)
		else:
			left.append(line[:index])
			right.append(line[index:])
	return left, right


'''
left, right = parseLeftAndRight(decode(parse_file))
l = concate(left)

txt = open("parce_sample.txt", "w")
for a in l:
    txt.write(a[1:] + "\n")
txt.close()
'''

sample = decode(parse_file)
citation = parseTxtFile(sample)

# print(len(citation))
# dict_data = writeDictToCSV(current_path, csv_columns, citation)
# print(dict_data)

querier = scholar.ScholarQuerier()
settings = scholar.ScholarSettings()
query = scholar.SearchScholarQuery()
settings.set_citation_format(scholar.ScholarSettings.CITFORM_BIBTEX)
querier.apply_settings(settings)

citationFile = codecs.open('citation.bib', 'w','utf-8')

with open('output.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(csv_columns)
    for c in citation:
        time.sleep(random.random())
        # print(c)
        query.set_words(c)
        querier.send_query(query)
        print(scholar.citation_export(querier))
        citationFile.write(scholar.citation_export(querier).encode('utf-8'))
        citationFile.write('\n')
        # writer.writerow(scholar.csv(querier, header=False, sep=','))

print('finish writing to CSV file!')


