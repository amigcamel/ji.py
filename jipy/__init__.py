from multiprocessing.managers import SyncManager

from .multiprocessing_extras import SetProxy

__version__ = '0.0.1a5'


SyncManager.register('set', set, SetProxy)
