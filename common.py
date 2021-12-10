from typing import Dict
import os
import re

def read_texts(text_dir):
    texts = []
    for f in os.listdir(text_dir):
        if f.endswith(".txt"):
            f = os.path.join(text_dir, f)
            text_parsed = _parse_text(f)
            texts.append(text_parsed)
    return texts

def _parse_text(text_path: str):
    all_text = []

    with open(text_path, 'r') as fp:
        for line in fp:
            text = line.strip()
            if text.endswith(("?", "!", ".")):
                text = text[:-1]
            text = text.replace(",", "")
            text = text.replace("-", " ")
            text = text.replace(".", " ")
            text = text.replace(":", " ")
            text = text.replace("9", " nine ")
            text = text.replace("8", " eight ")
            text = text.replace("7", " seven ")
            text = text.replace("6", " six ")
            text = text.replace("5", " five ")
            text = text.replace("4", " four ")
            text = text.replace("3", " three ")
            text = text.replace("2", " two ")
            text = text.replace("1", " one ")
            text = text.replace("0", " zero ")
            text = re.sub('\s+',' ', text)
            text = text.rstrip()
            all_text.append(text.lower())
    full_text = " ".join([k for k in all_text])
    return full_text

def sort_dict_by_values(d, reverse=True):
    return {k: v for k, v in sorted(d.items(), key=lambda x: x[1], reverse=reverse)}