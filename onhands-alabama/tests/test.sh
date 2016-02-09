sudo pip install --editable onhands-core
sudo pip install --editable ../
sudo service postgresql start
python -m populate
onhands up --wsgifile app.py &
sleep 2
py.test test_integrated.py
