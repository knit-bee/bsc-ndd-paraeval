"Split xml files into paragraphs (used for 'blogs' and 'wikisource' corpora)"

import os
import sys
from uuid import uuid4

import parapartition as para


def main(input_dir, output_dir):
    files = os.listdir(input_dir)
    all_paragraphs = set()
    for file in files:
        file_path = os.path.join(input_dir, file)
        paragraphs = [
            text for fn, line, text in para.split_into_paragraphs(file_path, "xml")
        ]
        all_paragraphs.update(paragraphs)
    os.makedirs(output_dir, exist_ok=True)
    for par in all_paragraphs:
        with open(os.path.join(output_dir, f"{uuid4()}"), "w", encoding="utf-8") as ptr:
            ptr.write(par)


if __name__ == "__main__":
    input_dir, output_dir = sys.argv[1:]
    main(input_dir, output_dir)
