import click, os


@click.command()
@click.option('--ini', default=None, help='uwsgi ini file')
@click.option('--pid', default='dev_ray.pid', help='pid file')
@click.option('--wsgifile', help='the wsgi.py file that starts application')
def cli(ini, pid, wsgifile=None):
    if not wsgifile:
        raise Exception('you have to provide the path o wsgi.py file')
    to_run = 'uwsgi --http=0.0.0.0:8080 --wsgi-file=' + wsgifile + ' --threads=2 --py-autoreload=1 --pidfile=' + pid
    if ini:
        to_run = 'uwsgi  --ini ' + ini + ' --pidfile ' + pid

    os.system(to_run)
