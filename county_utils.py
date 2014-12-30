import csv
import requests
from BeautifulSoup import BeautifulSoup

"""
The functions here scrape county-level results from the
Nevada Secretary of State's website and output CSV files with
county-level candidate totals.
"""
# 2012 general county-level results
# http://www.nvsos.gov/silverstate2012gen/_xml/USandNV.xml

def parse_2004_primary():
    base_url = "http://nvsos.gov/SOSelectionPages/results/2004Primary/"
    counties = ['CarsonCity.aspx', 'Churchill.aspx','Clark.aspx','Douglas.aspx','Elko.aspx',
    'Esmeralda.aspx','Eureka.aspx','Humboldt.aspx','Lander.aspx','Lincoln.aspx','Lyon.aspx',
    'Mineral.aspx','Nye.aspx','Pershing.aspx','Storey.aspx','Washoe.aspx','WhitePine.aspx']
    for county in counties:
        soup, jurisdiction, filename = fetch_and_parse_2006(base_url+county, '2004', '20040907__nv__primary__')
        offices = [x.find('b').text for x in soup.findAll('th') if x.find('b')]
        max_offices = len(offices)-1
        candidates = []
        for i in range(1,max_offices):
            office = offices[i-1]
            results = soup.findAll('table')[11+i]
            for candidate in results.findAll('tr')[1:]:
                cand = [td.text.replace('&nbsp;','').strip() for td in candidate.findAll('td')]
                cand.append(office)
                candidates.append(cand)
            with open(filename, 'wb') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quotechar='"')
                writer.writerow(['candidate','party','percent','votes','office'])
                try:
                    [writer.writerow(row) for row in candidates if not row[2] == '']
                except:
                    next

def parse_2004_general():
    base_url = "http://nvsos.gov/SOSelectionPages/results/2004General/"
    counties = ['CarsonCity.aspx', 'Churchill.aspx','Clark.aspx','Douglas.aspx','Elko.aspx',
    'Esmeralda.aspx','Eureka.aspx','Humboldt.aspx','Lander.aspx','Lincoln.aspx','Lyon.aspx',
    'Mineral.aspx','Nye.aspx','Pershing.aspx','Storey.aspx','Washoe.aspx','WhitePine.aspx']
    for county in counties:
        soup, jurisdiction, filename = fetch_and_parse_2006(base_url+county, '2004', '20041102__nv__general__')
        offices = [x.find('b').text for x in soup.findAll('th') if x.find('b')]
        max_offices = len(offices)-1
        candidates = []
        for i in range(1,max_offices):
            office = offices[i-1]
            results = soup.findAll('table')[11+i]
            for candidate in results.findAll('tr')[1:]:
                cand = [td.text.replace('&nbsp;','').strip() for td in candidate.findAll('td')]
                cand.append(office)
                candidates.append(cand)
            with open(filename, 'wb') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quotechar='"')
                writer.writerow(['candidate','party','percent','votes','office'])
                try:
                    [writer.writerow(row) for row in candidates if not row[2] == '']
                except:
                    next


def parse_2006_primary():
    base_url = "http://nvsos.gov/SOSelectionPages/results/2006StateWidePrimary/"
    counties = ['CarsonCity.aspx', 'Churchill.aspx','Clark.aspx','Douglas.aspx','Elko.aspx',
    'Esmeralda.aspx','Eureka.aspx','Humboldt.aspx','Lander.aspx','Lincoln.aspx','Lyon.aspx',
    'Mineral.aspx','Nye.aspx','Pershing.aspx','Storey.aspx','Washoe.aspx','WhitePine.aspx']
    for county in counties:
        soup, jurisdiction, filename = fetch_and_parse_2006(base_url+county, '2006', '20060815__nv__primary__')
        labels = [x['id'] for x in soup.findAll('span') if x.text != '']
        max_label = int(labels[len(labels)-1].split('_')[1].split('ctl')[1])
        candidates = []
        for i in range(1, max_label):
            race_title = '_ctl'+str(i)+'_lblRaceTitle'
            try:
                office = soup.find('span', {'id': race_title}).text
            except:
                next
            results = soup.findAll('table')[11+i]
            for candidate in results.findAll('tr')[1:]:
                cand = [td.text.replace('&nbsp;','') for td in candidate.findAll('td')]
                cand.append(office)
                candidates.append(cand)
            with open(filename, 'wb') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quotechar='"')
                writer.writerow(['candidate','party','percent','votes','office'])
                try:
                    [writer.writerow(row) for row in candidates if not row[2] == '']
                except:
                    next

