
rm -rf libs/*
pip install ../../ray-core/ -t libs/ --ignore-installed
pip install ../../ray-appengine/ -t libs/ --ignore-installed
/usr/local/google_appengine/dev_appserver.py . 
