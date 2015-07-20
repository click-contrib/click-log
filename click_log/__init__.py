# -*- coding: utf-8 -*-

import click
import logging
import functools

__version__ = '0.1.1'
LOGGER_KEY = __name__ + '.logger'


if not hasattr(click, 'get_current_context'):
    raise RuntimeError('You need Click 5.0.')


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


class ClickStream(object):
    def write(self, string):
        click.echo(string, err=True, nl=False)


_default_handler = logging.StreamHandler(ClickStream())
_default_handler.formatter = ColorFormatter()


def basic_config(logger=None):
    if not isinstance(logger, logging.Logger):
        logger = logging.getLogger(logger)
    logger.handlers = [_default_handler]
    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger
