from typing import Tuple


class FixTypoQuiz:

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

    init_text = '\n'.join(
        f'{key} = {repr(value)}'
        for key, value
        in local.items()
    )

    def __repr__(self, *args, **kwargs):
        return f'<Quiz: {self.name}>'

    def __call__(self, snippet: str) -> Tuple[int, str]:
        snippet = snippet.strip('\r\n ')
        if not snippet:
            return (-2, 'Input is empty')
        try:
            exec(snippet, {}, self.local)
            for j in (
                self.local['sentence'] == self.answer,
                '.replace' in snippet,
            ):
                if not j:
                    return (0, 'Wrong answer')
            return (1, 'Correct answer')
        except Exception as err:
            return (-1, err)
