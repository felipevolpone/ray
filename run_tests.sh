rm dev_onhands.pid || true
uwsgi --ini onhands/wsgi/dev.ini --pidfile dev_onhands.pid &

sleep 2

py.test tests/ $1

cat dev_onhands.pid | xargs kill -9
rm dev_onhands.pid