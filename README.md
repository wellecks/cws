##Chinese Word Segmentation
In languages such as English or French, words are typically separated by spaces, making sentence tokenization simple. However, in Chinese (and Japanese Kanji), the written language consists of characters that are not delimited, making word tokenization difficult. A given character may have an independent meaning as a word, and a separate meaning when grouped with other characters. For instance, the character 中 means 'middle', 将 means 'will', and when combined, 中将 means 'lieutenant general'. This can lead to ambiguities when attempting to segment and translate a sentence, since depending on the context, the correct translation of 中将 may be 'middle will', while in another context it may be 'lieutenant general'. 

To illustrate with a couple English examples, first consider the character sequence “thesearedaredevils”. This sequence could either be segmented as “these are daredevils” or “the seared are devils”. Even a single segmentation affects the interpretation of a sentence: “iship” can be segmented as “I ship” or “is hip”, leading to the two different sentences “I’ll save the code that I ship” and “I’ll save the code that is hip”. Without word delimiters, Chinese text encounters these ambiguities, making Chinese word segmentation (CWS) an important step when translating from Chinese.

The CWS problem is to transform an input character sequence S without spaces to a sequence S', where S' contains spaces between word segments. Numerous methods have been developed or applied to the problem, such as the [Compression-Based algorithm](http://acl.ldc.upenn.edu/J/J00/J00-3004.pdf) and [Conditional Random Fields](http://scholarworks.umass.edu/cgi/viewcontent.cgi?article=1091&context=cs_faculty_pubs). 

##Default Model
A default word segmenter is included in `default_model.py`. It is a simple model that
adds a space after every Chinese character in the dataset. To run the model
on a test set, use the command:

```python default_model.py -f [test_filename] -o [desired_output_filename]```

e.g.

```python default_model.py -f "data/test_unseg.utf8" -o "default_output.utf8"```

##Objective Function
The ```score``` script computes the average of Recall, Precision, and F-Measure for a given prediction set. It takes three arguments: a dictionary, a truth dataset, and a predicted dataset. The script also has an optional ```-v``` (verbose) flag to output detailed statistics.

Example usage:

```./score data/dict.utf8 data/test_seg.utf8 default_output.utf8```
##Data
The dataset is provided by Beijing University. The training data has 1.1M Chinese words that are separated by line into sentences. There is a segmented and corresponding unsegmented version. The testing data consists of 104K Chinese words. Similar to the training set, there is a segmented file and a corresponding unsegmented file. Finally, to run the scoring script, a dictionary file is included.


##Your Task
Your task is to use Conditional Random Fields to segment Chinese words. For a good background, see [Chinese Segmentation and New Word Detection using Conditional Random Fields](http://scholarworks.umass.edu/cgi/viewcontent.cgi?article=1091&context=cs_faculty_pubs). (Note: of course you could also create a completely different model (e.g. compression-based) to beat the baseline!)

You can use the [CRFsuite](http://www.chokkan.org/software/crfsuite/) library to implement the model; several files have also been provided to help you implement the system.

First, install CRFsuite by following the instructions found [here](http://www.chokkan.org/software/crfsuite/manual.html#id489766). Then, read through [the tutorial](http://www.chokkan.org/software/crfsuite/tutorial.html) to get an idea of how the library works. You can then fill out the commands to train the model, and to run it on the test set in `crf.py`.

Next, pose word segmentation as a tagging problem by assigning a tag to each character based on whether it begins a new word (B) or does not begin a new word (N). The segmenting problem becomes a problem of assigning tags to the characters of a test sequence. In order to view the problem this way, we first need to tag the training set; to do so, fill in the functions found in `crf_formatter.py`. The CRFsuite tutorial is again helpful in understanding this step.

Finally, we define features for the CRF model. `features.py` contains an easy way of defining positional features using 'templates'. Your task is to define some of these features; see the paper
http://www.newdesign.aclweb.org/anthology/Y/Y06/Y06-1012.pdf for some good ideas. In addition, you can define your own feature functions without the templates. An example feature could be whether the current character is punctuation. Defining novel feature functions may be helpful in increasing your model's score.

To run the entire train / test / score process, use the command `python crf.py`. By default, the predicted segmentations will be written to `output/predictions.utf8`. Non-default filenames can be passed in as command-line arguments.

Using the baseline model, you should see the following output at the end:
```bash
=== TOTAL TRUE WORDS RECALL:	0.907
=== TOTAL TEST WORDS PRECISION:	0.926
=== F MEASURE:	0.916
0.916333
```
