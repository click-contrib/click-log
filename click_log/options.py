import logging

import click

from .core import set_level


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
