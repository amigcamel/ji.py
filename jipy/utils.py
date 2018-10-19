# -*- coding: utf-8 -*-
"""Utilities."""
from multiprocessing.managers import MakeProxyType, SyncManager
from typing import Optional
from urllib.request import urlopen
import json

from . import __version__


def check_latest_version() -> Optional[str]:
    """Check latest version."""
    url = 'https://pypi.org/pypi/ji.py/json'
    try:
        resp = urlopen(url, timeout=5)
        raw = resp.read()
        data = json.loads(raw)
        releases = list(data['releases'].keys())
        latest_version = releases[-1]
        if __version__ != latest_version:
            return latest_version
    except Exception as e:
        print('無法檢查更新')
        print(e)


BaseSetProxy = MakeProxyType('BaseSetProxy', ('__and__', '__contains__', '__iand__', '__ior__', '__isub__', '__ixor__', '__len__', '__or__', '__rand__', '__ror__', '__rsub__', '__rxor__', '__sub__', '__xor__', 'add', 'clear', 'copy', 'difference', 'difference_update', 'discard', 'intersection', 'intersection_update', 'isdisjoint', 'issubset', 'issuperset', 'pop', 'remove', 'symmetric_difference', 'symmetric_difference_update', 'union', 'update'))


class SetProxy(BaseSetProxy):  # noqa: D101
    """Using sets with the multiprocessing module.

    reference: https://stackoverflow.com/a/16415356
    """

    def __iter__(self):  # noqa: D105
        _set = self.copy()
        while len(_set) > 0:
            yield _set.pop()

    def __iand__(self, value):  # noqa: D105
        self._callmethod('__iand__', (value,))
        return self

    def __ior__(self, value):  # noqa: D105
        self._callmethod('__ior__', (value,))
        return self

    def __isub__(self, value):  # noqa: D105
        self._callmethod('__isub__', (value,))
        return self

    def __ixor__(self, value):  # noqa: D105
        self._callmethod('__ixor__', (value,))
        return self


SyncManager.register('set', set, SetProxy)
