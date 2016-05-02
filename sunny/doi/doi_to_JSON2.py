# -*- coding: utf-8 -*-
# import requests
# import urllib

import re
import urllib
import urllib.request
import json
import sys
import codecs

def search_doi(s):
    url = "http://api.crossref.org/works/" + s
    with urllib.request.urlopen(url) as htmlfile:
        htmltext = htmlfile.read().decode('utf-8')
    curdata = json.loads(htmltext)
    print(htmltext)
    return curdata

def convert_string(s):
    s = str(s)
    replaced = re.sub(',', '%2C' , s)
    replaced = re.sub(';', '%3B', replaced)
    # replaced = re.sub('?', '%3F', replaced)
    replaced = re.sub(' ', '+', replaced)
    replaced = re.sub(':', '%3A' , replaced)
    replaced = re.sub('/', '%2F', replaced)
    replaced = re.sub('&', '%26' , replaced)
    replaced = re.sub(r'\(', '%28', replaced)
    replaced = re.sub(r'\)', '%29', replaced)   
    return replaced


def decode(parse_file):
    with codecs.open(parse_file, 'r+', encoding='utf-8', errors='ignore') as txt_file:
        txt = txt_file.readlines() 
    return txt

def main():

    master_dictionary = {}

    for i in range(8, 20):
        try:
            data_ref = []
            name = (str(i) + 'doi.txt')
            data = open(name, 'r')
            if data:
                my_list = data
                #out = (str(i) + 'data_ref.json')
                #outfile = open(out, 'w')
                for line in my_list:
                    print(line)
                    cur_data = search_doi(line)
                    data_ref.append(cur_data)

            master_dictionary[i] = data_ref

            data.close()

            with open("master_data_ref", "w") as outfile:
                outfile.write(str(master_dictionary))
            outfile.close()
            
        except IOError:
            pass
        except ValueError:
            pass
        


if __name__ == '__main__':
    main()
