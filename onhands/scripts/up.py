import click, os

@click.command()
@click.option('--ini', default="onhands/wsgi/dev.ini", help='uwsgi ini file')
@click.option('--pid', default='dev_onhands.pid', help='pid file')
              
def cli(ini, pid):
    to_run = 'uwsgi  --ini ' + ini + ' --pidfile ' + pid
    print to_run
    os.system(to_run)
