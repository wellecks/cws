#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A feature extractor for chunking.
Copyright 2010,2011 Naoaki Okazaki.

Modified by Sean Welleck for use in Chinese Word Segmentation applicaiton.
"""

# Separator of field values.
separator = ' '

# Field names of the input data.
fields = 'w y'

# Attribute templates.
templates = (
    (('w', -2), ),
    (('w', -1), ),
    (('w',  0), ),
    (('w',  1), ),
    (('w',  2), ),
    (('w', -2), ('w', -1)),
    (('w', -1), ('w',  0)),
    (('w',  0), ('w',  1)),
    (('w', -1), ('w',  1)),
    (('w', -1), ('w',  0), ('w',  1)),
    )

import crfutils
import unicodedata

# Return whether the given character is punctuation.
# Specially, whether it is a member of the Unicode character
# class 'Po'.
def is_punct(c):
    c = c.decode('utf-8')
    if unicodedata.category(c) == 'Po':
        return "1"
    else:
        return "0"

def feature_extractor(X):
    # Apply attribute templates to obtain features (in fact, attributes).
    crfutils.apply_templates(X, templates)
    # Add the is_punct() feature.
    map(lambda x: x['F'].append("punct=" + is_punct(x['w']),), X)

if __name__ == '__main__':
    crfutils.main(feature_extractor, fields=fields, sep=separator)
