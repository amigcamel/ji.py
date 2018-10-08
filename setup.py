"""Package setup."""
from setuptools import setup, find_packages


setup(
    name='ji.py',
    author='amigcamel(阿吉/Aji)',
    author_email='amigcamel@gmail.com',
    version='0.0.0',
    url='https://github.com/amigcamel/ji.py',
    packages=find_packages(),
    description='吉.py 是一個幫助學習Python的小工具',
    long_description='吉.py 是一個幫助學習Python的小工具',
    install_requires=[],
    package_data={
        'core': ['data/*.json'],
    },
    entry_points={
        'console_scripts': ['ji.py = core.main:run_app']
    },
)
