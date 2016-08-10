
from setuptools import setup, find_packages

setup(
    name="ray-peewee",
    version="0.0.2",
    author="Felipe Volpone",
    author_email="felipevolpone@gmail.com",
    license="MIT",
    keywords="peewee framework ray api rest",
    url="http://github.com/felipevolpone/ray",
    packages=find_packages(exclude=['tests']),
    install_requires=['peewee'],
    long_description="Check on github: http://github.com/felipevolpone/ray",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
    ],
)
