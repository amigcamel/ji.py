"""Test quizzes in data/*.json."""
from itertools import chain

import pytest

from jipy.quiz import QUIZ_DICT

quizzes = list(chain.from_iterable(QUIZ_DICT.values()))


@pytest.mark.parametrize('Q', quizzes)
def test_valid_quiz(Q):
    """Validate quiz."""
    assert Q()


@pytest.mark.parametrize('Q', quizzes)
def test_quiz_criteria(Q):
    """Test if criteria are correct."""
    status, _ = Q()('\n'.join(Q.test_code))
    assert status == 1
