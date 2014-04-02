# -*- coding: utf-8 -*-
import optparse
import codecs
import sys
import unicodedata

optparser = optparse.OptionParser()
optparser.add_option("-f", "--unsegmented-input-file", dest="f", default="data/training_unseg.utf8", help="N-best lists")
optparser.add_option("-n", "--num-training-sentences", dest="n", default=sys.maxint, type="int", help="Number of training sentences (default=all)")
optparser.add_option("-o", "--output-file", dest="o", default="output/basic_output.utf8", help="Number of training sentences (default=all)")
(opts,_) = optparser.parse_args()

# read in n lines of the given utf8 file
space = '  '
train = [line for line in codecs.open(opts.f, 'r', encoding='utf-8')][:opts.n]
		
seg_train = [space.join(line) for line in train]
with open(opts.o, 'wb') as f:
	for line in seg_train: 
		f.write(line.encode('utf-8').replace('\r', ''))