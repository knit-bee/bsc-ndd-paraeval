import configparser
import logging
import os
import sys
import time
from typing import Dict, List, Tuple, Union

import numpy as np
import scipy.sparse
from deduplication.candidate_ranker import CandidateRanker
from deduplication.candidate_searcher import CandidateSearcher
from deduplication.document_processing import DocumentProcessorImpl
from deduplication.minhashing import MinHasher
from deduplication.pipeline import NddPipeline
from deduplication.preprocessor import Preprocessor

logger = logging.getLogger()


def read_config(config_file: str) -> Dict[str, Dict[str, str]]:
    conf_parser = configparser.ConfigParser()
    conf_parser.read(config_file)
    config_dict = {}
    for sect in conf_parser.sections():
        config_dict[sect] = dict(conf_parser.items(sect))
    return convert_config_parameters(config_dict)


def convert_config_parameters(
    config_dict: Dict[str, Dict[str, str]]
) -> Dict[str, Dict[str, Union[bool, float, int]]]:
    expected_keys = {"preprocessor", "minhasher", "candidate_searcher"}
    parameter_types = {
        "int": ["num_perm", "shingle_size"],
        "float": ["lsh_threshold"],
        "bool": [
            "case_insensitive",
            "ignore_nums",
            "normalize_whitespace",
            "ignore_interpunctuation",
            "use_token",
        ],
    }
    for key, values in config_dict.items():
        if key not in expected_keys:
            print(f"Didn't expect {key} here.")
            continue
        for parameter, value in values.items():
            if parameter in parameter_types["int"]:
                try:
                    value = int(value)
                except ValueError:
                    value = -1
            elif parameter in parameter_types["float"]:
                try:
                    value = float(value)
                except ValueError:
                    value = -1
            elif parameter in parameter_types["bool"]:
                if value not in {"1", "0"}:
                    value = -1
                else:
                    value = bool(int(value))
            else:
                value = -1
            config_dict[key][parameter] = value

    return {
        key: {param: val for param, val in values.items() if val != -1}
        for key, values in config_dict.items()
    }


def get_document_index_mapping(doc_list: List[str]) -> Dict[str, int]:
    return {doc: i for i, doc in enumerate(sorted(doc_list))}


def set_up_ndd_pipeline(config_file: str) -> NddPipeline:
    config_dict = read_config(config_file)
    preprocessor = Preprocessor(**config_dict["preprocessor"])
    minhash = MinHasher(**config_dict["minhasher"])
    document_processor = DocumentProcessorImpl()
    candidate_searcher = CandidateSearcher(**config_dict["candidate_searcher"])
    candidate_ranker = CandidateRanker()
    pipeline = NddPipeline(
        document_processor, preprocessor, minhash, candidate_searcher, candidate_ranker
    )
    return pipeline


def run_deduplication(data_dir: str, config_file: str) -> None:
    pipeline = set_up_ndd_pipeline(config_file)
    start_preprocessing = time.time()
    pipeline.process_files(data_dir)
    end_preprocessing = time.time()
    nd_candidates = pipeline.find_near_duplicates()
    end_dedup = time.time()
    logger.info(f"{data_dir}, {config_file}")
    logger.info(f"Preprocessing time: {end_preprocessing-start_preprocessing} s")
    logger.info(f"Deduplication time: {end_dedup -end_preprocessing} s")

    results_dir = f"results_{os.path.basename(data_dir.rstrip(os.sep))}_{os.path.basename(config_file)}"
    os.makedirs(results_dir, exist_ok=True)
    build_similarity_matrix(nd_candidates, results_dir)
    return results_dir


def build_similarity_matrix(
    nd_candidates: Dict[str, List[Tuple[str, float]]], results_dir: str
) -> None:
    similarities = []
    doc_to_index_map = get_document_index_mapping(nd_candidates.keys())
    start_char = "0"
    start_index = 0
    output_file = os.path.join(results_dir, start_char)
    processed = 0
    for target_doc, i in doc_to_index_map.items():
        if not os.path.basename(target_doc).startswith(start_char):
            _save_results_to_file(f"{output_file}_{start_index}", similarities)
            similarities = []
            start_char = os.path.basename(target_doc)[0]
            output_file = os.path.join(results_dir, start_char)
            start_index = i
            processed = 0
        if processed >= 4100:  # split dataset part if too large
            _save_results_to_file(f"{output_file}_{start_index}", similarities)
            similarities = []
            start_index = i
            processed = 0
        candidates = nd_candidates[target_doc]
        doc_sim_vector = np.zeros((1, len(doc_to_index_map)))
        for doc, jacc_sim in candidates:
            insert_index = doc_to_index_map[doc]
            doc_sim_vector[0][insert_index] = jacc_sim
        # add 1 for similarity of doc with itself, because gold standard
        # has the same format
        doc_sim_vector[0][doc_to_index_map[target_doc]] = 1
        similarities.append(doc_sim_vector)
        processed += 1
    else:
        _save_results_to_file(f"{output_file}_{start_index}", similarities)


def _save_results_to_file(output_file, similarity_vectors) -> None:
    sparse_matrix = scipy.sparse.csc_matrix(np.vstack(similarity_vectors))
    scipy.sparse.save_npz(output_file, sparse_matrix)


if __name__ == "__main__":
    dataset, config_file = sys.argv[1:]
    run_deduplication(dataset, config_file)
