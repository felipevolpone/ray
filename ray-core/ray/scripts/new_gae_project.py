import click
import os


@click.command()
def cli():
    f = click.open_file('app.yaml', 'w')
    f.write("""

application: app
runtime: python27
api_version: 1
threadsafe: yes

handlers:

- url: /api.*
  script: your_models_file.application

libraries:
- name: pycrypto
  version: "2.6"

""")
    f.close()

    f = click.open_file('appengine_config.py', 'w')
    f.write('''
"""This file is loaded when starting a new application instance."""

import sys, os

# add `lib` subdirectory to `sys.path`, so our `main` module can load
# third-party libraries.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'libs'))
''')
    f.close()

    os.system('mkdir libs;')
    
