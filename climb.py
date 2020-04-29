#!/usr/bin/env python3

'''Common code for climb analysis'''

import cruise
from common import getLogger

log = getLogger(__name__)

def find_climb_data(data):
    '''Return a data frame with all climb data

    Definition of cruise is IAS above 70 and vertical speed > 200 fpm'''

    return data[(data['IAS'] > 60) & (data['VSpd'] > 200)].reset_index(drop=True)

def analyze(data):
    '''Print and plot analysis for a given data column

    data -- a column from a data frame'''

    # Same as the cruise one right now. It may change.
    cruise.analyze(data)
