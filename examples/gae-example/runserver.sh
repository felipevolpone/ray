
rm -rf libs/*
pip install ../../ray-core/ -t libs/ --ignore-installed
pip install ../../ray-appengine/ -t libs/ --ignore-installed
dev_appserver.py .
