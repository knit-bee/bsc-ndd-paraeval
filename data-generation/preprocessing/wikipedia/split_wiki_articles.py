"Find unique paragraphs in wikipedia data set and save each to file"


import ast
import os
import sys
from uuid import uuid4

import pandas as pd


def load_text_data(file_path):
    df = pd.read_csv(file_path)
    return df["text"]


def find_unique_paragraphs(text_col):
    all_paragraphs = set()
    for edit in text_col:
        all_paragraphs.update(ast.literal_eval(edit))
    return all_paragraphs


def main(input_dir, output_dir):
    all_files = os.listdir(input_dir)
    for file in all_files:
        texts = load_text_data(os.path.join(input_dir, file))
        all_paragraphs = find_unique_paragraphs(texts)
        for para in all_paragraphs:
            clean = para.strip()
            if clean:
                with open(
                    os.path.join(output_dir, f"{uuid4()}"), "w", encoding="utf-8"
                ) as ptr:
                    ptr.write(clean)


if __name__ == "__main__":
    input_dir, output_dir = sys.argv[1:]
    main(input_dir, output_dir)
