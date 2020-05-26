#! /usr/bin/env python

import collections

from autocomplete.core.trie import Trie

import autocomplete.core.loadArtifacts as loadArtifacts


class TestTrie:

    def test_add_word_search_word(self):
        trie = Trie()
        trie.add_word("Apple")
        trie.add_word("Bat")
        assert trie.search_word("Apple")
        assert trie.search_word("Bat")

    def test_add_word_remove_word(self):
        trie = Trie()
        trie.add_word("Apple")
        trie.remove_word("Apple")
        assert not trie.search_word("Apple")

    def test_add_two_words_remove_word(self):
        trie = Trie()
        trie.add_word("Apple")
        trie.add_word("Bat")

        assert trie.search_word("Apple")
        trie.remove_word("Apple")

        assert not trie.search_word("Apple")
        assert trie.search_word("Bat")

    def test_add_overlapping_words_remove_short_word(self):
        trie = Trie()
        short_word = "Apple"
        long_word = "Applebees"

        trie.add_word(short_word)
        trie.add_word(long_word)

        assert trie.search_word(short_word)
        assert trie.search_word(long_word)

        trie.remove_word(short_word)
        assert not trie.search_word(short_word)
        assert trie.search_word(long_word)

    def test_add_overlapping_words_remove_long_word(self):
        trie = Trie()
        short_word = "Apple"
        long_word = "Applebees"
        trie.add_word(short_word)
        trie.add_word(long_word)

        assert trie.search_word(short_word)
        assert trie.search_word(long_word)

        trie.remove_word(long_word)
        assert not trie.search_word(long_word)
        assert trie.search_word(short_word)

    def test_is_word_false_missing_word(self):
        trie = Trie()
        missing_word = "cat"
        assert not trie.search_word(missing_word)

    def test_case_insensitive_search(self):
        trie = Trie()
        word = "apple"
        trie.add_word(word)
        assert trie.search_word(word.title())
        assert trie.search_word(word.upper())
        assert trie.search_word(word.lower())

    def test_case_sensitive_search(self):
        trie = Trie(is_case_sensitive=True)
        word = "Apple"
        trie.add_word(word)
        assert not trie.search_word(word.upper())
        assert not trie.search_word(word.lower())

    def test_load_file_contents(self):
        trie = Trie()
        for fname in loadArtifacts.get_dictionary_test_files():
            trie.load_file_contents(fname)

        assert trie.search_word("aardvarks")

    def test_search_phrase(self):
        max_results_count = 5
        trie = Trie()
        initial_word_list = [
            "app",
            "apple",
            "applet",
            "application",
            "appetite"
        ]
        [trie.add_word(word) for word in initial_word_list]
        assert collections.Counter(trie.search_phrase("ap", max_len_closest_words=max_results_count)) == collections.Counter(initial_word_list)

    def test_search_phrase_max(self):
        trie = Trie()
        initial_word_list = [
            "app",
            "apple",
            "applet",
            "application",
            "appetite"
        ]
        [trie.add_word(word) for word in initial_word_list]
        
        max_results_count = 2
        result = trie.search_phrase(initial_word_list[0], max_len_closest_words=max_results_count)

        assert len(result)==max_results_count
        assert all(word in initial_word_list for word in result)

    def test_invalid_phrase(self):
        invalid_phrase = "apa"
        trie = Trie()
        initial_word_list = [
            "app",
            "apple",
            "applet",
            "application",
            "appetite"
        ]
        [trie.add_word(word) for word in initial_word_list]
        
        max_results_count = 2
        result = trie.search_phrase(invalid_phrase, max_len_closest_words=max_results_count)

        assert len(result)==0

    def test_is_empty(self):
        trie = Trie()
        assert trie.is_empty()

    def test_is_not_empty(self):
        trie = Trie()
        trie.add_word("test")

        assert not trie.is_empty()

    def test_remove_non_existent_word(self):
        trie = Trie()
        non_existent_word = "abcd"
        trie.add_word("app")
        assert not trie.remove_word(non_existent_word)

    def test_remove_not_a_word(self):
        trie = Trie()
        word = "application"
        not_a_word = "app"
        trie.add_word(word)

        assert not trie.remove_word(not_a_word)
