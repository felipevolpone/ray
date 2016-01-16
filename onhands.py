import click, os

@click.command('server')
@click.option('--ini', default="onhands/wsgi/dev.ini", help='uwsgi ini file')
@click.option('--pid', default='dev_onhands.pid', help='pid file')
              
def up(ini, pid):
    to_run = 'uwsgi  --ini ' + ini + ' --pidfile ' + pid
    print to_run
    os.system(to_run)

if __name__ == '__main__':
    up()