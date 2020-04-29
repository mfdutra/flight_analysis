#!/usr/bin/env python3

'''Common code for cruise analysis'''

import matplotlib.pyplot as plt
from common import getLogger

log = getLogger(__name__)

def find_cruise_data(data):
    '''Return a data frame with all cruise data

    Definition of cruise is IAS above 60 and vertical speed within +/- 200 fpm'''

    return data[(data['IAS'] > 60) & (data['VSpd'].between(-200, 200))].reset_index(drop=True)

def analyze(data):
    '''Print and plot analysis for a given data column

    data -- a column from a data frame'''

    fig = plt.figure()
    p1 = fig.add_subplot(2, 2, 1)
    p2 = fig.add_subplot(2, 2, 2)

    data.rolling(len(data) // 20).median().plot.line(ax=p1, title='Trend (moving median)')
    p1.get_xaxis().set_visible(False)

    data.plot.kde(ax=p2, title='Distribution')

    print(data.describe())
