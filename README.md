# research_phonetic_edit_distance

## Purpose

This is a tool that performs a search on sequences of phonemes. Given a target text, it will search through a set of target texts and find ngrams with similar phonetic represetations as the phonetic representation of your target text.

## Installation

1. Maybe create a virtual environment, with `python3.6 -m venv .venv`
1. Activate the environment, with `source .venv/bin/activate`
1. Install requirements.txt with pip, with `pip install -r requirements.txt`

## Copyright Information

1. Carnegie Mellon University provides the phonetic representation dictionary found in `resource/cmudict-0.7b`
1. The edit distance mappings are mostly inspired from two papers:
1. Wang-Bilger's Confusion Matrix, from the paper by Marilyn DeMorrest Wang and Robert Bilger, "Consonant Confusions in Noise", JASA 54(5):1248-66. It has been further adapted to vowels and translated from its phonetic representation to Arpabet by me.
1. Munson, Benjamin & Donaldson, Gail & Allen, Shanna & Collison, Elizabeth & Nelson, David. (2003). Patterns of phoneme perception errors by listeners with cochlear implants as a function of overall speech perception ability. The Journal of the Acoustical Society of America. 113. 925-35. 10.1121/1.1536630.
1. Sungmin Lee, Lisa Lucks Mendel, Effect of the Number of Maxima and Stimulation Rate on Phoneme Perception Patterns Using Cochlear Implant Simulation. Clin Arch Commun Disord. 2016;1 (1): 87-100.
1. Bronwen G. Evans, Wafaa Alshangiti, The perception and production of British English vowels and consonants by Arabic learners of English, Journal of Phonetics, Volume 68, 2018, Pages 15-31, ISSN 0095-4470,
1. You may find this library useful for an arpabet->ipa mappings: https://github.com/wwesantos/arpabet-to-ipa/blob/master/src/App.php

## Phonetic Edit Distance Matrix Construction Methodology

Arpabet is a 39-phoneme representation of the English language, so the confusion matrix we need to build is a 39x39. Munson and Wang-Bilger provide good starting spots for filling in particular consonants,
namely fricatives, stops, and liquids. Munson doesn't include affricates, so those had to be inferred from Wang with the help of some spotty nearest-neighbor decisions on my part.

Three more consonants are missing as well, the hard H (HH in arpabet), the nasal NG, and W, which I filled in with the matrices from Wang CV2 and some more nearest neighbor decisions. I never filled matrix values with zero.

Vowels are taken from Bronwen and Evans, with care taken to remove the two vowels that are not part of Arpabet. In addition, Laplacian smoothing was added so there are no zero entries between vowels. This is to distinguish vowels from 0-filled consonant-vowel pairs in the matrix, which follows the intuition that humans and machines can distinguish between open and closed air flows.

It is common in the literature to also fill in a value of 0 for all consonant vs. vowel entries in the matrix. The exception is the R-colored vowel ER. This is not a zero entry between R-ER, but a scaled value I chose from some of the other sources listed above.

## Usage

1. `./run.sh` will run the program with default args.
1. You need to have at least one target sentence. You will need to enter a phonetic representation for your target phrase by looking it up in the CMU dict file at `resource/cmudict-0.7b`. Remove any numeric commponent of a phoneme. Have a look at `main.py` and see how the tool is used.
1. Two files will be created when you run the tool. The first, `normalized_phonetic_distance_matrix.csv` is a distance matrix between phonemes where you can look up the normalized distance between two phonemes. The second file, `results.json` is the results that contain the samples in the next under the specified threshold.
1. Make sure to point to a directory of parsed texts. These texts have some simple parsing logic in it. Change it for your data use case if they are in a different forat.
1. The return dictionary will show you vocabulary that could not be found in the dictionary. You can add these manually. I suggest using this tool http://www.speech.cs.cmu.edu/tools/lextool.html
1. You may wish to adjust the threshold or ngrams argument to speed things up or return more results.
