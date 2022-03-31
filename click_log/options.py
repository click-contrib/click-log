import logging

import click
from .core import _normalize_logger


def simple_verbosity_option(logger=None, *names, **kwargs):
    '''A decorator that adds a `--verbosity, -v` option to the decorated
    command.

    Name can be configured through ``*names``. Keyword arguments are passed to
    the underlying ``click.option`` decorator.
    '''

    if not names:
        names = ['--verbosity', '-v']
    if isinstance(logger, str) and logger.startswith('-'):
        raise ValueError('Since click-log 0.2.0, the first argument must now '
                         'be a logger.')

    kwargs.setdefault('default', 'INFO')
    kwargs.setdefault('metavar', 'LVL')
    kwargs.setdefault('expose_value', False)
    kwargs.setdefault('help', 'Either CRITICAL, ERROR, WARNING, INFO or DEBUG')
    kwargs.setdefault('is_eager', True)

    logger = _normalize_logger(logger)

    def decorator(f):
        def _set_level(ctx, param, value):
            x = getattr(logging, value.upper(), None)
            if x is None:
                raise click.BadParameter(
                    'Must be CRITICAL, ERROR, WARNING, INFO or DEBUG, not {}'
                    .format(value)
                )
            logger.setLevel(x)

        return click.option(*names, callback=_set_level, **kwargs)(f)

    return decorator


def verbosity_option(logger=None, *names, **kwargs):
    """A decorator that adds a `--verbosity, -v` option to the decorated
    command, allowing to configure log levels of a logger and its
    child-loggers.

    If for example::

    .. code-block:: python

        from logging import getLogger
        from click import command
        from click_log import verbosity_option

        @command
        @verbosity_option(getLogger('foo'))
        def command():
            pass

    is called via

    .. code-block:: sh

        $ ./script.py -v WARNING,bar=DEBUG

    the logger `'foo'` is set to level WARNING, but its child logger `'foo.bar'`
    will still log messages with level DEBUG.

    Name can be configured through ``*names``. Keyword arguments are passed to
    the underlying ``click.option`` decorator.

    :param logger: logging.Logger
        Logger instance for which log levels are set.
    :param names: str
        Option names (default: `['-v', '--verbose']`)
    """
    if not names:
        names = ["-v", "--verbose"]
    SYNTAX_DESC = "comma-separated list of [LOGGER=]LEVEL assignments, where LEVEL is one of CRITICAL, ERROR, WARNING, INFO or DEBUG"
    kwargs.setdefault("default", "INFO")
    kwargs.setdefault("metavar", "[LOGGER=]LEVEL[,...]")
    kwargs.setdefault("expose_value", False)
    kwargs.setdefault("help", "A %s." % (SYNTAX_DESC,))
    kwargs.setdefault("is_eager", True)

    logger = _normalize_logger(logger)

    def decorator(f):
        def _set_log_levels(_ctx, _param, value):
            for item in value.split(","):
                try:
                    name, level = item.split("=", 1)
                    target_logger = logger.getChild(name)
                except ValueError:
                    level = item
                    target_logger = logger

                logging_level = getattr(logging, level.upper(), None)
                if logging_level is None:
                    raise click.BadParameter("Must be a %s, not {}" % SYNTAX_DESC)

                target_logger.setLevel(logging_level)

        return click.option(*names, callback=_set_log_levels, **kwargs)(f)

    return decorator