def parse_2006_general():
    base_url = "http://nvsos.gov/SOSelectionPages/results/2006StateWideGeneral/"
    counties = ['CarsonCity.aspx', 'Churchill.aspx','Clark.aspx','Douglas.aspx','Elko.aspx',
    'Esmeralda.aspx','Eureka.aspx','Humboldt.aspx','Lander.aspx','Lincoln.aspx','Lyon.aspx',
    'Mineral.aspx','Nye.aspx','Pershing.aspx','Storey.aspx','Washoe.aspx','WhitePine.aspx']
    for county in counties:
        soup, jurisdiction, filename = fetch_and_parse_2006(base_url+county, '2006', '20061107__nv__general__')
        labels = [x['id'] for x in soup.findAll('span') if x.text != '']
        max_label = int(labels[len(labels)-1].split('_')[1].split('ctl')[1])
        candidates = []
        for i in range(1, max_label):
            race_title = '_ctl'+str(i)+'_lblRaceTitle'
            try:
                office = soup.find('span', {'id': race_title}).text
            except:
                next
            results = soup.findAll('table')[11+i]
            for candidate in results.findAll('tr')[1:]:
                cand = [td.text.replace('&nbsp;','') for td in candidate.findAll('td')]
                cand.append(office)
                candidates.append(cand)
            with open(filename, 'wb') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quotechar='"')
                writer.writerow(['candidate','party','percent','votes','office'])
                try:
                    [writer.writerow(row) for row in candidates if not row[2] == '']
                except:
                    next

def parse_2008_primary():
    base_url = "http://nvsos.gov/SOSelectionPages/results/2008StateWidePrimary/"
    counties = ['CarsonCity.aspx', 'Churchill.aspx','Clark.aspx','Douglas.aspx','Elko.aspx',
    'Esmeralda.aspx','Eureka.aspx','Humboldt.aspx','Lander.aspx','Lincoln.aspx','Lyon.aspx',
    'Mineral.aspx','Nye.aspx','Pershing.aspx','Storey.aspx','Washoe.aspx','WhitePine.aspx']
    for county in counties:
        soup, jurisdiction, filename = fetch_and_parse_2008(base_url+county, '2008', '20080812__nv__primary__')
        labels = [x['id'] for x in soup.findAll('span') if x.text != '']
        max_label = int(labels[len(labels)-1].split('_')[1].split('ctl')[1])
        candidates = []
        for i in range(1, max_label):
            race_title = '_ctl'+str(i)+'_lblRaceTitle'
            try:
                office = soup.find('span', {'id': race_title}).text
            except:
                next
            results = soup.findAll('table')[11+i]
            for candidate in results.findAll('tr')[1:]:
                cand = [td.text.replace('&nbsp;','') for td in candidate.findAll('td')]
                cand.append(office)
                candidates.append(cand)
            with open(filename, 'wb') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quotechar='"')
                writer.writerow(['candidate','party','percent','votes','office'])
                try:
                    [writer.writerow(row) for row in candidates if not row[2] == '']
                except:
                    next


