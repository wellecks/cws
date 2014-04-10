# -*- coding: utf-8 -*-
import optparse
import codecs
import unicodedata
import sys

optparser = optparse.OptionParser()
optparser.add_option("-f", "--unsegmented-test-file", dest="f", default="data/test_unseg.utf8", help="Unsegmented test file")
optparser.add_option("-n", "--num-sentences", dest="n", default=sys.maxint, type="int", help="Number of sentences to process (default=all)")
optparser.add_option("-o", "--output-file", dest="o", default="basic_output.utf8", help="Desired output file (default=basic_output.utf8)")
(opts,_) = optparser.parse_args()

# read in n lines of the given utf8 file
space = '  '
train = [line for line in codecs.open(opts.f, 'r', encoding='utf-8')][:opts.n]
seg_train = [space.join(line) for line in train]
with open(opts.o, 'wb') as f:
	for line in seg_train: 
		f.write(line.encode('utf-8').replace('\r', ''))