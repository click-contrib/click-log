# -*- coding: utf-8 -*-

import logging
import sys

import click

LOGGER_KEY = __name__ + '.logger'
DEFAULT_LEVEL = logging.INFO


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
            msg = record.getMessage()
            if level in self.colors:
                prefix = click.style('{}: '.format(level),
                                     **self.colors[level])
                msg = '\n'.join(prefix + x for x in msg.splitlines())
            return msg
        return logging.Formatter.format(self, record)


class ClickHandler(logging.Handler):
    _use_stderr = True

    def emit(self, record):
        try:
            msg = self.format(record)
            level = record.levelname.lower()
            newline = True

            if hasattr(record, 'nl'):
                newline = record.nl;

            click.echo(msg, nl=newline, err=self._use_stderr)
        except Exception:
            self.handleError(record)


_default_handler = ClickHandler()
_default_handler.formatter = ColorFormatter()


def _normalize_logger(logger):
    if not isinstance(logger, logging.Logger):
        logger = logging.getLogger(logger)
    return logger


def basic_config(logger=None):
    '''Set up the default handler (:py:class:`ClickHandler`) and formatter
    (:py:class:`ColorFormatter`) on the given logger.'''
    logger = _normalize_logger(logger)
    logger.handlers = [_default_handler]
    logger.propagate = False

    return logger
