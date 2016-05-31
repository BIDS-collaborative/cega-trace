#!/usr/bin/python
from nltk.tag.stanford import StanfordNERTagger
import operator
import re

fileList = open("fileList.txt", "r")
fileName = fileList.readlines()
fileList.close()

outfile = open("country.txt", "w")

english_nertagger = StanfordNERTagger('/Users/stellamberv/Documents/stanford-ner-2014-08-27/classifiers/english.muc.7class.distsim.crf.ser.gz','/Users/stellamberv/Documents/stanford-ner-2014-08-27/stanford-ner.jar')

for i in range(len(fileName)): 
  oneFile = open(fileName[i].rstrip(), "r")
  oneFileContent = oneFile.read()
  oneFile.close()

  str_split = english_nertagger.tag(oneFileContent.split())
  
  j = 0
  country = ""
  while j < len(str_split):
    if str_split[j][1] == u'LOCATION':
      country = country + " " + (str_split[j][0]).encode("utf-8")
      j = j + 1
    else:
      j = j + 1
      if len(country) == 0:
        continue
      else:
        outfile.write(country + '\n')
        country = ""

outfile.close()




