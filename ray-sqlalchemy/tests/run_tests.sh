#!/bin/bash -xe

rm example.db || true
ps auxx | grep uwsgi | cut -c18-22 | xargs kill -9 || true

ray up --wsgifile app.py &
sleep 2
py.test test_integrated.py

rm example.db
rm *.pid

ps auxx | grep uwsgi | cut -c18-22 | xargs kill -9 || true
