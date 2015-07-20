import click
from click.testing import CliRunner
import pytest

import click_log

@pytest.fixture
def runner():
    return CliRunner()

def test_basic(runner):
    @click.command()
    def cli():
        logger = click_log.basic_config()
        logger.error('damn')

    result = runner.invoke(cli, catch_exceptions=False)
    assert not result.exception
    assert result.output == 'error: damn\n'
