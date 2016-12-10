# -*- coding: utf-8 -*-

import logging

import click
from click.testing import CliRunner

import click_log

import pytest


test_logger = logging.getLogger(__name__)


@pytest.fixture
def runner():
    return CliRunner()


def test_basic(runner):
    @click.command()
    @click_log.init()
    def cli():
        test_logger.info('hey')
        test_logger.error('damn')
        test_logger.warning(u"""
            Multiline error text with unicode chars:
            ❤️ 💔 💌 💕 💞 💓 💗 💖 💘 💝 💟 💜 💛 💚 💙""")

    result = runner.invoke(cli, catch_exceptions=False)
    assert not result.exception
    assert result.output == (
        'hey\n'
        'error: damn\n'
        'warning: \n'
        'warning:             Multiline error text with unicode chars:\n'
        u'warning:             ❤️ 💔 💌 💕 💞 💓 💗 💖 💘 💝 💟 💜 💛 💚 💙\n')
