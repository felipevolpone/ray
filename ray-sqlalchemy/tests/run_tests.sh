#!/bin/bash -xe

ray up --wsgifile app.py &
sleep 1
py.test test_integrated.py

ps auxx | grep uwsgi | cut -c10-14 | xargs kill -9

rm example.db
