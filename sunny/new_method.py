import csv
import json
import os
import re
import codecs
import scholar
import random
import time
import sys  

#reload(sys)  
#sys.setdefaultencoding('utf8')


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

def scholarURLLookup(str):
    time.sleep(random.random())
    query.set_words(str)
    querier.send_url(query)
    return querier.articles

def articleToDict(article):
    # The triplets for each keyword correspond to (1) the actual
    # value, (2) a user-suitable label for the item, and (3) an
    # ordering index:
    articleDict = article.attrs
    for attr in articleDict:
        articleDict[attr] = articleDict[attr][0]
    articleDict["citation"] = article.as_citation()
    return articleDict


with open('proquest_journals.csv', encoding='utf-8', errors = "ignore") as csvfile:
    reader = csv.DictReader(csvfile)
    fulljson = []

    for row in reader:
        article = scholarLookup(str(row['Title']))
        current_dict = articleToDict(article)
        current_dict['abstract'] = str(row['Abstract'])
        current_dict['url'] = str(row['DocumentURL'])
        current_dict['subjects'] = str(row['subjectTerms'])
        current_dict['year'] = str(row['year'])

        if(current_dict["url_citations"]):
            citedby = []
            cites = scholarURLLookup(current_dict["url_citations"])
            for i in cites:
                citedby += [articleToDict(i)]
                print(i)
            current_dict['citedby'] = citedby
        
        fulljson += [current_dict]

        print(fulljson)

        
with open('output.txt', 'w') as outfile:
    json.dump(fulljson, outfile)