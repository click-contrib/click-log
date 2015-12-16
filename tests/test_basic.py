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

    result = runner.invoke(cli, catch_exceptions=False)
    assert not result.exception
    assert result.output == 'hey\nerror: damn\n'
