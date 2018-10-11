"""Test quizzes in data/*.json."""
from itertools import chain
from os.path import join, dirname, abspath
import os
import json

import pytest

from jipy.quiz import QUIZ_DICT

quizzes = list(chain.from_iterable(QUIZ_DICT.values()))


def dict_raise_on_duplicates(ordered_pairs):
    """Reject duplicate keys."""
    d = {}
    for k, v in ordered_pairs:
        if k in d:
            raise ValueError("duplicate key: %r" % (k,))
        else:
            d[k] = v
    return d


def test_duplicate_keys():
    """Test if json object contains duplicate keys."""
    data_path = join(dirname(dirname(abspath(__file__))), 'jipy', 'data')
    for _, _, filenames in os.walk(data_path):
        for filename in filenames:
            if filename.endswith('.json'):
                with open(join(data_path, filename), encoding='utf-8') as f:
                    json.load(f, object_pairs_hook=dict_raise_on_duplicates)
                    assert True


@pytest.mark.parametrize('Q', quizzes)
def test_valid_quiz(Q):
    """Validate quiz."""
    assert Q()


@pytest.mark.parametrize('Q', quizzes)
def test_quiz_criteria(Q):
    """Test if criteria are correct."""
    status, _ = Q()('\n'.join(Q.test_code))
    assert status == 1
