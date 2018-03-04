import pandas as pd
import requests
import csv
from bs4 import BeautifulSoup
from us import states

def get_children(node):
    children = list(node.children)
    children = list(filter(lambda x: x != '\n', children))
    return children

def remove_commas(num_str):
    return num_str.replace(',', '')

def scrape (state_fips):
    url = 'http://www.censusscope.org/us/s' + str(state_fips) + '/print_rank_dissimilarity_white_black.html'
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')

    top = soup.find('table')
    rows = top('tr', {'class': 'datarow'})

    output = list(map(lambda row: list(map(lambda x: remove_commas(x.text), row.findChildren()[1:])), rows))

    return output[1:-1]

abbr_table = states.mapping('fips', 'abbr')
for i in range(56):
    nice_str = str(i + 1)
    if len(nice_str) == 1:
        nice_str = '0' + nice_str
    if nice_str not in abbr_table:
        continue
    abbr = abbr_table[nice_str]
    results = scrape(i + 1)
    results = map(lambda row: row + [abbr], results)

    with open('../res/' + abbr + '_DI.csv','w+') as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=',')
        csvWriter.writerow(['CITY', 'B_POP', 'W_POP', 'TOTAL_POP', 'BW_DI', 'STATE'])
        csvWriter.writerows(results)
