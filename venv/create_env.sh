#!/bin/bash -e

virtualenv env_$1 --python=$1;

source env_$1/bin/activate && pip install --editable ../ray-core;
source env_$1/bin/activate && pip install --editable ../ray-appengine;
source env_$1/bin/activate && pip install --editable ../ray-peewee;

# to fix the appengine bug
source env_$1/bin/activate && pip install PyYAML
source env_$1/bin/activate && pip install --editable ../ray-sqlalchemy;

# to test enviroment
source env_$1/bin/activate && pip install -r requirements_tests.txt;
