import click, os


@click.command()
@click.option('--env', help='the virtualenv dir')
@click.option('--wsgifile', help='the wsgi.py file that starts application')
def cli(env, wsgifile):

    if not wsgifile:
        raise Exception('you have to provide the path of the wsgi file that has the application')

    to_run = 'uwsgi --http=0.0.0.0:8080 --wsgi-file=' + wsgifile

    if env:
        to_run += ' -H=' + env

    os.system(to_run)
