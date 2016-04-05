import csv
import json
import os
import re
import codecs
import scholar
import random
import time
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')


try:
    from urllib.parse import quote, unquote
    from http.cookiejar import MozillaCookieJar
except ImportError:
    from urllib import quote, unquote
    from cookielib import MozillaCookieJar




querier = scholar.ScholarQuerier()
settings = scholar.ScholarSettings()
query = scholar.SearchScholarQuery()
settings.set_citation_format(scholar.ScholarSettings.CITFORM_BIBTEX)
querier.apply_settings(settings)

def scholarLookup(str):
    time.sleep(random.random())
    query.set_words(str)
    querier.send_query(query)
    return querier.articles[0]

def articleToDict(article):
    # The triplets for each keyword correspond to (1) the actual
    # value, (2) a user-suitable label for the item, and (3) an
    # ordering index:
    articleDict = artcle.attrs
    for attr in articleDict:
        articleDict[attr] = articleDict[attr][0]
    articleDict["citation"] = article.as_citation()
    return articleToDict

def decode(parse_file):
    with codecs.open(parse_file, 'r+', encoding='utf-8') as txt_file:
        txt = txt_file.readlines()
    return txt

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



with open('sources.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    fulljson = []

    for row in reader:
        try:
            article = scholarLookup(str(row['citation']))
            current_dict = articleToDict(article)
            current_dict['id'] = str(row['id'])
            cited_lst = parseTxtFile(decode(parse_file))
            citations = [articleToDict(scholarLookup(i)) for i in cited_lst]
            current_dict['citations'] = citations

            fulljson += [current_dict]

        except Exception, e:
            print("Could not find article")

with open('output.txt', 'w') as outfile:
    json.dump(data, outfile)