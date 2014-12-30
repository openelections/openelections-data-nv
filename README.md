OpenElections Data NV
=====================

Converted CSVs of Nevada election results. For primary and general elections from 2000 through 2012 primary, county-level results are scraped from [pages on the Nevada Secretary of State site](http://nvsos.gov/index.aspx?page=93). Beginning with the 2012 general election, the state provides XML files of county-level results:

* [2014 general county-level results](http://www.silverstateelection.com/_xml/USandNV.xml)
* [2014 primary county-level results](http://www.nvsos.gov/silverstate2014pri/_xml/USandNV.xml)
* [2012 general county-level results](http://www.nvsos.gov/silverstate2012gen/_xml/USandNV.xml)

Precinct-level results are available for 2004-2012 via [a separate form on the SOS site](http://www.nvsos.gov/electionresults/PrecinctReport.aspx).

The `county_utils.py` file contains functions for fetching and parsing HTML into CSV files, which are places in year-specific directories using the OpenElections file-naming conventions.
