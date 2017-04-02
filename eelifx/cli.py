import logging

import click

from eelifx.config import display_config, setup_loop


def _call_loop(
    mode: str,
    endpoint: str=None,
    config=None,
    loglevel=None,
):
    if loglevel is None:
        loglevel = logging.INFO
    else:
        loglevel = getattr(logging, loglevel)

    setup_loop(
        mode,
        config=config,
        endpoint=endpoint,
        loglevel=loglevel
    )


@click.option(
    '--loglevel',
    default=None,
    help='E.g. "DEBUG" or "INFO"'
)
@click.group()
def root(loglevel=None):
    pass


@click.command()
def showconfig(loglevel=None):
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
@click.command(
    short_help='Execute each rule in succession.',
    help='A test cycle which exercises each rule for each group in succession, resetting lights to base prior to each test.'
)
def grouptest(config=None, loglevel=None):
    _call_loop(
        'grouptest',
        endpoint=None,
        config=config,
        loglevel=loglevel
    )


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
def run(endpoint, config=None, loglevel=None):
    print('running')


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
@click.command(help='Reset lights to base state.')
def reset(config=None, loglevel=None):
    _call_loop(
        'reset',
        endpoint=None,
        config=config,
        loglevel=loglevel
    )


root.add_command(showconfig)
root.add_command(grouptest)
root.add_command(run)
root.add_command(reset)

if __name__ == '__main__':
    root()
