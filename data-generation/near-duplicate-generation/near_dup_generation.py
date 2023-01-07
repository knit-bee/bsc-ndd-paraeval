"Create near duplicate files for dataset"

import configparser
import os
import random
import shutil
import sys
from uuid import uuid4
from typing import List

import numpy as np
import augtxt.order
from augtxt.augmenters import sentaugm


class TextAugmenter:
    typo_settings = [
        {
            "weight": 2,
            "fn": "typo.drop_n_next_twice",
            "args": {"loc": "u", "keep_case": True},
        },
        {
            "weight": 2,
            "fn": "typo.swap_consecutive",
            "args": {"loc": "u", "keep_case": True},
        },
        {
            "weight": 1,
            "fn": "typo.pressed_twice",
            "args": {"loc": "u", "keep_case": True},
        },
        {
            "weight": 1,
            "fn": "typo.drop_char",
            "args": {"loc": "u", "keep_case": True},
        },
    ]

    def __init__(
        self,
        word_list: List[str],
        input_dir: str,
        output_dir: str,
        max_length: str,
        average: str,
    ) -> None:
        self.word_list = word_list
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.max_length = int(max_length)
        self.average = int(average)

    def file_processed(self, file: str) -> bool:
        file_path = os.path.join(self.input_dir, file)
        with open(file_path, "r") as ptr:
            content = ptr.read()
        if self._check_content_length(content):
            augmented = self.apply_augmentations(content)
            for augm_version in augmented:
                self._save_augmentation(augm_version)
            self.copy_original_file(file_path)
            return True
        return False

    def _save_augmentation(self, augmentation: str) -> None:
        with open(
            os.path.join(self.output_dir, f"{uuid4()}"), "w", encoding="utf-8"
        ) as ptr:
            ptr.write(augmentation)

    def _check_content_length(self, content: str) -> bool:
        if 20 > len(content) or len(content) > self.max_length:
            return False
        return True

    def apply_augmentations(self, file_content: str) -> List[str]:
        augmentations = []
        augmentations.extend(self.token_swap(file_content))
        augmentations.extend(self.typo_augmentation(file_content))
        augmentations.extend(self.insert_random_words(file_content))
        return augmentations

    def typo_augmentation(self, file_content: str) -> List[str]:
        """Produce three augmented versions of the original with typos."""
        return sentaugm(
            file_content,
            settings={
                "typo": {
                    "num_augmentations": 3,
                    "settings": self.typo_settings,
                    "pmax": 0.1,
                },
            },
        )

    def token_swap(self, file_content: str) -> List[str]:
        """
        Produce three augmented version of the original with token swaps.
        The number of swaps depends on the length of the input.
        """
        return [
            augtxt.order.swap_consecutive(
                file_content,
                num_aug=min(max(i * (len(file_content) // self.average), 30), 1),
            )
            for i in range(1, 4)
        ]

    def insert_random_words(self, file_content: str) -> List[str]:
        tokenized = file_content.split()
        augmented = []
        for i in range(1, 5):
            for _ in range(0, len(file_content), self.average):
                rand_index = random.randint(0, len(tokenized) - 1)
                rand_word = random.choice(self.word_list)
                tokenized[rand_index] = rand_word
            augmented.append(" ".join(tokenized))
        return augmented

    def copy_original_file(self, file_path: str) -> None:
        shutil.copy(file_path, self.output_dir)


def read_config(cfg_file: str, dataset_name: str):
    config = configparser.ConfigParser()
    config.read(cfg_file)
    return config[dataset_name]


def main(config_file: str, dataset: str) -> None:
    with open("wordlist-german.txt") as ptr:
        wordlist = [line.strip() for line in ptr]

    config = read_config(config_file, dataset)
    augmenter = TextAugmenter(wordlist, **config)
    np.random.seed(42)
    random.seed(42)
    all_files = sorted(os.listdir(augmenter.input_dir))
    os.makedirs(augmenter.output_dir, exist_ok=True)
    count = 0
    for file in all_files:
        if count >= 10000:
            break
        if augmenter.file_processed(file):
            count += 1
    print(count)


if __name__ == "__main__":
    cfg_file, dataset = sys.argv[1:]
    main(cfg_file, dataset)
