#!/usr/bin/env python3

'''Common functions'''

import logging

def getLogger(name):
    '''Return a configured logging'''

    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(message)s'))
    log.handlers = [handler]
    return log
