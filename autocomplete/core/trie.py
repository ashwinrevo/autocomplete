#! /usr/bin/env python

import os
import logging
import collections

from typing import Dict, List


class TrieNode:

    def __init__(self):
        self.children: Dict[str, TrieNode] = {}
        self.is_word: bool = False


class Trie:

    def __init__(self, is_case_sensitive=False):
        self.root: TrieNode = TrieNode()
        self.is_case_sensitive: bool = is_case_sensitive
        self.logger = logging.getLogger(__name__)

    def is_empty(self):
        if not self.root.children:
            return True
        return False

    def load_file_contents(self, file_name: str) -> None:
        with open(file_name, 'r') as fread:
            for line in fread:
                word = line.strip()
                self.add_word(word)

    def search_phrase(self, phrase: str, max_len_closest_words=5) -> List:
        """Returns up to max_len_closest_words closest words given a phrase"""
        phrase = self._sanitize_word(phrase)
        status, current_trie_node = self._traverse_trie(phrase)

        if not status:
            return []

        closest_words = []
        queue = collections.deque([(current_trie_node, phrase)])

        while queue:
            current_trie_node, word_so_far = queue.popleft()

            if current_trie_node.is_word:
                closest_words.append(word_so_far)
                if len(closest_words) == max_len_closest_words:
                    break

            for new_char, child_trie_node in current_trie_node.children.items():
                queue.append((child_trie_node, word_so_far + new_char))

        return closest_words

    def search_word(self, word) -> bool:
        """Returns bool value indicating word is present in dictionary"""
        word = self._sanitize_word(word)
        status, current_trie_node = self._traverse_trie(word)
        return status and current_trie_node and current_trie_node.is_word
        
    def add_word(self, new_word) -> bool:
        """Add a word back in to the trie. Sets is_word=True in the end to indicate valid word"""

        new_word = self._sanitize_word(new_word)

        current_trie_node = self.root
        for char in new_word:
            if char not in current_trie_node.children:
                new_trie_node = TrieNode()
                current_trie_node.children[char] = new_trie_node
            current_trie_node = current_trie_node.children[char]
        
        current_trie_node.is_word = True
        return True

    def remove_word(self, remove_word):
        """Remove word from trie. Additionally deletes the TrieNode if no other valid word ending goes down the same path"""
        remove_word = self._sanitize_word(remove_word)
        
        trie_node_iteration_stack = []
        status, current_trie_node = self._traverse_trie(remove_word, maintain_stack=True, trie_node_iteration_stack=trie_node_iteration_stack)
        if not status:
            return False

        if not current_trie_node.is_word:
            return False

        current_trie_node.is_word = False
        while (not current_trie_node.children and 
               current_trie_node is not self.root and
               not current_trie_node.is_word):
            current_char, previous_trie_node = trie_node_iteration_stack.pop()
            previous_trie_node.children[current_char] = None
            del previous_trie_node.children[current_char]
            current_trie_node = previous_trie_node

        return True

####  HELPER FUNCTIONS  ####

    def _sanitize_word(self, word: str) -> str:
        word = word.strip()
        return word if self.is_case_sensitive else word.lower()

    def _traverse_trie(self, word: str, maintain_stack:bool=False, trie_node_iteration_stack=None):
        current_trie_node = self.root
        
        if maintain_stack:
            assert isinstance(trie_node_iteration_stack, list) 
    
        for char in word:
            if char not in current_trie_node.children:
                return False, None

            if maintain_stack:
                trie_node_iteration_stack.append((char, current_trie_node))
    
            current_trie_node = current_trie_node.children[char]

        return True, current_trie_node
