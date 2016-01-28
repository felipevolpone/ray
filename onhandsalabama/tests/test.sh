service postgresql start; onhands up --wsgifile app.py &; sleep 2; py.test test_integrated.py;
# call a python unit test that through urls call the api
# and checks if everything was saved
