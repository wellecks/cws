# -*- coding: utf-8 -*-

### crf_formatter.py
# Converts files to / from SIGHAN TAGGED TAGGED formats.
# Use -c flag for SIGHAN      -> TAGGED.
# Use -s flag for TAGGED      -> SIGHAN.
# Use -p flag for predictions -> SIGHAN.
# Use -i flag to specify input filename.
# Use -n flag to specify number of input lines.
# Outputs to STDOUT.
#
# Ex: python crf_formatter.py -c -i "data/test_seg.utf8" > data/test_sighan.utf8
#     python crf_formatter.py -s -i "data/test_sighan.utf8" > data/test_seg.utf8

import codecs
import optparse
import sys
import os
import tempfile

# Converts a segmented corpus in SIGHAN format into a TAGGED file.
# Output Format:
#    CHAR B
#    CHAR N
#    ...
# B = beginning of word tag. N = non-beginning of word tag.
# CHAR = Chinese character. A blank line separates sentences.
# segname - filename of segmented corpus
# n - number of lines to convert
def sighan_to_tagged(segname, n, outfile=None):
	sys.stderr.write("Converting SIGHAN to TAGGED format.\n")
	if outfile == None:
		out = codecs.getwriter("utf-8")(sys.stdout)
	else:
		out = codecs.open(outfile, 'wb', encoding='utf-8')
	for line in codecs.open(segname, 'r', encoding='utf-8'):
		numspaces = 0
		first = True
		for c in line:
			if c == ' ':
				numspaces += 1
				if numspaces == 2:
					first = True
					numspaces = 0
			elif c != '\r' and c != '\n':
				if first:
					out.write(c + ' B\n')
					first = False
				else:
					out.write(c + ' N\n')
		out.write('\n')
		n -= 1
		if n == 0: break

# Converts a TAGGED file into a segmented SIGHAN format file.
# The SIGHAN format is one sentence per line, words delimited by two spaces.
def tagged_to_sighan(crfname, n, outfile=None):
	sys.stderr.write("Converting TAGGED to SIGHAN format.\n")
	if outfile == None:
		out = codecs.getwriter("utf-8")(sys.stdout)
	else:
		out = codecs.open(outfile, 'wb', encoding='utf-8')
	start = True
	for line in codecs.open(crfname, 'r', encoding='utf-8'):
		if line == '\n':
			out.write('\n')
			start = True
		else:
			c, tag = line.split(' ')
			if tag.strip() == u'B':
				if start:
					out.write(c)
					start = False
				else:
					out.write(' ' + c)
			else:
				out.write(c)
		n -= 1
		if n == 0: break

# Pairs each character from the test set with its predicted tag.
# Then converts the (character, tag) pairs into SIGHAN format.
def predictions_to_sighan(test_chars, tags, tagfile=None, outfile=None):
	sys.stderr.write("Pairing characters with tags.\n")
	chrs = codecs.open(test_chars, 'r', encoding='utf-8')
	if tagfile:
		tags = codecs.open(tagfile, 'r', encoding='utf-8')
	temp = tempfile.NamedTemporaryFile(delete=False)
	tempname = temp.name
	with temp as f:
		for (char, tag) in zip([line[0] for line in chrs], [line for line in tags]):
			if char == '\n':
				f.write('\n')
			else:
				if tagfile:
					f.write((char + ' ' + tag).encode('utf-8'))
				else:
					f.write((char + ' ' + tag + '\n').encode('utf-8'))
	tagged_to_sighan(tempname, sys.maxint, outfile)
	os.unlink(temp.name)

if __name__ == '__main__':
	optparser = optparse.OptionParser()
	optparser.add_option("-c", "--sighan_to_tagged", dest="c", action="store_true", default=False, help="Convert SIGHAN to CRFSUITE format.")
	optparser.add_option("-s", "--tagged_to_sighan", dest="s", action="store_true", default=False, help="Convert CRFSUITE format to SIGHAN.")
	optparser.add_option("-i", "--input_filename", dest="i", default="data/training_seg.utf8", help="Input filename.")
	optparser.add_option("-n", "--num_lines", dest="i", default=sys.maxint, help="Number of input lines.")
	optparser.add_option("-p", "--pred_to_sighan", dest="p", action="store_true", default=False, help="Convert predictions to SIGHAN.")
	(opts,_) = optparser.parse_args()
	if (not opts.c and not opts.s and not opts.p):
		optparser.print_help()
	elif opts.c:
		sighan_to_tagged(opts.i, opts.n)
	elif opts.s:
		tagged_to_sighan(opts.i, opts.n)
	elif opts.p:
		predictions_to_sighan("output/test_crfsuite.utf8", [], tagfile="output/tag_predictions2.utf8")
