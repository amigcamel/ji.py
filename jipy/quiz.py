"""Quizzes."""
# -*- coding: utf-8 -*-
import os
import abc
import yaml
from typing import Tuple, List
from os.path import join, dirname, abspath


class Quiz(abc.ABC):
    """Base quiz class."""

    hint = None

    def __init__(self):
        """Copy presets to local variables for the use of exec."""
        self.local = self.presets.copy()
        if self.result_variable == 'ans':
            self.local['ans'] = None

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
    def presets(self):
        """Initial variables."""
        return {}

    @property
    @abc.abstractproperty
    def answer(self):
        """Quiz answer."""
        raise NotImplemented

    @property
    def _criteria(self) -> List[bool]:
        """Quiz criteria."""
        output = [f'self.local.get("{self.result_variable}") == self.answer']
        output.extend(getattr(self, 'criteria', []))
        return output

    @property
    def result_variable(self) -> str:
        """Result variable."""
        return 'ans'

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
            for c in self._criteria:
                if not eval(c):
                    return (0, 'Wrong approach or answer')
            return (1, 'Correct answer')
        except Exception as err:
            return (-1, err)


QUIZ_DICT = {}


def _collect_quizzes():
    """Dynamically collect class inherited from Quiz."""
    data_path = join(dirname(abspath(__file__)), 'data')
    for _, _, filenames in os.walk(data_path):
        for filename in filenames:
            if filename.endswith('.yml'):
                quiz_type = filename.replace('.yml', '').capitalize()
                QUIZ_DICT[quiz_type] = []
                with open(join(data_path, filename), encoding='utf-8') as f:
                    data = yaml.load(f)
                for class_name, settings in data.items():
                    QUIZ_DICT[quiz_type].append(
                        type(class_name, (Quiz, ), settings))


_collect_quizzes()
