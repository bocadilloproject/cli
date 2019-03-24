from multiprocessing import Process
import time

import pytest


@pytest.fixture(name="serve")
def fixture_serve(cli, runner):
    def _check():
        p = Process(target=runner.invoke, args=(cli, ["serve"]))
        p.start()
        time.sleep(1)
        result = p.is_alive()
        p.terminate()
        p.join(1)
        assert not p.is_alive()
        return result

    return _check


def test_if_no_app_then_serve_fails(serve):
    assert not serve()


def test_serve_app(runner, serve):
    with runner.isolated_filesystem():
        with open("app.py", "w") as appfile:
            appfile.write("from bocadillo import App\n")
            appfile.write("app = App()")
        assert serve()


def test_serve_help(cli, runner):
    result = runner.invoke(cli, ["serve", "--help"])
    assert result.exit_code == 0, result.output
    assert "-- [UVICORN_OPTIONS]" in result.output
    assert "--host" in result.output  # forwarded from `uvicorn`
