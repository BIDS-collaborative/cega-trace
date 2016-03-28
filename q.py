# -*- coding: utf-8 -*-
# import requests
# import urllib

import re
import urllib
import json
import sys

def search_doi(s):
	url = "http://search.crossref.org/?q=" + convert_string(s)
	htmlfile = urllib.urlopen(url)
	htmltext = htmlfile.read()
	regex ="href='http://dx.doi.org/"+ '(.*)' + "'>"
	pattern = re.compile(regex)
	match = re.search(pattern, htmltext)
	if match:
		doi = match.group(1)
	else:
		print('did not found')
		return None
	print(doi)
	return doi

def convert_string(s):
	replaced = re.sub(',', '%2C' , s)
	replaced = re.sub(';', '%3B', replaced)
	replaced = re.sub(' ', '+', replaced)
	replaced = re.sub(':', '%3A' , replaced)
	replaced = re.sub('/', '%2F', replaced)
	replaced = re.sub('&', '%26' , replaced)
	replaced = re.sub(r'\(', '%28', replaced)
	replaced = re.sub(r'\)', '%29', replaced)	
	return replaced

# s = 'Benjamin, D., & Brandt, L.2002.Property rights, labour markets, and efficiency in a transition economy: the case of rural China.Canadian Journal of Economics, 35(4), 689-716.'
# search_doi(s)


# def check_matching(doi_citation, doi_title):
# 	if doi_citation == doi_title:
# 		return doi_title
# 	else:
# 		url_citation = "http://api.crossref.org/works/" + doi_citation
# 		url_title = "http://api.crossref.org/works/" + doi_title
# 		htmlfile_citation = urllib.urlopen(url_citation)
# 		htmlfile_title = urllib.urlopen(url_citation)
# 		htmltext_citation = htmlfile_citation.read()
# 		htmltext_titel = htmlfile_title.read()
# 		regex = '"title":["'+ '(.*)' + '."]'
def check_matching(doi_citation, citation):
	url_citation = "http://api.crossref.org/works/" + doi_citation
	htmlfile_citation = urllib.urlopen(url_citation)
	htmltext_citation = htmlfile_citation.read()
	regex = '"title":["'+ '(.*)' + '."]'
	pattern = rre.compile(regex)
	match = re.search(pattern, htmltext_citation)
	if match:
		title = match.group(1)
	else:
		print('wrong.....')
		return False
	if title in citation:
		return True
	return False
	

def main(argv):
	infile = open(sys.argv[1], 'r')
	print(infile)
	data = infile.read()
	my_list = data.splitlines()
	print(my_list)
	outfile = open(sys.argv[2], 'w')
	for line in my_list:
		print(line)
		doi = search_doi(line)
		outfile.write(doi+"\n")
	outfile.close()
	infile.close()


main(sys.argv[1:])
