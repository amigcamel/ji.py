"""Test jipa.main."""
# -*- coding: utf-8 -*-
from tkinter import Tk, END, messagebox
from itertools import chain

from jipy.main import Window
from jipy.quiz import QUIZ_DICT
root = Tk()
window = Window(root)


def test_quizzes_amount():
    """Test quizzes amount."""
    assert len(window.quizzes) == len(
        list(chain.from_iterable(QUIZ_DICT.values())))


def test_chanllenge_status():
    """Test chanllenge status."""
    left = window.total_quiz_num - len(window.quizzes)
    assert (window.chanllenge_status ==
            f'已完成練習題數: {left}/{window.total_quiz_num}')


def test_skip():
    """Test skip function."""
    quizzes = window.quizzes.copy()
    window.skip()
    assert (quizzes[1:] + quizzes[:1]) == window.quizzes


def test_reset(monkeypatch):
    """Test reset functino."""
    test_sentence = '# this is a sentence'
    window.snippet.insert(END, test_sentence)
    # test is NO
    monkeypatch.setattr(messagebox, 'askquestion', lambda *args, **kw: 'no')
    assert (test_sentence in window.snippet.get('1.0', END))
    window.reset()

    # test if YES
    monkeypatch.setattr(messagebox, 'askquestion', lambda *args, **kw: 'yes')
    window.reset()
    assert (test_sentence not in window.snippet.get('1.0', END))
