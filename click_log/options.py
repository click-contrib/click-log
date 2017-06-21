import logging

import click

from .core import set_level, set_logfile


def simple_verbosity_option(*names, **kwargs):
    '''A decorator that adds a `--verbosity, -v` option to the decorated
    command.

    Name can be configured through ``*names``. Keyword arguments are passed to
    the underlying ``click.option`` decorator.
    '''

    if not names:
        names = ['--verbosity', '-v']

    kwargs.setdefault('default', 'INFO')
    kwargs.setdefault('metavar', 'LVL')
    kwargs.setdefault('expose_value', False)
    kwargs.setdefault('help', 'Either CRITICAL, ERROR, WARNING, INFO or DEBUG')
    kwargs.setdefault('is_eager', True)

    def decorator(f):
        def _set_level(ctx, param, value):
            x = getattr(logging, value.upper(), None)
            if x is None:
                raise click.BadParameter(
                    'Must be CRITICAL, ERROR, WARNING, INFO or DEBUG, not {}'
                )
            set_level(x)

        return click.option(*names, callback=_set_level, **kwargs)(f)
    return decorator


def logfile_option(*names, **kwargs):
    if not names:
        names = ['--logfile', '-l']

    kwargs.setdefault('default', 'None')
    kwargs.setdefault('metavar', 'LOGFILE')
    kwargs.setdefault('expose_value', False)
    kwargs.setdefault('help', 'File to log to (default: stdout)')
    kwargs.setdefault('is_eager', True)
    kwargs.setdefault('type', click.Path(writable=True, dir_okay=False))

    def decorator(f):
        def _set_logfile(ctx, param, value):
            set_logfile(value)
        return click.option(*names, callback=_set_logfile, **kwargs)(f)
    return decorator
