"""Test quizzes in data/*.yml."""
from itertools import chain
from os.path import join, dirname, abspath
import os
import yaml

import pytest

from jipy.quiz import QUIZ_DICT

quizzes = list(chain.from_iterable(QUIZ_DICT.values()))


def test_duplicate_keys():
    """Test if yaml object contains duplicate keys."""
    def map_constructor(loader, node, deep=False):
        """Walk over the mapping and detect duplicate keys.

        reference: https://stackoverflow.com/a/48460700
        """
        mapping = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            value = loader.construct_object(value_node, deep=deep)
            if key in mapping:
                raise Exception(f'Duplicate key found: {key}')
            mapping[key] = value
        return mapping

    loader = type('_', (yaml.loader.Loader, ), {})
    loader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, map_constructor)
    data_path = join(dirname(dirname(abspath(__file__))), 'jipy', 'data')
    for _, _, filenames in os.walk(data_path):
        for filename in filenames:
            if filename.endswith('.yml'):
                with open(join(data_path, filename), encoding='utf-8') as f:
                    yaml.load(f, loader)
                    assert True


@pytest.mark.parametrize('Q', quizzes)
def test_valid_quiz(Q):
    """Validate quiz."""
    assert Q()


@pytest.mark.parametrize('Q', quizzes)
def test_quiz_criteria(Q):
    """Test if criteria are correct."""
    status, _ = Q()(Q.test_code)
    assert status == 1
