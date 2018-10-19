"""Implement multiprocessing `set` proxy."""
from multiprocessing.managers import MakeProxyType
from multiprocessing import Process, Pipe
import traceback


BaseSetProxy = MakeProxyType('BaseSetProxy', (
    '__and__', '__contains__', '__iand__', '__ior__', '__isub__', '__ixor__',
    '__len__', '__or__', '__rand__', '__ror__', '__rsub__', '__rxor__',
    '__sub__', '__xor__', 'add', 'clear', 'copy', 'difference',
    'difference_update', 'discard', 'intersection', 'intersection_update',
    'isdisjoint', 'issubset', 'issuperset', 'pop', 'remove',
    'symmetric_difference', 'symmetric_difference_update', 'union', 'update')
)


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


class PatchedProcess(Process):
    """Add feature: handling Child Errors in Parent.

    reference: https://stackoverflow.com/a/33599967/1105489
    """

    def __init__(self, *args, **kwargs):  # noqa: D107
        super().__init__(*args, **kwargs)
        self._pconn, self._cconn = Pipe()
        self._exception = None

    def run(self):  # noqa: D102
        try:
            Process.run(self)
            self._cconn.send(None)
        except Exception as e:
            tb = traceback.format_exc()
            self._cconn.send((e, tb))

    @property
    def exception(self):  # noqa: D102
        if self._pconn.poll():
            self._exception = self._pconn.recv()
        return self._exception
