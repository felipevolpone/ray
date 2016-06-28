#!/bin/bash -e

virtualenv env --python=python2;
source env/bin/activate && pip install --editable ../ray-core;
source env/bin/activate && pip install --editable ../ray-appengine;
source env/bin/activate && pip install --editable ../ray-sqlalchemy;

# to test enviroment
source env/bin/activate && pip install pytest;
