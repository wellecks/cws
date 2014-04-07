# Runs the entire CRF word segmentation process.
# Given an input training file, and an unsegmented testing file,
# produces a segmented testing file using a trained model.

def run(training, testing):
	train(training)
	test(testing)

def train(training):
	# tag the segmented training file

	# generate features for the tagged file

	# train a CRF model
	return -1

def test(testing):
	# tag the testing file with placeholder tags

	# generate features for the tagged file

	# generate predicted tags using the trained model

	# pair the testing characters with their predicted tags

	# convert the tagged file back to lines of text
	return -1

if __name__ == 'main':
	optparser = optparse.OptionParser()
	optparser.add_option("-t", "--training_filename", dest="training", action="store_true", default="data/training_seg.utf8", help="Training data filename.")
	optparser.add_option("-s", "--testing_filename", dest="testing", action="store_true", default="data/test_unseg.utf8", help="Unsegmented Testing data filename.")
	run(opts.training, opts.testing)