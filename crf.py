# Runs the entire CRF word segmentation process.
# Given an input training file, and an unsegmented testing file,
# produces a segmented testing file using a trained model.
# Also scores the segmented file and outputs a score to STDOUT.

import crf_formatter
import features
import sys
import optparse
import os
from subprocess import call, Popen, PIPE
import tempfile

def run(training, testing, predfile='output/predictions.utf8', 
	model='models/crf.model', d='data/dict.utf8', targets='data/test_seg.utf8'):
	train(model, training)
	test(model, testing, predfile)
	evaluate(d, targets, predfile)

def train(model, training):
	sys.stderr.write("Training.\n")
	training_tagfile = tempfile.NamedTemporaryFile(delete=False)
	training_features = tempfile.NamedTemporaryFile(delete=False)
	# tag the segmented training set
	crf_formatter.sighan_to_tagged(training, training_tagfile.name)
	# generate features for the tagged set
	features.generate(training_tagfile.name, training_features.name)

	# Call CRFSuite using the command line to train a CRF model.
	### Your code here: define the command.
	cmd = ["crfsuite",  "learn", "-m", model, training_features.name]
	call(cmd)

	# clear the temp files
	os.unlink(training_tagfile.name)
	os.unlink(training_features.name)

def test(model, testing, outfile):
	sys.stderr.write("Testing.\n")
	testing_tagfile = tempfile.NamedTemporaryFile(delete=False)
	testing_features = tempfile.NamedTemporaryFile(delete=False)
	# tag the testing file with placeholder tags
	crf_formatter.sighan_to_tagged(testing, testing_tagfile.name)
	# generate features for the tagged file
	features.generate(testing_tagfile.name, testing_features.name)
	
	# Generate predicted tags using the trained model
	sys.stderr.write("Predicting tags.\n")

	# Call CRFSuite using the command line to tag the testing_features
	# using your trained CRF model.
	### Your code here: define the command.
	cmd = ["crfsuite",  "tag", "-m", model, testing_features.name]
	predictions, _ = Popen(cmd, stdout=PIPE).communicate()
	
	# pair the testing characters with their predicted tags
	# convert the tagged file back to lines of text
	crf_formatter.predictions_to_sighan(testing_tagfile.name, predictions.split('\n'), outfile=outfile)
	
	# clear the temp files
	os.unlink(testing_tagfile.name)
	os.unlink(testing_features.name)

def evaluate(dictionary, targets, predictions):
	sys.stderr.write("Evaluating predictions.\n")
	cmd = ["./score",  dictionary, targets, predictions]
	score, _ = Popen(cmd, stdout=PIPE).communicate()
	print score

if __name__ == '__main__':
	optparser = optparse.OptionParser()
	optparser.add_option("-t", "--training_filename", dest="trainset", 
		default="data/training_seg.utf8", help="Training data filename.")
	optparser.add_option("-s", "--testing_filename", dest="testset", 
		default="data/test_unseg.utf8", help="Unsegmented Testing data filename.")
	(opts,_) = optparser.parse_args()
	run(opts.trainset, opts.testset, opts.n)