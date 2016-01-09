#!/bin/bash

echo 'aqui'
service postgresql start
echo 'aqui'
uwsgi --ini onhands/wsgi/dev.ini --pidfile dev_onhands.pid &
echo 'aqui'
sleep 2
echo 'aqui'
py.test tests/ $1
