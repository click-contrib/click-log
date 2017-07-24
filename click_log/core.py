# -*- coding: utf-8 -*-

import sys

import collections
import functools
import logging

import click

_ctx = click.get_current_context

LOGGER_KEY = __name__ + '.logger'
DEFAULT_LEVEL = logging.INFO

PY2 = sys.version_info[0] == 2

if PY2:
    text_type = unicode  # noqa
else:
    text_type = str


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

                msg = record.msg
                if not PY2 and isinstance(msg, bytes):
                    msg = msg.decode(sys.getfilesystemencoding(),
                                     'replace')
                elif not isinstance(msg, (text_type, bytes)):
                    msg = str(msg)
                record.msg = '\n'.join(prefix + x for x in msg.splitlines())

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


class PrerecordingHandler(logging.Handler):
    def __init__(self, queue):
        logging.Handler.__init__(self, logging.DEBUG)
        self._record_queue = queue

    def handle(self, record):
        self._record_queue.append(record)


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


def init(logger=None):
    '''Set the application's logger and call :py:func:`basic_config` on it.'''
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            m = _meta()
            l = basic_config(logger=logger)
            l.setLevel(m.get('level', DEFAULT_LEVEL))

            if m.setdefault('logger', l) is not l:
                raise RuntimeError('Only one main logger allowed.')

            _handle_prerecorded(l)

            return f(*args, **kwargs)
        return wrapper
    return decorator


def _handle_prerecorded(l):
    try:
        records = l._click_log_prerecorded
        del l._click_log_prerecorded
    except AttributeError:
        return

    for record in records:
        if l.isEnabledFor(record.levelno):
            l.handle(record)


def pre_record(logger=None, maxlen=20):
    '''
    click-log only initializes the logger after the options have been parsed,
    since only at that point the logging level is known. This is often too late
    since other log-worthy initialization may have happened before (e.g. at
    import time).

    To work around this, use this function to "pre-initialize" your logger to
    keep track the last `maxlen` records before the logger gets properly
    initialized. :py:func:`init` will replay those log records when it is ready
    to do so.

    Example::

        logger = logging.getLogger('foobar')
        click_log.pre_record(logger)

        try:
            import optional_package
        except ImportError:
            logger.debug('optional_package not available.')
        else:
            logger.debug('optional_package available.')

        # Without pre_record, the above messages will get lost

        @click.command()
        @click_log.simple_verbosity_option()
        @click_log.init(logger)
        def cli():
            logger.info('Hello world!')
    '''
    logger = _normalize_logger(logger)
    queue = collections.deque(maxlen=maxlen)
    logger.handlers = [PrerecordingHandler(queue)]
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    logger._click_log_prerecorded = queue
    return logger


def get_logger():
    '''Get the application's logger.'''
    return _meta().get('logger')


def set_level(level):
    '''Set the level for the application's logger.'''

    if not isinstance(level, int):
        raise ValueError('Must be constant from `logging`.')

    logger = get_logger()
    if logger is not None:
        logger.setLevel(level)

    _meta()['level'] = level


def get_level():
    '''Get the level for the application's logger.'''
    return _meta().get('level', DEFAULT_LEVEL)
