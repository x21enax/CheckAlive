from setuptools import setup, find_packages

setup(
    name='checkalive',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'checkalive=checkalive.checkalive:main',
        ],
    },
)
