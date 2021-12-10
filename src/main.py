import argparse
import json
from phoneme_helper import PhonemeHelper
from distance_matrix import DistanceMatrix
from common import read_texts, sort_dict_by_values

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--text_dir", type=str, default=None, help="Path for parsed texts that will be hunted through and cleaed for similar phrases")
    parser.add_argument("--ngram", type=int, default=3, help="Perform search for a maximum sequence of ngram words when hunting for similar phonetic phrases")
    parser.add_argument("--threshold", type=float, default=None, help="Threshold for edit distance required to record a positive result and add it to the return list")
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    dm = DistanceMatrix()
    texts = read_texts(args.text_dir)

    #TODO - let the user look up a word by character string, not have to do this phonetic representation BS
    #Put words and their phonetic representations in all caps. Use the CMU dict to look them up. Remove any numeric component
    candidate_dict = {}
    candidate_dict['HELLO FRIEND'] = 'HH AH L OW F R EH N D'
    #candidate_dict['HEY YOU'] = 'HH EY Y UW'

    helper = PhonemeHelper(candidate_dict, ngram=args.ngram, distance_threshold=args.threshold, distance_matrix=dm)
    helper.search_texts(texts)

    all_res = {}
    all_res['dist'] = sort_dict_by_values(helper.distance_dict, reverse=False)
    all_res['counts'] = sort_dict_by_values(helper.occurrence_dict)
    all_res['unknown'] = sort_dict_by_values(helper.unknown_words) #you should iterate on this and add words to the vocabulary in future runs

    with open("results.json", "w") as f_out:
        json.dump(all_res, f_out, indent=4)
         
if __name__ == '__main__':
    main()