def parse_2008_general():
    base_url = "http://www.nvsos.gov/SilverState2008Gen/Counties/"
    counties = ['Carson%20City.aspx', 'Churchill.aspx','Clark.aspx','Douglas.aspx','Elko.aspx',
    'Esmeralda.aspx','Eureka.aspx','Humboldt.aspx','Lander.aspx','Lincoln.aspx','Lyon.aspx',
    'Mineral.aspx','Nye.aspx','Pershing.aspx','Storey.aspx','Washoe.aspx','White%20Pine.aspx']
    for county in counties:
        soup, jurisdiction, filename = fetch_and_parse(base_url+county, '2008', '20081104__nv__general__')
        finish = len(soup.findAll('li'))-2
        candidates = []
        for i in xrange(8,finish,2):
            results = soup.findAll('li')[i]
            office = results.find('span').text
            if 'QUESTION' in office:
                next
            for candidate in results.findAll('tr')[1:len(results.findAll('tr'))-1]:
                cands = [td.text.strip() for td in candidate.findAll('td')]
                cands.append(office)
                candidates.append(cands)
        with open(filename, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"')
            writer.writerow(['candidate','party','votes','percent','office'])
            try:
                [writer.writerow(row) for row in candidates if not row[2] == '']
            except:
                next

def parse_2010_primary():
    base_url = "http://www.nvsos.gov/SilverState2010Pri/Counties/"
    counties = ['Carson%20City.aspx', 'Churchill.aspx','Clark.aspx','Douglas.aspx','Elko.aspx',
    'Esmeralda.aspx','Eureka.aspx','Humboldt.aspx','Lander.aspx','Lincoln.aspx','Lyon.aspx',
    'Mineral.aspx','Nye.aspx','Pershing.aspx','Storey.aspx','Washoe.aspx','White%20Pine.aspx']
    for county in counties:
        soup, jurisdiction, filename = fetch_and_parse(base_url+county, '2010', '20100608__nv__primary__')
        finish = len(soup.findAll('li'))-2
        candidates = []
        for i in xrange(8,finish,2):
            results = soup.findAll('li')[i]
            office = results.find('a', {'class' : 'fakelink'})['onclick'].split('(', 1)[1].replace("'","").replace("))",")")
            for candidate in results.findAll('tr')[1:len(results.findAll('tr'))-1]:
                cands = [td.text.strip() for td in candidate.findAll('td')]
                cands.append(office)
                candidates.append(cands)
        with open(filename, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"')
            writer.writerow(['candidate','party','votes','percent','office'])
            try:
                [writer.writerow(row) for row in candidates if not row[2] == '']
            except:
                next

def parse_2010_general():
    base_url = "http://www.nvsos.gov/SilverState2010Gen/Counties/"
    counties = ['Carson%20City.aspx', 'Churchill.aspx','Clark.aspx','Douglas.aspx','Elko.aspx',
    'Esmeralda.aspx','Eureka.aspx','Humboldt.aspx','Lander.aspx','Lincoln.aspx','Lyon.aspx',
    'Mineral.aspx','Nye.aspx','Pershing.aspx','Storey.aspx','Washoe.aspx','White%20Pine.aspx']
    for county in counties:
        soup, jurisdiction, filename = fetch_and_parse(base_url+county, '2010', '20101102__nv__general__')
        finish = len(soup.findAll('li'))-2
        candidates = []
        for i in xrange(8,finish,2):
            results = soup.findAll('li')[i]
            office = results.find('span').text
            if 'STATE QUESTION' in office:
                next
            for candidate in results.findAll('tr')[1:len(results.findAll('tr'))-1]:
                cands = [td.text.strip() for td in candidate.findAll('td')]
                cands.append(office)
                candidates.append(cands)
        with open(filename, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"')
            writer.writerow(['candidate','party','votes','percent','office'])
            try:
                [writer.writerow(row) for row in candidates if not row[2] == '']
            except:
                next

def parse_2011_special():
    base_url = "http://www.nvsos.gov/SilverState2011Special/Counties/"
    counties = ['Carson%20City.aspx', 'Churchill.aspx','Clark.aspx','Douglas.aspx','Elko.aspx',
    'Esmeralda.aspx','Eureka.aspx','Humboldt.aspx','Lander.aspx','Lincoln.aspx','Lyon.aspx',
    'Mineral.aspx','Nye.aspx','Pershing.aspx','Storey.aspx','Washoe.aspx','White%20Pine.aspx']
    office = "U.S REPRESENTATIVE IN CONGRESS, DISTRICT 2"
    for county in counties:
        candidates = []
        soup, jurisdiction, filename = fetch_and_parse(base_url+county, '2011', '20110913__nv__special__general__')
        results = soup.find('table', {'class' : 'tableshadow'})
        for candidate in results.findAll('tr')[1:]:
            cands = [td.text.strip() for td in candidate.findAll('td')]
            cands.append(office)
            candidates.append(cands)
        with open(filename, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"')
            writer.writerow(['candidate','party','votes','percent','office'])
            [writer.writerow(row) for row in candidates]


def parse_2012_primary():
    base_url = "http://www.nvsos.gov/SilverState2012Pri/Counties/"
    counties = ['Carson%20City.aspx', 'Churchill.aspx','Clark.aspx','Douglas.aspx','Elko.aspx',
    'Esmeralda.aspx','Eureka.aspx','Humboldt.aspx','Lander.aspx','Lincoln.aspx','Lyon.aspx',
    'Mineral.aspx','Nye.aspx','Pershing.aspx','Storey.aspx','Washoe.aspx','White%20Pine.aspx']
    for county in counties:
        soup, jurisdiction, filename = fetch_and_parse(base_url+county, '2012', '20120712__nv__primary__')
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

def fetch_and_parse(url, year, name):
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    jurisdiction = soup.find('title').text.split(' Results')[0]
    if 'County' in jurisdiction:
        jurisdiction = jurisdiction.split(' County')[0]
    jurisdiction = jurisdiction.lower().replace(' ','_')
    filename = year+'/'+name+jurisdiction+'.csv'
    return [soup, jurisdiction, filename]


def fetch_and_parse_2008(url, year, name):
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    jurisdiction = soup.find('span', {'id': 'lblAgencyName'}).text.lower().replace(' ','_')
    filename = year+'/'+name+jurisdiction+'.csv'
    return [soup, jurisdiction, filename]


def fetch_and_parse_2006(url, year, name):
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    jurisdiction = soup.find('h2').text.split('Results')[1].lower().replace(' ','_').strip()
    filename = year+'/'+name+jurisdiction+'.csv'
    if '__.csv' in filename:
        jurisdiction = 'pershing'
        filename = '2006/20061107__nv__general__pershing.csv'
    return [soup, jurisdiction, filename]
