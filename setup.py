from setuptools import setup, find_packages


setup(
    name='ji.py',
    author='amigcamel',
    author_email='amigcamel@gmail.com',
    version='0.0.0',
    url='https://github.com/amigcamel/ji.py',
    packages=find_packages(),
    description='只要有心,人人都是py神',
    long_description='...............',
    install_requires=[],
    entry_points={
        'console_scripts': ['ji.py = core.main:run_app']
    },
)
