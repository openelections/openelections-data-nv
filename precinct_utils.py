import csv
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from BeautifulSoup import BeautifulSoup

"""
Scrapes precinct-level results from Nevada SOS site
and generates CSV file for a given jurisdiction.
"""

ELECTIONS = [
    {"year": "2012", "type": "primary", "id": "16", "datestring":"20120712"},
    {"year": "2012", "type": "general", "id": "17", "datestring":"20121106"},
    {"year": "2011", "type": "special__general", "id": "15", "datestring":"20110913"},
    {"year": "2010", "type": "primary", "id": "11", "datestring":"20100608"},
    {"year": "2010", "type": "general", "id": "12", "datestring":"20101102"},
    {"year": "2008", "type": "primary", "id": "7", "datestring":"20080812"},
    {"year": "2008", "type": "general", "id": "8", "datestring":"20081104"},
    {"year": "2006", "type": "primary", "id": "3", "datestring":"20060815"},
    {"year": "2006", "type": "general", "id": "4", "datestring":"20061107"},
    {"year": "2004", "type": "general", "id": "1", "datestring":"20041102"}
]

JURISDICTIONS = [
    {'name': "carson_city", "id": "4"},
    {'name': "churchill", "id": "5"},
    {'name': "clark", "id": "6"},
    {'name': "douglas", "id": "7"},
    {'name': "elko", "id": "8"},
    {'name': "esmeralda", "id": "9"},
    {'name': "eureka", "id": "10"},
    {'name': "humboldt", "id": "11"},
    {'name': "lander", "id": "12"},
    {'name': "lincoln", "id": "13"},
    {'name': "lyon", "id": "14"},
    {'name': "mineral", "id": "15"},
    {'name': "nye", "id": "16"},
    {'name': "pershing", "id": "17"},
    {'name': "storey", "id": "18"},
    {'name': "washoe", "id": "19"},
    {'name': "white_pine", "id": "20"}
]

def fetch_and_parse_all():
    driver = webdriver.Firefox()
    for election in ELECTIONS:
        for jurisdiction in JURISDICTIONS:
            filename = election['year']+'/'+election['datestring']+"__nv__"+election['type']+"__"+jurisdiction['name']+'__precinct.csv'
            driver.get('http://www.nvsos.gov/electionresults/PrecinctReport.aspx')
            setup_form(driver, election, jurisdiction, filename)

def fetch_and_parse_jurisdiction(jurisdiction):
    """
    For more populous jurisdictions like Clark and Washoe, it's
    necessary to go race-by-race to limit the overall pagination
    size (site errors out at 657 pages).
    """
    driver = webdriver.Firefox()
    for election in ELECTIONS:
        filename = election['year']+'/'+election['datestring']+"__nv__"+election['type']+"__"+jurisdiction['name']+'__precinct.csv'
        driver.get('http://www.nvsos.gov/electionresults/PrecinctReport.aspx')
        options = get_race_options(driver, election, jurisdiction)
        setup_race_form(options, driver, election, jurisdiction, filename)

def get_race_options(driver, election, jurisdiction):
        election_select = Select(driver.find_element_by_name('ddlElections'))
        election_select.select_by_value(election['id'])
        time.sleep(3)
        jurisdiction_select = Select(driver.find_element_by_name('ddlAgencies'))
        jurisdiction_select.select_by_value(jurisdiction['id'])
        time.sleep(3)
        race_select = Select(driver.find_element_by_name('ddlContests'))
        return [x.get_attribute('value') for x in race_select.options][1:]

def setup_race_form(options, driver, election, jurisdiction, filename):
    candidates = []
    for option in options:
        driver.get('http://www.nvsos.gov/electionresults/PrecinctReport.aspx')
        election_select = Select(driver.find_element_by_name('ddlElections'))
        election_select.select_by_value(election['id'])
        time.sleep(3)
        jurisdiction_select = Select(driver.find_element_by_name('ddlAgencies'))
        jurisdiction_select.select_by_value(jurisdiction['id'])
        time.sleep(3)
        race_select = Select(driver.find_element_by_name('ddlContests'))
        race_select.select_by_value(option)
        driver.find_element_by_name('btnElectionSearch').click()
        soup = BeautifulSoup(driver.page_source)
        try:
            postback_links, replacements = fetch_postback_links(soup)
        except:
            print jurisdiction['name'] + ' - ' + election['datestring']
            raise
        # parse first page
        for candidate in soup.findAll('tr', {'class':'TDColorC'}):
            cand = [td.text.replace('&nbsp;','').strip() for td in candidate.findAll('td')]
            candidates.append(cand)
        # do other pages
        for postback_link in postback_links:
            if postback_link in replacements:
                postback_link = '...'
            try:
                print postback_link
                if postback_link == '...':
                    if len(driver.find_elements_by_link_text(postback_link)) > 1:
                        driver.find_elements_by_link_text(postback_link)[1].click()
                    else:
                        driver.find_elements_by_link_text(postback_link)[0].click()
                else:
                    driver.find_element_by_link_text(postback_link).click()
                results = BeautifulSoup(driver.page_source)
                for candidate in results.findAll('tr', {'class':'TDColorC'}):
                    cand = [td.text.replace('&nbsp;','').strip() for td in candidate.findAll('td')]
                    candidates.append(cand)
            except:
                continue
    write_csv(filename, candidates)

def setup_form(driver, election, jurisdiction, filename):
    election_select = Select(driver.find_element_by_name('ddlElections'))
    election_select.select_by_value(election['id'])
    time.sleep(3)
    jurisdiction_select = Select(driver.find_element_by_name('ddlAgencies'))
    jurisdiction_select.select_by_value(jurisdiction['id'])
    driver.find_element_by_name('btnElectionSearch').click()
    soup = BeautifulSoup(driver.page_source)
    try:
        postback_links, replacements = fetch_postback_links(soup)
    except:
        print jurisdiction['name'] + ' - ' + election['datestring']
        raise
    candidates = []
    # parse first page
    for candidate in soup.findAll('tr', {'class':'TDColorC'}):
        cand = [td.text.replace('&nbsp;','').strip() for td in candidate.findAll('td')]
        candidates.append(cand)
    # do other pages
    for postback_link in postback_links:
        if postback_link in replacements:
            postback_link = '...'
        try:
            print postback_link
            if postback_link == '...':
                if len(driver.find_elements_by_link_text(postback_link)) > 1:
                    driver.find_elements_by_link_text(postback_link)[1].click()
                else:
                    driver.find_elements_by_link_text(postback_link)[0].click()
            else:
                driver.find_element_by_link_text(postback_link).click()
            results = BeautifulSoup(driver.page_source)
            for candidate in results.findAll('tr', {'class':'TDColorC'}):
                cand = [td.text.replace('&nbsp;','').strip() for td in candidate.findAll('td')]
                candidates.append(cand)
        except:
            continue
    write_csv(filename, candidates)

def fetch_postback_links(results):
    num = float(results.find('span', {'id':'lblMessage'}).text.split()[5])
    last_page = int((num/50.0)+2)
    pages = [str(x) for x in xrange(2,last_page)]
    replacements = [str(x) for x in xrange(26,last_page,25)]
    return [pages, replacements]

def write_csv(filename, candidates):
    with open(filename, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"')
        writer.writerow(['precinct','office','candidate','votes'])
        try:
            [writer.writerow(row) for row in candidates if not row[2] == '']
        except:
            next
