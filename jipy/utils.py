# -*- coding: utf-8 -*-
"""Utilities."""
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
