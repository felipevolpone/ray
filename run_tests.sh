# docker rm -f "onhands"
# docker run -i -t  -v "$(pwd):/home/onhands/" --rm=true --name "onhands" "onhands:latest" /home/onhands/tests/up.sh $1
#!/bin/bash

#service postgresql start
uwsgi --ini onhands/wsgi/dev.ini --pidfile dev_onhands.pid &
sleep 2
py.test tests/ $1
