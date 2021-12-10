import numpy as np
import pandas as pd

class DistanceMatrix():
    def __init__(self, cv_fill=0., csv_f=None):
        self.cv_fill = cv_fill
        self.csv_f = "../resource/phonetic_cm_wang_bronwen_smoothed.csv" if csv_f is None else csv_f
        cm = self.load_csv()
        self.cm = self.normalize_cm(cm)
    
    def load_csv(self):
        cm_df = pd.read_csv(self.csv_f)
        cm_df = cm_df.drop(cm_df.columns[0], axis=1) #remove first column (the symbol names)

        # We set diagonals to 0 (for matching phonemes) first, so that we can get a smoother distribution over the normalized errors for other phonemes in a row
        cm_df.values[[np.arange(cm_df.shape[0])] * 2] = self.cv_fill
        
        return cm_df
    
    def normalize_cm(self, cm_df: pd.DataFrame, write_to_disk=True):
        def norm_dist(x):
            return 1. - x
        
        def square(x):
            return x**2

        #Take the log of each value, to give a smoother distribution between consonants
        cm_df.applymap(square)

        #normalize the squared sum to 1 for each phoneme
        cm_df = cm_df.div(cm_df.sum(axis=1), axis=0)

        #each value is subtracted from 1 to represent edit distance from each other phoneme.
        cm_df = cm_df.applymap(norm_dist)

        # Then set the diagonals to 0 (for matching phonemes) again.
        # Note this second time isn't really necessary since the levenshtein algorithm will call it 0 anyway, but still the right thing to do.
        cm_df.values[[np.arange(cm_df.shape[0])] * 2] = self.cv_fill
        if write_to_disk:
            cm_df.to_csv('normalized_phonetic_distance_matrix.csv', index=False)
        return cm_df
    
    def get_phoneme_distance(self, prediction, target):
        try:
            row_n = self.cm.columns.get_loc(target)
            col_n = self.cm.columns.get_loc(prediction)
        except KeyError:
            print("Could not locate columns for both phonemes {} and {}. Returning infinity".format(target, prediction))
            return np.inf
        
        return self.cm.iloc[row_n, col_n]


