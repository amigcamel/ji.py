"""Test quizzes in data/*.json."""
import pytest

from core.quiz import collect_quizzes

quizzes = collect_quizzes()


@pytest.mark.parametrize('Q', quizzes)
def test_valid_quiz(Q):
    """Validate quiz."""
    assert Q()


@pytest.mark.parametrize('Q', quizzes)
def test_quiz_criteria(Q):
    """Test if criteria are correct."""
    status, _ = Q()('\n'.join(Q.test_code))
    assert status == 1
