import abc
from typing import Tuple


class Quiz(abc.ABC):

    hint = None

    def __repr__(self, *args, **kwargs):
        return f'<Quiz: {self.name}>'

    @property
    @abc.abstractproperty
    def name(self):
        raise NotImplemented

    @property
    @abc.abstractproperty
    def description(self):
        raise NotImplemented

    @property
    @abc.abstractproperty
    def local(self):
        raise NotImplemented

    @property
    @abc.abstractproperty
    def answer(self):
        raise NotImplemented

    @property
    def init_text(self):
        return '\n'.join(
            f'{key} = {repr(value)}'
            for key, value
            in self.local.items()
        )

    @abc.abstractmethod
    def judge(self):
        raise NotImplemented

    def __call__(self, snippet: str) -> Tuple[int, str]:
        snippet = snippet.strip('\r\n ')
        if not snippet:
            return (-2, 'Input is empty')
        try:
            exec(snippet, {}, self.local)
            if self.judge(snippet):
                return (1, 'Correct answer')
            else:
                return (0, 'Wrong approach or answer')
        except Exception as err:
            return (-1, err)


class FixTypoQuiz(Quiz):

    name = 'Fix typo'
    description = (
        'sentence 裡面有一個錯字"Pyton"，'
        '請把它修正為"Python"'
    )
    hint = 'str.replace'

    local = {
        'sentence': 'I love Pyton',
    }

    answer = 'I love Python'

    def judge(self, snippet) -> bool:
        for j in (
            self.local['sentence'] == self.answer,
            '.replace' in snippet,
        ):
            if not j:
                return False
        return True


class DelListElementPopQuiz(Quiz):

    name = 'Delete list element'
    description = '刪除 "x" 之最後一個元素'
    hint = 'del'
    local = {'x': ['a', 'b', 'c', 'd', 'x']}
    answer = ['a', 'b', 'c', 'd']

    def judge(self, snippet) -> bool:
        for j in (
            self.local['x'] = self.answer,
        ):
            if not j:
                return False
        return True
