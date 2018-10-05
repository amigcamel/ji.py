from core.quiz import Quiz

import pytest


def test_abc():
    with pytest.raises(TypeError) as e:
        class TestQuiz(Quiz):
            pass
        TestQuiz()
    message = (
        "Can't instantiate abstract class TestQuiz with abstract methods "
        'answer, description, judge, name, presets'  # sorted alphabetically
    )
    assert e.value.args[0] == message
