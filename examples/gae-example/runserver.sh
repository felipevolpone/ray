
rm -rf libs/*
pip install ../../ray-core/ -t libs/ --ignore-installed
pip install ../../ray-appengine/ -t libs/ --ignore-installed

cd libs
rm -rf ray*
ln -s ../../../ray-core/ray/ ray
ln -s ../../../ray-appengine/ray_appengine ray_appengine

/usr/local/google_appengine/dev_appserver.py . 
