#!/usr/bin/env python3

'''Common code for takeoff analysis'''

import numpy as np
import pandas as pd
import cruise
from common import getLogger

log = getLogger(__name__)

def find_all_takeoffs(data, future=30):
    '''Return the number of detected takeoffs and
    a dataframe with all takeoff datapoints

    future -- number of datapoints for each takeoff (default 30)'''

    # Initial filter for faster processing
    indexes = data.index[(data['E1 RPM'] >= 2450) & (data['IAS'].between(50, 75))]
    if indexes.empty:
        return pd.DataFrame()

    takeoff_indexes = []
    skip = None
    for i in indexes:
        if i == skip:
            # Skip this one and the next. Same takeoff.
            skip += 1
            continue

        # If IAS is accelerating into 'future' at least 10 knots:
        if data[i:i+future]['IAS'].diff().sum() > 10:
            takeoff_indexes.append(i)

            # Skip the next data point, as it's the same takeoff
            skip = i + 1

    ranges = [np.arange(i, i+future) for i in takeoff_indexes]
    return len(takeoff_indexes), data.iloc[np.r_[tuple(ranges)]].reset_index(drop=True)

def to_analyze(data):
    '''Print and plot analysis for a given data column

    data -- a column from a data frame'''

    # Same as the cruise one right now. It may change.
    cruise.analyze(data)
