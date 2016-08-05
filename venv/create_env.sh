#!/bin/bash -e

virtualenv env --python=python2.7;
source env/bin/activate && pip install --editable ../ray-core;
source env/bin/activate && pip install --editable ../ray-appengine;
# to fix the appengine bug
source env/bin/activate && pip install PyYAML
source env/bin/activate && pip install --editable ../ray-sqlalchemy;
source env/bin/activate && pip install --editable ../ray-peewee;

# to test enviroment
source env/bin/activate && pip install pytest;
