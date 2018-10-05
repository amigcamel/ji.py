"""Test quizzes in data/*.json."""
import pytest

from core.quiz import collect_quizzes


@pytest.mark.parametrize('Q', collect_quizzes())
def test_valid_quiz(Q):
    """Validate quiz."""
    assert Q()
