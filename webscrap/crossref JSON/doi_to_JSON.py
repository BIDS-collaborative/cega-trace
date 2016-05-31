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

def decode(parse_file):
    with codecs.open(parse_file, 'r+', encoding='utf-8', errors='ignore') as txt_file:
        txt = txt_file.readlines() 
    return txt

def main():
    data_ref = []
    # get bibliometric for all the references using DOI search by crossref.
    for i in range(0, 568):
        try:
            name = (str(i) + 'doi.txt')
            data = open(name, 'r')
            if data:
                my_list = data
                for line in my_list:
                    print('reading:' + str(i) + 'doi.txt')
                    cur_data = search_doi(line)
                    cur_data["ID"] = str(i)
                    data_ref.append(cur_data)
            data.close()
            # Every time finish searching. overwrite the previous JSON file.
            with open("master_data_ref.json", "w") as outfile:
                json.dump(data_ref, outfile)
            print(str(i) + 'finish searching '+'doi.txt')
        except IOError:
            pass
        except ValueError:
            pass

if __name__ == '__main__':
    main()
