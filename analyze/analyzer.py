import json
import pandas as pd
import scipy.stats as ss
import numpy as np
import matplotlib.pyplot as plt
import math

def analysis_correlation(resultfiles):
    with open(resultfiles['tourspot_visitor'], 'r', encoding = 'utf-8') as infile:
        json_data = json.loads(infile.read())
        print(json_data)

    tourspotvisitor_table = pd.DataFrame(json_data, columns = ['count_forigner', 'date', 'tourist_spot'])
    temp_tourspotvisitor_table = pd.DataFrame(tourspotvisitor_table.groupby('date')['count_forigner'].sum())

    results = []
    for filename in resultfiles['foreign_visitor']:
        with open(filename, 'r', encoding='utf-8')as infile:
            json_data = json.loads(infile.read())

        foreignvisitor_table = pd.DataFrame(json_data, columns=['country_name', 'date', 'visit_count'])
        foreignvisitor_table = foreignvisitor_table.set_index('date')
        merge_table = pd.merge(temp_tourspotvisitor_table,
                 foreignvisitor_table,
                 left_index=True, right_index=True)

        x = list(merge_table['visit_count'])
        y = list(merge_table['count_forigner'])
        country_name = foreignvisitor_table['country_name'].unique().item(0)
        r = ss.pearsonr(x, y)[0]
        r2 = ss.pearsonr(x, y)[1]
        print(r, r2)
        # r = np.corrcoef(x, y)[0]
        results.append({'x':x, 'y':y, 'country_name':country_name, 'r':r})
        merge_table['visit_count'].plot(kind='bar')
        plt.show()
    return results

def analysis_correlation_by_tourspot(resultfiles):
    with open(resultfiles['tourspot_visitor'], 'r', encoding = 'utf-8') as infile:
        json_data = json.loads(infile.read())
    tourspotvisitor_table = pd.DataFrame(json_data, columns = ['date', 'count_forigner', 'tourist_spot'])

    results = []
    json_data2 = []
    r=[]
    x= []
    for filename in resultfiles['foreign_visitor']:
        with open(filename, 'r', encoding='utf-8')as infile:
            # ad += infile.read()
            json_data2 += json.loads(infile.read())
    # print(json_data2)
    foreignvisitor_table = pd.DataFrame(json_data2[:12], columns=['country_name', 'date', 'visit_count'])
    foreignvisitor_table2 = pd.DataFrame(json_data2[12:23], columns=['country_name', 'date', 'visit_count'])
    foreignvisitor_table3 = pd.DataFrame(json_data2[23:], columns=['country_name', 'date', 'visit_count'])

    mg = pd.merge(tourspotvisitor_table, foreignvisitor_table)
    mg2 = pd.merge(tourspotvisitor_table, foreignvisitor_table2)
    mg3 = pd.merge(tourspotvisitor_table, foreignvisitor_table3)

    tourist_spot = tourspotvisitor_table['tourist_spot'].unique()
    forigner_country = foreignvisitor_table['country_name'].unique()

    for i in range(len(tourist_spot)):
        # tmp = mg[mg['country_name'] == mg['country_name'].unique().item(j)]
        temp_table = mg[mg['tourist_spot'] == mg['tourist_spot'].unique().item(i)]
        temp_table2 = mg2[mg2['tourist_spot'] == mg2['tourist_spot'].unique().item(i)]
        temp_table3 = mg3[mg3['tourist_spot'] == mg3['tourist_spot'].unique().item(i)]
        # print(temp_table)

        x = list(temp_table['visit_count'])
        y = list(temp_table['count_forigner'])
        x2 = list(temp_table2['visit_count'])
        y2 = list(temp_table3['count_forigner'])
        x3 = list(temp_table2['visit_count'])
        y3 = list(temp_table3['count_forigner'])

        r = (correlation_coefficient(x, y))
        r2 = (correlation_coefficient(x2, y2))
        r3 = (correlation_coefficient(x3, y3))

        print(tourist_spot[i])
        results.append({'tourspot': tourist_spot[i], 'r_중국': r, 'r_일본': r2, 'r_미국': r3})

    return results

def correlation_coefficient(x, y):
    n = len(x)
    vals = range(n)
    x_sum = 0.0
    y_sum = 0.0
    x_sum_pow = 0.0
    y_sum_pow = 0.0
    mul_xy_sum = 0.0

    for i in vals:
        mul_xy_sum = mul_xy_sum + float(x[i]) * float(y[i])
        x_sum = x_sum + float(x[i])
        y_sum = y_sum + float(y[i])
        x_sum_pow = x_sum_pow + pow(float(x[i]), 2)
        y_sum_pow = y_sum_pow + pow(float(y[i]), 2)

    try:
        r = ((n * mul_xy_sum) - (x_sum * y_sum)) / \
            math.sqrt(((n * x_sum_pow) - pow(x_sum, 2)) * ((n * y_sum_pow) - pow(y_sum, 2)))
    except ZeroDivisionError:
        r = 0.0
    return r