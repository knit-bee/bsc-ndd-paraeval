import logging
import os
import sys

from run_deduplication import run_deduplication
from evaluate import compare_with_gold


logging.basicConfig(
    filename="dedup.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s: %(message)s",
)


def main(dataset, config_dir, gold):
    logger = logging.getLogger()
    logger.info("Processing dataset %s" % dataset)
    for file in os.listdir(config_dir):
        results_dir = run_deduplication(dataset, os.path.join(config_dir, file))
        compare_with_gold(gold, results_dir)


if __name__ == "__main__":
    dataset, config_dir, gold = sys.argv[1:]
    main(dataset, config_dir, gold)
