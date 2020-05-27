#! /usr/bin/env python

import logging

from abc import ABC, abstractmethod

from core.trie import Trie
from core.loadArtifacts import get_dictionary_files


class Db(ABC):

    def __init__(self, db_object=None):
        self.db = db_object
        self.logger = logging.getLogger(__name__)

    @abstractmethod
    def get(self, query):
        pass


class TrieDb(Db):

    def __init__(self, db=Trie()):
        super().__init__()
        self.db = db
        self.build()

    def build(self):
        raw_word_files = get_dictionary_files()
        for raw_file in raw_word_files:
            self.db.load_file_contents(raw_file)

    def get(self, word):
        self.logger.debug(f"Incoming word: {word}")
        return self.db.search_phrase(word)
