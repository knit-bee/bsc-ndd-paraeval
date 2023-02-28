import os
import sys

import numpy as np
import scipy.sparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def main(dataset_path: str, gold: str) -> None:
    file_names = sorted([file for file in os.listdir(dataset_path)])
    file_paths = [os.path.join(dataset_path, file) for file in file_names]

    vectorizer = TfidfVectorizer(
        input="filename",
        token_pattern=r"\w\w+|[^\w\s]+",
        ngram_range=(1, 2),
    )
    tf_idf_vectors = vectorizer.fit_transform(file_paths)
    os.makedirs(gold, exist_ok=True)
    with open(os.path.join(gold, "file_index.txt"), "w") as ptr:
        for i, file in enumerate(file_names):
            print(i, file, sep=",", file=ptr)
    cos_sim = []
    start_chars = [
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
    ]
    start_char = start_chars.pop(0)
    start_index = 0
    max_files = 4100
    num_files = 0
    for i, (vector, file) in enumerate(zip(tf_idf_vectors, file_paths)):
        if not os.path.basename(file).startswith(start_char):
            data = np.vstack(cos_sim)
            data = scipy.sparse.csc_matrix(data)
            scipy.sparse.save_npz(
                os.path.join(gold, f"{start_char}_{start_index}"), data
            )
            start_index += len(cos_sim)
            if start_chars:
                start_char = start_chars.pop(0)
            else:
                print("error")
                break
            cos_sim = []
            data = []
            num_files = 0
        if num_files >= max_files:
            data = np.vstack(cos_sim)
            data = scipy.sparse.csc_matrix(data)
            scipy.sparse.save_npz(
                os.path.join(gold, f"{start_char}_{start_index}"), data
            )
            start_index += len(cos_sim)
            cos_sim = []
            data = []
            num_files = 0
        vec = cosine_similarity(vector, tf_idf_vectors).astype(np.float32)
        cos_sim.append(vec)
        num_files += 1
    else:
        data = np.vstack(cos_sim)
        data = scipy.sparse.csc_matrix(data)
        scipy.sparse.save_npz(os.path.join(gold, f"{start_char}_{start_index}"), data)


if __name__ == "__main__":
    input_dir, gold = sys.argv[1:]
    main(input_dir, gold)
