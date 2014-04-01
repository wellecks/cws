# -*- coding: utf-8 -*-

import codecs

# Converts a segmented corpus in SIGHAN format into a CRFSuite-formatted file.
# Format:
#    CHAR B
#    CHAR N
#    ...
# B = beginning of word tag. N = non-beginning of word tag.
# CHAR = Chinese character. A blank line separates sentences.
# segname - filename of segmented corpus
# outname - desired output filename
def sighan_to_crf(segname, outname):
	with codecs.open(outname, 'wb', encoding='utf-8') as out:
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

# Converts a CRFSuite-formatted file into a segmented SIGHAN format file.
# The SIGHAN format is one sentence per line, words delimited by two spaces.
def crf_to_sighan(crfname, outname):
	with codecs.open(outname, 'wb', encoding='utf-8') as out:
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


