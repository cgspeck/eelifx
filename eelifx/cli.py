import click

from eelifx.config import display_config

@click.group()
def root():
    pass

@click.command()
def showdefaultconfig():
    display_config()

@click.option(
    '--config',
    default=None,
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True
    ),
    help='Path to optional config file with rules to load'
)
@click.command()
def grouptest(config=None):
    print('group test')

@click.option(
    '--config',
    default=None,
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True
    ),
    help='Path to optional config file with rules to load'
)
@click.argument(
    'endpoint'
)
@click.command()
def run(endpoint, config=None):
    print('running')


root.add_command(showdefaultconfig)
root.add_command(grouptest)
root.add_command(run)

if __name__ == '__main__':
    root()
