from multiprocessing.managers import SyncManager

from .set_proxy import SetProxy

__version__ = '0.0.1a5'


SyncManager.register('set', set, SetProxy)
