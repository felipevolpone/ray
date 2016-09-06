
from setuptools import setup, find_packages

setup(
    name="ray_sqlalchemy",
    version="0.0.1",
    author="Felipe Volpone",
    author_email="felipevolpone@gmail.com",
    license="MIT",
    keywords="python framework ray api rest",
    url="http://github.com/felipevolpone/ray",
    packages=find_packages(exclude=['tests']),
    install_requires=['sqlalchemy'],
    long_description="Check on github: http://github.com/felipevolpone/ray",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
    ],
)
