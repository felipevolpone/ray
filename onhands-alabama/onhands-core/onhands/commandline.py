import click, os, sys

cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),'scripts'))


class OnHandsCLI(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py'):
                rv.append(filename[:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            mod = __import__('onhands.scripts.' + name,
                             None, None, ['onhands.commandline'])
        except ImportError:
            return
        return mod.cli


@click.command(cls=OnHandsCLI)
def interface():
    pass
