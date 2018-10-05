"""Quizzes."""
# -*- coding: utf-8 -*-
import abc
from typing import Tuple, List


class Quiz(abc.ABC):
    """Base quiz class."""

    hint = None

    def __init__(self):
        """Copy presets to local variables for the use of exec."""
        self.local = self.presets.copy()

    def __repr__(self, *args, **kwargs):  # noqa: D105
        return f'<Quiz: {self.name}>'

    @property
    @abc.abstractproperty
    def name(self):
        """Quiz name."""
        raise NotImplemented

    @property
    @abc.abstractproperty
    def description(self):
        """Quiz description."""
        raise NotImplemented

    @property
    @abc.abstractproperty
    def presets(self):
        """Initial variables."""
        raise NotImplemented

    @property
    @abc.abstractproperty
    def answer(self):
        """Quiz answer."""
        raise NotImplemented

    @property
    @abc.abstractproperty
    def criteria(self) -> List[bool]:
        """Quiz criteria."""
        raise NotImplemented

    @property
    def init_text(self):
        """Initial text displayed on window."""
        return '\n'.join(
            f'{key} = {repr(value)}'
            for key, value
            in self.local.items()
        )

    def __call__(self, snippet: str) -> Tuple[int, str]:
        """Run snippet."""
        snippet = snippet.strip('\r\n ')
        if not snippet:
            return (-2, 'Input is empty')
        try:
            exec(snippet, {}, self.local)
            for c in self.criteria:
                if not eval(c):
                    return (0, 'Wrong approach or answer')
            return (1, 'Correct answer')
        except Exception as err:
            return (-1, err)


class FixTypoQuiz(Quiz):  # noqa: D101

    name = 'Fix typo'
    description = (
        'sentence 裡面有一個錯字"Pyton"，'
        '請把它取代為"Python"'
    )
    hint = 'str.replace'

    presets = {
        'sentence': 'I love Pyton',
    }

    answer = 'I love Python'
    criteria = (
        "self.local['sentence'] == self.answer",
        "'.replace' in snippet",
    )


class DelListElementQuiz(Quiz):  # noqa: D101

    name = 'Delete list element'
    description = '刪除 "x" 之最後一個元素'
    hint = 'del'
    presets = {'x': ['a', 'b', 'c', 'd', 'x']}
    answer = ['a', 'b', 'c', 'd']
    criteria = (
        "self.local['x'] == self.answer",
    )
