from __future__ import division, print_function
""" Parse Nevada election results into OpenElection format
    available here:
    http://nvsos.gov/sos/elections/election-information/precinct-level-results
"""
import pandas as pd

from nameparser import HumanName

positions = ['President', 'U.S. Senate', 'U.S. House',
            'State Senate','State House', 'Governor']

header_map = {'jurisdiction':'county', 'precinct':'precinct',
            'contest':'office', 'district':'district', 'party':'party',
            'selection':'candidate', 'votes':'votes'}


def parser(file, **kwargs):
    """ Generic parser for NV election results
    """

    # read in the file
    df = pd.read_csv(file, **kwargs)

    # assign headers in lowercase
    df.columns = [x.lower() for x in df.columns]

    # extract district information from the contest column
    df['district'] = df['contest'].str.extract('(\d{1,3})', expand=True)
    df['precinct'] = df['precinct'].str.extract('(\d{1,3})', expand=False)
    df.contest.unique()

    # clean up office descriptions
    df.loc[df['contest'].str.contains(
        'PRESIDENT AND VICE', case=False), 'contest'] = 'President'
    df.loc[df['contest'].str.contains(
        'UNITED STATES SENATOR', case=False), 'contest'] = 'U.S. Senate'
    df.loc[df['contest'].str.contains(
        'U.S. REPRESENTATIVE', case=False), 'contest'] = 'U.S. House'
    df.loc[df['contest'].str.contains(
        'STATE ASSEMBLY', case=False), 'contest'] = 'State House'
    df.loc[df['contest'].str.contains(
        'STATE SENATE', case=False), 'contest'] = 'State Senate'

    # select only the positions of interest
    df = df[df['contest'].isin(positions)].copy()
    df.votes = pd.to_numeric(df.votes, errors='coerce')

    # reverse naming convention from last, first to first last
    names = []
    for index, row in df.iterrows():
        name = HumanName(row['selection'])
        names.append(" ".join([name.first, name.last, name.suffix]))
    names = pd.Series(names)
    df.selection = names.values
    df.selection = df.selection.str.title()
    df.selection = df.selection.str.strip()

    df = df.rename(columns = header_map)

    return df

if __name__ == '__main__':
    file = 'http://www.nvsos.gov/sos/home/showdocument?id=4615'
    df = parser(file, skiprows=[0,1], header=0)
    df.to_csv('2016/20161108__nv__general__precinct.csv',
        index=False, float_format='%.0f')

    file = 'http://nvsos.gov/sos/home/showdocument?id=3660'
    df = parser(file, skiprows=[0,1,2], header=0)
    df.to_csv('2012/20121106__nv__general__precinct.csv',
        index=False, float_format='%.0f')
    #
    file = 'http://nvsos.gov/sos/home/showdocument?id=3680'
    df = parser(file, skiprows=[0,1,2], header=0)
    df.to_csv('2008/20081104__nv__general__precinct.csv',
        index=False, float_format='%.0f')
    #
    file = 'http://nvsos.gov/sos/home/showdocument?id=3694'
    df = parser(file, skiprows=[0,1,2], header=0)
    df.to_csv('2004/20041102__nv__general__precinct.csv',
        index=False, float_format='%.0f')
