
# ray-appengine

## How to use

### CLI scaffold
You can use this command to generate your app.yaml and appengine_config.py already configurated
to work with Ray.

```bash
ray new_gae_project # this will create the app.yaml and appengine_config files and a dir called libs
cd libs/
pip install ray -t . # this will download the ray library in this dir
pip install ray-appengine -t . # this will download the ray-appengine library in this dir
cd ..
```

Run the dev_server:
```bash
# in the same dir that has the app.yaml file
dev_appserver.py .
```

### How to run the tests

```bash
# at the ray-core directory
pip install --editable .

cd ../ray-sqlalchemy/
pip install --editable .

cd tests/
./run_tests.sh
```
