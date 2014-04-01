cws
===

##Chinese Word Segmentation - Overview
In languages such as English or French, words are typically separated by spaces, making sentence tokenization simple. However, in Chinese (and Japanese Kanji), the written language consists of characters that are not delimited, making word tokenization difficult. A given character may have an independent meaning as a word, and a separate meaning when grouped with other characters. For instance, the character 中 means 'middle', 将 means 'will', and when combined, 中将 means 'lieutenant general'. This can lead to ambiguities when attempting to segment and translate a sentence, since depending on the context, the correct translation of 中将 may be 'middle will', while in another context it may be 'lieutenant general'. 

To illustrate with a couple English examples, first consider the character sequence “thesearedaredevils”. This sequence could either be segmented as “these are daredevils” or “the seared are devils”. Even a single segmentation affects the interpretation of a sentence: “iship” can be segmented as “I ship” or “is hip”, leading to the two different sentences “I’ll save the code that I ship” and “I’ll save the code that is hip”. Without word delimiters, Chinese text encounters these ambiguities, making Chinese word segmentation (CWS) an important step when translating from Chinese.

The CWS problem is to transform an input character sequence S without spaces to a sequence S', where S' contains spaces between word segments. Numerous methods have been developed or applied to the problem, such as the Compression-Based algorithm, Conditional Random Fields, and the Maximum Entropy Model. 

##This Project
This project implements three models:
  1. A basic baseline model that simply adds a space after every one or two characters.
  2. A Conditional Random Field model, using the CRFSUITE library.
  3. A Compression-based model.

The dataset used is a standard corpus provided by Beijing University, that was used in the SIGHAN Bakeoff.

###Files  
```score```: a perl script that computes the average of Recall, Precision, and F-Measure, as well as various statistics for a given prediction set. It is a slightly modified version of the script used for the SIGHAN Bakeoff competition. Contains an optional ```-v``` (verbose) flag.
