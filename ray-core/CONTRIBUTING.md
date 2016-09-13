
# How to contribute to Ray

### Development

**How to run the tests**
```bash
cd ray-core  # or any other dir
py.test tests/
```

If you wanna check the test coverage
```bash
cd ray-core
nosetests --tests=tests --with-coverage --cover-package=ray
```

### Code style
Please, follow the PEP 8 style guide, but also, check the [pep8](https://github.com/felipevolpone/ray/blob/master/ray-core/.pep8) file, because some rules are not followed.
