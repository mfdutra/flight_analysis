#!/usr/bin/env python3

'''Common I/O functions'''

from io import BytesIO
import glob
import logging
import time
import pandas as pd
import pandas.api.types as ptypes

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(message)s'))
log.handlers = [handler]

def open_g1000_data(filename):
    '''Return a data frame for one flight'''

    # G1000's data isn't very clean unfortunately.
    # List of issues I've observed so far:
    #
    # - The avionics starts logging before knowing what time it is
    #   First data points will have no date and time information
    #
    # - Since there's no clean shutdown, the last line is usually broken
    #
    # - On some departure or missed approach procedures, the avionics logs
    #   the byte 0x80, which can't be decoded in ascii or utf-8
    buffer = BytesIO()
    with open(filename, 'rb') as f:
        for line in f:
            # All lines should be terminated with \n.
            # If not, it's likely the avionics was powered off.
            if not line.endswith(b'\n'):
                continue

            # Skip lines with no date and time information
            if line.startswith(b'        '):
                continue

            # Remove 0x80 bytes
            line = line.replace(b'\x80', b'')

            buffer.write(line)

    buffer.seek(0)

    # The internal time series must be converted to UTC, because on long
    # flights, the avionics may change the timezone automatically
    df = pd.read_csv(buffer, header=0, comment='#',
                     skipinitialspace=True,
                     parse_dates={'DateTime': [0, 1, 2]},
                     date_parser=lambda col: pd.to_datetime(col, utc=True),
                     low_memory=False)
    assert ptypes.is_datetime64_any_dtype(df['DateTime'])

    return df

def open_all_directory(directory, recursive=False, match='*.csv', ignore_errors=False):
    '''Scan a directory, loading all flights and building one giant
    data frame

    recursive -- (default False)
    match -- what files to match (default *.csv)
    ignore_errors -- keep going if one file fails (default False)'''

    t1 = time.time()
    result = pd.DataFrame()
    flights = 0
    log.info('Scanning %s. This may take a long time.', directory)
    for f in sorted(glob.glob(directory + '/' + match, recursive=recursive)):
        log.debug('Loading %s', f)
        try:
            df = open_g1000_data(f)

        except pd.errors.EmptyDataError:
            continue

        except Exception:
            log.error('Error loading %s', f)
            if ignore_errors:
                continue
            raise

        result = result.append(df, ignore_index=True)
        flights += 1

    log.info('Loaded %d flights, with %d data points', flights, len(result))
    log.debug('Took %.2f seconds to load all flights', time.time() - t1)

    return result
