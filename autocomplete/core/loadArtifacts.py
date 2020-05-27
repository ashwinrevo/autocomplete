#! /usr/bin/env python

import os


def get_artifact_directory() -> str:
    current_dir = os.getcwd()
    artifacts_dir = [
        os.path.join(current_dir, "artifacts"),
        os.path.join(current_dir, "../..", "artifacts")
    ]
    artifacts_dir = list(filter(os.path.isdir, artifacts_dir))
    if artifacts_dir:
        return artifacts_dir[0]
    return FileNotFoundError("Can't locate artifacts directory")


def get_dictionary_files():
    artifact_directory = get_artifact_directory()
    artifact_files = os.listdir(artifact_directory)
    ignore_files = [".DS_Store"]
    for fname in artifact_files:
        if fname not in ignore_files:
            yield os.path.join(artifact_directory, fname)


def get_dictionary_test_files():
    test_file_names = ['words_alpha_test.txt']
    artifact_directory = get_artifact_directory()

    test_files_with_dir = list(map(lambda fname:
                                   os.path.join(artifact_directory, fname),
                                   test_file_names))
    for fname in get_dictionary_files():
        if fname in test_files_with_dir:
            yield fname
