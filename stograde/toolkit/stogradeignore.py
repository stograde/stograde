import logging
from typing import List


def load_stogradeignore() -> List[str]:
    try:
        with open('.stogradeignore', encoding='utf-8') as infile:
            ignored_specs = [line.strip() for line in infile.read().splitlines()]
            logging.debug("Ignored specs: {}".format(ignored_specs))
    except FileNotFoundError:
        logging.debug("No .stogradeignore file found")
        return []
