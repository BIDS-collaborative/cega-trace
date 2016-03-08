import os
import sys
import time
import json
import urllib.request
from bs4 import BeautifulSoup
import re



def get_last_statements(url):
    r = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(r)

    result = str(soup.find(text = re.compile('Offender:')).findNext('p').findNext('p').findNext('p').get_text().encode('utf-8'))
    return result


def parse_rows(rows):
    heads = []
    results = []
    a = 0
    rows = rows[1:]
    for row in rows:
        table_data = row.find_all('td')
        current_row = []            
        for data in table_data:
            if(data.get_text() == "Last Statement"):
                try:
                    current_row.append(get_last_statements('https://www.tdcj.state.tx.us/death_row/' + data.find_all('a', href=True)[0]['href']))
                except:
                    current_row.append('This offender declined to make a last statement.')
                    print("OOPS!")
            elif(data.get_text() == "Offender Information"):
                pass
            else:
                current_row.append(data.get_text())
            
            #current_row.append(data.get_text())

        results.append(current_row)

        print(str(a) +' of ' + str(len(rows)))
        a+=1

    return heads,results

def createJSON(values):
    keys = ['Exectution', 'Last Statement', 'Last Name', 'First Name', 'TDCJ Number', "Age", 'Date', 'Race', 'County']
    return [dict(zip(keys, i)) for i in values]


r = urllib.request.urlopen('https://www.tdcj.state.tx.us/death_row/dr_executed_offenders.html').read()
soup = BeautifulSoup(r)

table = soup.find('table')

rows = table.find_all('tr')

table_heads, table_data = parse_rows(rows)

myJSON = createJSON(table_data)

print(table_data)
print(myJSON)

with open('data.txt', 'w') as outfile:
    json.dump(myJSON, outfile)







