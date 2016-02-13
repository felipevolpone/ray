
from setuptools import setup, find_packages

setup(
    name="onhands-sqlalchemy",
    version="0.0.1",
    author="Felipe Volpone",
    author_email="felipevolpone@gmail.com",
    #description=description(),
    license="MIT",
    keywords="python framework onhands api rest",
    url="http://github.com/felipevolpone/onhands",
    packages=find_packages(),
    install_requires=['sqlalchemy'],
    long_description="Check on github: http://github.com/felipevolpone/onhands",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
    ],
    entry_points='''
        [console_scripts]
        onhands=onhands.commandline:interface
    '''
)
