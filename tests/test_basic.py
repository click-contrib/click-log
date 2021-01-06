# -*- coding: utf-8 -*-

import logging

import click
from click.testing import CliRunner

import click_logging

import pytest


test_logger = logging.getLogger(__name__)
click_logging.basic_config(test_logger)
test_logger.level = logging.INFO


@pytest.fixture
def runner():
    return CliRunner()


def test_basic(runner):
    @click.command()
    def cli():
        test_logger.info('hey')
        test_logger.error('damn')

    result = runner.invoke(cli, catch_exceptions=False)
    assert not result.exception
    assert result.output == 'hey\nerror: damn\n'


def test_multilines(runner):
    @click.command()
    def cli():
        test_logger.warning("""
            Lorem ipsum dolor sit amet,
            consectetur adipiscing elit,
            sed do eiusmod tempor incididunt""")

    result = runner.invoke(cli, catch_exceptions=False)
    assert not result.exception
    assert result.output == (
        'warning: \n'
        'warning:             Lorem ipsum dolor sit amet,\n'
        'warning:             consectetur adipiscing elit,\n'
        'warning:             sed do eiusmod tempor incididunt\n')


def test_unicode(runner):
    @click.command()
    def cli():
        test_logger.error(u"""
            ❤️ 💔 💌 💕 💞 💓 💗 💖 💘
            💝 💟 💜 💛 💚 💙""")

    result = runner.invoke(cli, catch_exceptions=False)
    assert not result.exception
    assert result.output == (
        'error: \n'
        u'error:             ❤️ 💔 💌 💕 💞 💓 💗 💖 💘\n'
        u'error:             💝 💟 💜 💛 💚 💙\n')


def test_weird_types_log(runner):
    @click.command()
    def cli():
        test_logger.error(42)
        test_logger.error('42')
        test_logger.error(b'42')
        test_logger.error(u'42')

    result = runner.invoke(cli, catch_exceptions=False)
    assert not result.exception
    assert set(result.output.splitlines()) <= set(('error: 42', 'error: b\'42\''))


def test_early_logging(runner):
    i = None

    def callback(context, param, value):
        test_logger.debug('catch me {}!'.format(i))

    @click.command()
    @click_logging.simple_verbosity_option(test_logger)
    @click.option('--config', is_eager=True, default=None, expose_value=False,
                  callback=callback)
    def cli():
        test_logger.debug('hello')

    for i in range(2):
        result = runner.invoke(cli, ['-v', 'debug'], catch_exceptions=False)
        assert 'debug: hello' in result.output
        assert 'debug: catch me {}!'.format(i) in result.output


def test_logging_args(runner):
    @click.command()
    @click_logging.simple_verbosity_option(test_logger)
    def cli():
        test_logger.debug('hello %s', 'world')

    result = runner.invoke(cli, ['-v', 'debug'])
    assert 'debug: hello world' in result.output
