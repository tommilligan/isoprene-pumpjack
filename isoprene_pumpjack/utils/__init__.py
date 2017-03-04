#!/usr/bin/env python
'''Utility functions for isoprene_pumpjack'''

import logging

def object_fullname(obj):
    '''Returns the full absolute name of the object provided'''
    fullname = obj.__module__ + "." + obj.__class__.__name__
    return fullname

def object_logger(obj):
    '''Returns a correctly named logger for the given object'''
    fullname = object_fullname(obj)
    logger = logging.getLogger(fullname)
    return logger

def dedupe_dict_list(duped, id_prop):
    '''Dedupe a list of dicts by a dictionary property'''
    deduped = list({v[id_prop]:v for v in duped}.values())
    return deduped