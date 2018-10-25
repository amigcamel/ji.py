"""Quizzes."""
# -*- coding: utf-8 -*-
import os
import abc
import yaml
from typing import Tuple, List
from os.path import join, dirname, abspath
from multiprocessing import Manager

from .multiprocessing_extras import PatchedProcess


class Quiz(abc.ABC):
    """Base quiz class."""

    hint = None

    def __init__(self):
        """Copy presets to local variables for the use of exec."""
        manager = Manager()
        # As the snippet is executing in multiprocessing.Process, a shared
        # dict should be used to ensure the change is propagated.
        self.local = manager.dict()

        # the object in shared dict should also be shared
        for k, v in self.presets.items():
            if isinstance(v, list):
                self.local[k] = manager.list(v)
            elif isinstance(v, dict):
                self.local[k] = manager.dict(v)
            elif isinstance(v, set):
                self.local[k] = manager.set(v)
            else:
                self.local[k] = v

    def __repr__(self, *args, **kwargs):  # noqa: D105
        return f'<{self.__class__.__name__}: {self.name}>'

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
        output = [
            f'type(self.answer).__call__(\
            self.local.get("{self.result_variable}")) == self.answer'
        ]
        output.extend(getattr(self, 'criteria', []))
        return output

    @property
    def result_variable(self) -> str:
        """Result variable."""
        return 'ans'

    @property
    def init_text(self):
        """Initial text displayed on window."""
        text = ''
        for key, value in self.local.items():
            if value.__class__.__name__ == 'ListProxy':
                value = repr(list(value))
            elif value.__class__.__name__ == 'DictProxy':
                value = repr(dict(value))
            elif value.__class__.__name__ == 'SetProxy':
                value = repr(dict(value))
            else:
                value = repr(value)
            text += f'{key} = {value}\n'
        if text:
            intro_text = '# 預設變數\n'
        else:
            intro_text = '# 本題無預設變數\n'
        text = intro_text + text
        return text

    def __call__(self, snippet: str) -> Tuple[int, str]:
        """Run snippet."""
        snippet = snippet.strip('\r\n ')
        if not snippet:
            return (-2, 'Input is empty')
        try:
            p = PatchedProcess(target=exec, args=(snippet, {}, self.local))
            p.start()
            p.join(5)
            if p.is_alive():
                print('Process took too long, killed.')
                return (-3, 'Timeout')
            if p.exception:
                error, traceback = p.exception
                return (-1, error)
            for c in self._criteria:
                if not eval(c):
                    return (0, 'Wrong approach or answer')
            return (1, 'Correct answer')
        except Exception as err:
            return (-1, err)
        finally:
            p.terminate()
            # TODO: calling `close` leads pytest fail on some tests
            # p.close()
            p.join()


QUIZ_DICT = {}
QUIZ_DICT_FLAT = {}


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
                    Q = type(class_name, (Quiz, ), settings)
                    QUIZ_DICT[quiz_type].append(Q)
                    QUIZ_DICT_FLAT[class_name] = Q


_collect_quizzes()
