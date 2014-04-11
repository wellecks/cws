#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A feature extractor for chunking.
Copyright 2010,2011 Naoaki Okazaki.

Modified by Sean Welleck for use in Chinese Word Segmentation application.
"""
import crfutils
import unicodedata
import sys

# Separator of field values in the tagged file.
separator = ' '

# Field names of the input data.
fields = 'c y'

# Feature templates; a tuple of (name, offset) pairs,
# where name and offset specify a field name and offset from which
# the template extracts a feature value.
#   E.g. (('c', -3), ('c', 0)) is a feature containing the current character
#   and the character three positions back.
#
# See http://www.newdesign.aclweb.org/anthology/Y/Y06/Y06-1012.pdf for ideas
# on good features to define here.
templates = (
	# YOUR CODE HERE: Define feature templates
    (('c', -3), ('c',  0)), # <-- example
    )

# Feature function that returns "1" if the given character
# is punctuation and "0" otherwise. Specifically, decides 
# whether it is a member of a Unicode punctuation character class.
def is_punct(c):
	# YOUR CODE HERE: define this feature function
	return None

# Optional: define some more feature functions.
def your_feature_function():
	return None

def feature_extractor(X):
    # Apply templates to obtain features.
    crfutils.apply_templates(X, templates)
    # Add the is_punct() feature.
    map(lambda x: x['F'].append("punct=" + is_punct(x['c'])), X)

# Generate features for a tagged file.
# Outputs a file in CRFSuite format.
# Details of the format are found at:
#	http://www.chokkan.org/software/crfsuite/manual.html#id532502
def generate(infile, outfile):
	sys.stderr.write("Generating features.\n")
	crfutils.main(feature_extractor, fields, separator, open(infile, 'r'), open(outfile, 'w'))

if __name__ == '__main__':
    crfutils.main(feature_extractor, fields=fields, sep=separator)
