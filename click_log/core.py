# -*- coding: utf-8 -*-

import functools
import logging

import click

_ctx = click.get_current_context

LOGGER_KEY = __name__ + '.logger'
DEFAULT_LEVEL = logging.INFO


def _meta():
    return _ctx().meta.setdefault(LOGGER_KEY, {})


class ColorFormatter(logging.Formatter):
    colors = {
        'error': dict(fg='red'),
        'exception': dict(fg='red'),
        'critical': dict(fg='red'),
        'debug': dict(fg='blue'),
        'warning': dict(fg='yellow')
    }

    def format(self, record):
        if not record.exc_info:
            level = record.levelname.lower()
            if level in self.colors:
                prefix = click.style('{}: '.format(level),
                                     **self.colors[level])
                record.msg = '\n'.join(prefix + x
                                       for x in str(record.msg).splitlines())

        return logging.Formatter.format(self, record)


class ClickHandler(logging.Handler):
    def emit(self, record):
        try:
            msg = self.format(record)
            level = record.levelname.lower()
            err = level in ('warning', 'error', 'exception', 'critical')
            click.echo(msg, err=err)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


_default_handler = ClickHandler()
_default_handler.formatter = ColorFormatter()


def basic_config(logger=None):
    if not isinstance(logger, logging.Logger):
        logger = logging.getLogger(logger)
    logger.handlers = [_default_handler]
    logger.propagate = False

    return logger


def init(logger=None):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            m = _meta()
            l = basic_config(logger=logger)
            l.setLevel(m.get('level', DEFAULT_LEVEL))

            if m.setdefault('logger', l) is not l:
                raise RuntimeError('Only one main logger allowed.')

            return f(*args, **kwargs)
        return wrapper
    return decorator


def get_logger():
    return _meta().get('logger')


def set_level(level):
    '''Set the level for current context's logger.'''

    if not isinstance(level, int):
        raise ValueError('Must be constant from `logging`.')

    logger = get_logger()
    if logger is not None:
        logger.setLevel(level)

    _meta()['level'] = level


def get_level():
    return _meta().get('level', DEFAULT_LEVEL)
