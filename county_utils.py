import csv
import requests
from BeautifulSoup import BeautifulSoup

"""
The `parse_results` function scrapes county-level results from the
Nevada Secretary of State's website and outputs a CSV file with
county-level candidate totals.
"""

def parse_2012_primary():
    base_url = "http://www.nvsos.gov/SilverState2012Pri/Counties/"
    counties = ['Carson%20City.aspx', 'Churchill.aspx','Clark.aspx','Douglas.aspx','Elko.aspx',
    'Esmeralda.aspx','Eureka.aspx','Humboldt.aspx','Lander.aspx','Lincoln.aspx','Lyon.aspx',
    'Mineral.aspx','Nye.aspx','Pershing.aspx','Storey.aspx','Washoe.aspx','White%20Pine.aspx']
    for county in counties:
        r = requests.get(base_url+county)
        soup = BeautifulSoup(r.text)
        jurisdiction = soup.find('title').text.split(' Results')[0]
        if 'County' in jurisdiction:
            jurisdiction = jurisdiction.split(' County')[0]
        jurisdiction = jurisdiction.lower().replace(' ','_')
        filename = '2012/20120712__nv__primary__'+jurisdiction+'.csv'
        finish = len(soup.findAll('li'))-2
        candidates = []
        for i in xrange(8,finish,2):
            results = soup.findAll('li')[i]
            office = results.find('span').text
            for candidate in results.findAll('tr')[1:len(results.findAll('tr'))-1]:
                cands = [td.text.strip() for td in candidate.findAll('td')]
                cands.append(office)
                candidates.append(cands)
        with open(filename, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"')
            writer.writerow(['candidate','party','votes','percent','office'])
            [writer.writerow(row) for row in candidates]
