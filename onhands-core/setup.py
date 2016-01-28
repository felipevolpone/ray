from setuptools import setup


def description():
    return """
    Python on Hands is a framework that helps you to deliver
    well designed software without been stucked in your framework.
    On Hands it's a ready to production framework that contains
    a uWSGI server that can be used in production as well.
    """

setup(
    name="OnHands",
    version="0.0.1",
    author="Felipe Volpone",
    author_email="felipevolpone@gmail.com",
    description=description(),
    license="MIT",
    keywords="python framework onhands api rest",
    url="http://github.com/felipevolpone/onhands",
    packages=['onhands'],
    install_requires=['webapp2', 'webob', 'click', 'uwsgi'],
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
