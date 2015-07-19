import click
from click.testing import CliRunner
import pytest

import click_log

@pytest.fixture
def runner():
    return CliRunner()

def test_basic(runner):
    @click.command()
    @click_log.pass_logger
    def cli(logger):
        logger.error('damn')

    result = runner.invoke(cli, catch_exceptions=False)
    assert not result.exception
    assert result.output == 'error: damn\n'
