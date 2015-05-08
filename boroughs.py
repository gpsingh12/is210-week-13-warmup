#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Task_01"""


import csv
import json

GRADES = {
    'A': 1.0,
    'B': 0.90,
    'C': 0.80,
    'D': 0.70,
    'F': 0.60,
}


def get_score_summary(filename):
    """Function takes one argument as string which represent the filename
       whose data will be read and intrepreted.
    Args:
        filename(str):input value of data to be read.
    Returns:
        returns a dictionary with average score of the key of ditionary.
    Examples:
        >>>get_score_summary('inspection_results.csv')
        >>> {'BRONX': (156, 0.9762820512820514), 'BROOKLYN':
        (417, 0.9745803357314141), 'STATEN ISLAND': (46, 0.9804347826086955),
        'MANHATTAN': (748, 0.9771390374331531), 'QUEENS':
        (414, 0.9719806763285017)}
    """

    fhandler = open(filename, 'r')
    reader = csv.reader(fhandler, delimiter=',')
    mydict = {}
    for line in reader:
        if line[0] not in mydict and line[10] in GRADES:
            mydict[line[0]] = [line[1], line[10]]
    fhandler.close()

    mydict2 = {}
    for someval in mydict.itervalues():
        if someval[1] in mydict2:
            mydict2[someval[1]][1] += GRADES[someval[0]]
            mydict2[someval[1]][0] += 1
        else:
            mydict2[someval[1]] = [1, GRADES[someval[0]]]

    retval = {}
    for somekey, someval in mydict2.iterkeys():
        retval1 = [someval][0]
        retval2 = [someval][1]/retval1
        retval[somekey] = (retval1, retval2)
    return retval


def get_market_density(filename):
    """Function loads data using json module.
    Args:
        filename(str): input file for opening
    Return:
        return a dictionary performing calculations on the json file
    Examples:
        >>>get_market_density('green_markets.json')
        {u'STATEN ISLAND': 2, u'BROOKLYN': 48, u'BRONX': 32,
        u'MANHATTAN': 39, u'QUEENS': 16}
    """
    fhandler = open(filename, 'r')
    load_data = json.load(fhandler)
    fhandler.close()
    ret_data = {}
    for somedata in load_data:
        data1 = somedata[8].strip().upper()
        if data1 not in ret_data:
            ret_data[data1] = 1
        else:
            ret_data[data1] += 1
    return ret_data


def correlate_data(restscores, markdata, outfile):
    """Function takes three arguments and return  data into a single dictionary.
    Args:
        restscores(file): inspection.csv file containing restraunts scores data.
        markdata(file): green_markets.json file containing market data.
        outfile(file): file returning output of this function.
    Return:
        returns the data into single dictionary.
    """
    agg_score = get_score_summary(restscores)
    agg_mdata = get_market_density(markdata)
    final_dict = {}
    for somekey, someval in agg_score.iteritems():
        if somekey in agg_mdata:
            data2 = float(agg_mdata[somekey])/someval[0]
            final_dict[somekey] = (someval[1], data2)
    fhandler = open(outfile, 'w')
    json.dump(final_dict, fhandler)
    fhandler.close()
    return final_dict
