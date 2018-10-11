"""Package setup."""
from setuptools import setup, find_packages

import core

long_description = '吉.py 是一個幫助學習Python的小工具，題目按照Python的基本資\
料型態作為分類，使用者可以將不熟悉的題目收藏（點選右上角愛心圖示）， 讓日後複\
習更加方便。 如果妳/你覺得這個專案不錯，請在右上角幫我按顆星星，或是一起加入開\
發的行列，謝謝！'


setup(
    name='ji.py',
    author='amigcamel(阿吉/Aji)',
    author_email='amigcamel@gmail.com',
    version=core.__version__,
    url='https://github.com/amigcamel/ji.py',
    packages=find_packages(),
    description='吉.py 是一個幫助學習Python的小工具',
    long_description=long_description,
    install_requires=[],
    package_data={
        'core': ['data/*.json'],
    },
    entry_points={
        'console_scripts': ['ji.py = core.main:run_app']
    },
)
