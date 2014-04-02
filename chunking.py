#!/usr/bin/env python

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

def feature_extractor(X):
    # Apply attribute templates to obtain features (in fact, attributes)
    crfutils.apply_templates(X, templates)

if __name__ == '__main__':
    crfutils.main(feature_extractor, fields=fields, sep=separator)
