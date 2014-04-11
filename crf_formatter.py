# -*- coding: utf-8 -*-

### crf_formatter.py
# Converts files to / from lines of text and TAGGED formats.
# Sean Welleck | 2014
# 
# The Text format is one sentence per line, with characters and punctuation
# separated by spaces. The is the format specified by the SIGHAN competition:
# (http://www.sighan.org/bakeoff2005/data/instructions.php.htm).
# 
# The Tagged format is one character and one tag per line, separated by a space.
# A blank line separates sentences.	
# 
import codecs
import optparse
import sys
import os
import tempfile

# Converts a corpus in SIGHAN format into a TAGGED file.
# Input (Text) Format:
#    为  祖国  守岁  
#    编者  的  话 
#    ...
#  One sentence per line, words separated by a space.
#
# Output (Tagged) Format:
#    为 B
#    祖 B
#    国 N
#    守 B
#    岁 N
#
#    编 B
#    者 N
#    ...
#  B = beginning of word tag. N = non-beginning of word tag.
#  A blank line separates sentences.
#
#   corpus - filename of corpus
#   outfile - desired filename of tagged data
def text_to_tagged(corpus, outfile):
	sys.stderr.write("Converting SIGHAN text format to TAGGED format.\n")
	out = codecs.open(outfile, 'wb', encoding='utf-8')
	for line in codecs.open(corpus, 'r', encoding='utf-8'):
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

# Converts a tagged file into a segmented SIGHAN format file.
# The text format is one sentence per line, words delimited by a space.
#   tagged  - filename of tagged data
#   outfile - desired filename of text data
def tagged_to_text(tagged, outfile):
	sys.stderr.write("Converting TAGGED to SIGHAN text format.\n")
	out = codecs.open(outfile, 'wb', encoding='utf-8')
	start = True
	for line in codecs.open(tagged, 'r', encoding='utf-8'):
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

# Pairs each character from the test set with its predicted tag.
# Then converts the (character, tag) pairs into a SIGHAN text format.
# 
# test_tags - tagged test set with placeholder tags (one [char tag] pair per line)
# pred_tags - list of predicted tags output by CRFSuite, e.g. ['B', 'N', ... ]
# outfile   - desired name for segmented output text file.
def predictions_to_text(test_tags, pred_tags, outfile):
	sys.stderr.write("Pairing characters with tags.\n")
	chrs = codecs.open(test_tags, 'r', encoding='utf-8')
	temp = tempfile.NamedTemporaryFile(delete=False)
	tempname = temp.name
	with temp as f:
		for (char, tag) in zip([line[0] for line in chrs], [line for line in pred_tags]):
			if char == '\n':
				f.write('\n')
			else:
				f.write((char + ' ' + tag + '\n').encode('utf-8'))
	tagged_to_text(tempname, outfile)
	os.unlink(temp.name)
