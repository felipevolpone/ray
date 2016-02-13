#/bin/bash -xe

onhands up --wsgifile app.py &
sleep 1
py.test test_integrated.py

ps auxx | grep uwsgi | cut -c18-22 | xargs kill -9

rm example.db
