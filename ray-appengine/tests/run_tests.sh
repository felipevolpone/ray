#!/bin/bash -xe

ps auxx | grep uwsgi | cut -c18-22 | xargs kill -9 || true

# ray up --wsgifile app.py &
dev_appserver.py .
sleep 2
py.test test_integrated.py


ps auxx | grep uwsgi | cut -c18-22 | xargs kill -9 || true
