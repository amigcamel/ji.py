from multiprocessing.managers import SyncManager

from .multiprocessing_extras import SetProxy

__version__ = '0.0.1a8'


SyncManager.register('set', set, SetProxy)
