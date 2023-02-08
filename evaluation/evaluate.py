import logging
import os
import sys

import numpy as np
import numpy.typing as npt
import scipy.sparse
import sklearn.metrics as skm
import sklearn.utils as sku

logger = logging.getLogger()


def ndcg_score_adapted(y_true, y_score, k=None, ignore_ties=False):
    """
    Adapted implementation of scikit-learns ndcg_score function.
    Instead of returning averages as the original version, this
    version resturn a vector of scores.
    """
    # y_true = sku.check_array(y_true, ensure_2d=False)
    # y_score = sku.check_array(y_score, ensure_2d=False)
    # sku.check_consistent_length(y_true, y_score)
    skm._ranking._check_dcg_target_type(y_true)
    return skm._ranking._ndcg_sample_scores(
        y_true, y_score, k=k, ignore_ties=ignore_ties
    )


def compute_scores(gold_dir: str, scores_dir: str) -> npt.NDArray:
    all_ndcg_scores = []

    gold_files = sorted(
        [
            os.path.join(gold_dir, file)
            for file in os.listdir(gold_dir)
            if file.endswith(".npz")
        ]
    )
    result_files = sorted(
        [os.path.join(scores_dir, file) for file in os.listdir(scores_dir)]
    )
    assert len(gold_files) == len(result_files)

    for gold_file, result_files in zip(gold_files, result_files):
        gold_matrix = scipy.sparse.load_npz(gold_file).toarray().astype(np.float32)
        result_matrix = scipy.sparse.load_npz(result_files).toarray().astype(np.float32)
        scores = ndcg_score_adapted(gold_matrix, result_matrix, k=100)
        all_ndcg_scores.append(scores)
    return np.concatenate(all_ndcg_scores)


def dump_scores_to_file(scores: npt.NDArray, file: str) -> None:
    np.save(file, scores)


def compute_average_ndcg(scores: npt.NDArray) -> float:
    return np.average(scores)


def compare_with_gold(gold_dir: str, scores_dir: str) -> None:
    scores = compute_scores(gold_dir, scores_dir)
    file = f"ndcg_{scores_dir.rstrip(os.sep)}"
    dump_scores_to_file(scores, file)
    average = compute_average_ndcg(scores)
    logger.info("NDCG Average for %s : %f" % (scores_dir, average))


if __name__ == "__main__":
    gold_dir, scores_dir = sys.argv[1:]
    compare_with_gold(gold_dir, scores_dir)
