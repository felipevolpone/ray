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

- url: /st/
  static_dir: web

- url: /user.*
  script: src.service.login_service.app

- url: /event/(\d+)/schedule.*
  script: src.service.schedule_service.app

- url: /speaker.*
  script: src.service.speaker_service.app

- url: /talk.*
  script: src.service.talk_service.app

libraries:
- name: pycrypto
  version: "2.6"

- name: ssl
  version: latest
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
