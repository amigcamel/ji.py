"""Tests for quiz."""
from jipy.quiz import Quiz

import pytest


def test_abc():
    """Test Base class Quiz."""
    with pytest.raises(TypeError) as e:
        class TestQuiz(Quiz):
            pass
        TestQuiz()
    message = (
        "Can't instantiate abstract class TestQuiz with abstract methods "
        'answer, description, name'  # sorted alphabetically
    )
    assert e.value.args[0] == message
