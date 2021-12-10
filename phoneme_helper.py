from typing import Dict, List
from tqdm import tqdm
import numpy as np
from math import sqrt

class PhonemeHelper():
    def __init__(self, targets, ngram=3, distance_threshold=None, distance_matrix=None):
        self.phoneme_dict = self._read_cmu_arpabet_dict()
        self.targets = self._assign_targets(targets)
        self.distance_thresholds = self._initialize_distance_threshold(targets, distance_threshold)
        self.ngram = ngram
        self.distance_matrix = distance_matrix
        self.distance_dict = {}
        self.occurrence_dict = {}
        self.unknown_words = {}

    def _initialize_distance_threshold(self, target_dict, distance_threshold):
        if distance_threshold is None:
            distance_thresholds = {k: round(sqrt(len(v.split(" ")))) + 1 for k,v in target_dict.items()}
        else:
            distance_thresholds = {k: distance_threshold for k in self.targets}
        print("Using the following edit distance thresholds: {}".format(distance_thresholds))
        return distance_thresholds
    
    def _read_cmu_arpabet_dict(self):
        filename = "../resource/cmudict-0.7b"
        to_skip = 127
        num_read = 0
        phoneme_dict = {}
        # open the file for reading
        filehandle = open(filename, 'r', encoding='latin1')
        while True:
            line = filehandle.readline()
            num_read += 1
            if num_read < to_skip:
                continue
            if not line:
                break
            line = line.split(" ")
            word = line[0]
            if "(" in word: #alternate pronunciation
                continue
            line[-1] = line[-1].strip()
            pronunciation = ""
            for w in line[2:]:
                res = ''.join([i for i in w if not i.isdigit()])
                pronunciation += res
                pronunciation += " "
            phoneme_dict[word] = pronunciation.strip()

        filehandle.close()
        return phoneme_dict
    
    def _assign_targets(self, target_dict):
        self.add_vocabulary(target_dict)
        return list(target_dict.keys())
    
    def add_vocabulary(self, vocab: Dict):
        for k,v in vocab.items():
            self.phoneme_dict[k] = v
    
    def add_to_phoneme_distance_dict(self, candidate, target, distance):
        key = candidate + "|" + target
        self.distance_dict[key] = distance

    def add_to_phoneme_occurrence_dict(self, candidate, target):
        key = candidate + "|" + target
        self.occurrence_dict[key] = self.occurrence_dict.get(key,0) + 1

    def check_phonemes(self, candidate, target, threshold):
        ha_d = self.get_phoneme_edit_distance(candidate, target)
        if ha_d <= threshold and ha_d > -1:
            self.add_to_phoneme_distance_dict(candidate, target, ha_d)
            self.add_to_phoneme_occurrence_dict(candidate, target)
        return ha_d
    
    def _search(self, ngram_size, all_texts):
        for text in tqdm(all_texts):
            words = text.split(" ")
            if len(words) < ngram_size:
                continue
            for start_index in tqdm(range(len(words) - (ngram_size-1)), leave=False):
                word_list = [words[start_index+i] for i in range(ngram_size)]
                ngram = " ".join([w for w in word_list])
                for target in self.targets:
                    score = self.check_phonemes(ngram, target, self.distance_thresholds[target])
    
    def search_texts(self, all_texts):
        for ngram_size in range(1,self.ngram+1):
            print("Checking {}grams".format(ngram_size))
            self._search(ngram_size, all_texts)
    
    def _levenshtein_edit_distance(self, seq1: List, seq2: List):
        """
        Computes levenshtein edit distance between two list sequences, given an optional edit distance matrix.
        
        Args:
            seq1: The list of phonemes in candidate (prediction), for example: ['AE', 'P', 'AH', 'L'] (Apple)
            seq2: The list of phonemes in target, for example: ['B' 'AH' 'N' 'AE' 'N' 'AH'] (Banana)

        This algorithm computes levenshtein edit distance, but instead of defaulting to a 0/1 identify function for comparing
        distance between two entities, looks up the distance in a table.
        """
        size_x = len(seq1) + 1
        size_y = len(seq2) + 1
        matrix = np.zeros((size_x, size_y))
        for x in range(size_x):
            matrix[x, 0] = x
        for y in range(size_y):
            matrix[0, y] = y

        for x in range(1, size_x):
            for y in range(1, size_y):

                #If the two phonemes are the same, then we use an edit distance of 1 to represent insertion/deletion
                if seq1[x-1] == seq2[y-1]:
                    matrix[x,y] = min(
                        matrix[x-1, y] + 1,
                        matrix[x-1, y-1],
                        matrix[x, y-1] + 1
                    )
                
                #Otherwise, we look the phonemes up in the matrix we built. If no matrix is present, we use a 1 identify function
                else:
                    dist = self.distance_matrix.get_phoneme_distance(seq1[x-1], seq2[y-1]) if self.distance_matrix is not None else 1
                    matrix [x,y] = min(
                        matrix[x-1,y] + dist,
                        matrix[x-1,y-1] + dist,
                        matrix[x,y-1] + dist
                    )
        return (matrix[size_x - 1, size_y - 1])
        
    def get_phoneme_edit_distance(self, candidate, target):
        candidate = candidate.upper()
        target = target.upper()

        candidate_word_list = candidate.split(" ")
        candidate_phoneme_list = []

        for candidate in candidate_word_list:
            try:
                p = self.phoneme_dict[candidate]
                candidate_phoneme_list.append(p)
            except KeyError: #If a word isn't in the dictionary, return -1 but add to a unknown word dict so that you can call add_vocabulary() with them
                self.unknown_words[candidate] = self.unknown_words.get(candidate, 0) + 1
                return -1
        
        try:
            target_representation = self.phoneme_dict[target]
        except KeyError:
            print("Target {} was not found. Make sure you called assign_targets(d) with a dictionary d that contains the words and phonemes of all of your targets")
            raise KeyError

        candidate_representation = " ".join([c for c in candidate_phoneme_list]) # need to add a space between the words

        c = [p for p in candidate_representation.split()]
        t = [p for p in target_representation.split()]
        d = self._levenshtein_edit_distance(c, t)
        return d

        
