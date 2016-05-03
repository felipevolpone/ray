import click, os, sys

cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),
                             'scripts'))


class RayCLI(click.MultiCommand):

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
            mod = __import__('ray.scripts.' + name,
                             None, None, ['ray.commandline'])
        except ImportError:
            return
        return mod.cli


@click.command(cls=RayCLI)
def interface():
    """
        All command line are redirect to the name of the file inside the scripts directory. This means that
        the command: ray up, will call the scripts/up.py file.
    """
    pass
