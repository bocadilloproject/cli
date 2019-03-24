import os

os.environ["TESTING"] = "TRUE"

import pytest
from click.testing import CliRunner

from queso import create_cli


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def cli():
    return create_cli()
