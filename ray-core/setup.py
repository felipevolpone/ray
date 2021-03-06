from setuptools import setup, find_packages


def description():
    return """
    Ray is a framework that helps you to deliver
    well designed software without been stucked in your framework.
    Ray it's a ready to production framework that contains
    a uWSGI server that can be used in production as well.
    """

setup(
    name="ray_framework",
    version="0.2.0",
    author="Felipe Volpone",
    author_email="felipevolpone@gmail.com",
    description=description(),
    license="MIT",
    keywords="python framework ray api rest",
    url="http://github.com/felipevolpone/ray",
    packages=find_packages(exclude=['tests']),
    install_requires=['bottle', 'pycrypto', 'PyJWT', 'future'],
    long_description="Check on github: http://github.com/felipevolpone/ray",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
    ]
)
