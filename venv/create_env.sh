#!/bin/bash -e

virtualenv env --python=python3;

source env/bin/activate && pip install --editable ../ray-core;
source env/bin/activate && pip install --editable ../ray-appengine;
source env/bin/activate && pip install --editable ../ray-peewee;

# to fix the appengine bug
source env/bin/activate && pip install PyYAML
source env/bin/activate && pip install --editable ../ray-sqlalchemy;

# to test enviroment
source env/bin/activate && pip install -r requirements_tests.txt;
