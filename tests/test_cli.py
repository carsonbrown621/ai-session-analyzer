import pytest

from session_analyzer import __version__
from session_analyzer.cli import main


def test_no_args_prints_help_and_exits_zero(capsys):
    assert main([]) == 0
    assert "usage: session-analyzer" in capsys.readouterr().out


def test_help_exits_zero(capsys):
    # argparse handles --help by raising SystemExit(0) after printing.
    with pytest.raises(SystemExit) as exc_info:
        main(["--help"])
    assert exc_info.value.code == 0
    assert "usage: session-analyzer" in capsys.readouterr().out


def test_version_prints_version(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main(["--version"])
    assert exc_info.value.code == 0
    assert capsys.readouterr().out.strip() == f"session-analyzer {__version__}"
