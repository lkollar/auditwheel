import logging
import sys

from unittest.mock import patch, Mock

from auditwheel.main import main


def test_non_linux_platform(monkeypatch, capsys):
    # GIVEN
    monkeypatch.setattr(sys, "platform", "darwin")

    # WHEN
    retval = main()

    # THEN
    assert retval == 1
    captured = capsys.readouterr()
    assert captured.out == "Error: This tool only supports Linux\n"


@patch("auditwheel.main.argparse.ArgumentParser")
@patch("auditwheel.main.logging.basicConfig")
def test_verbose_logging_non_verbose(basic_cfg_mock, parser_mock, monkeypatch):
    # GIVEN
    monkeypatch.setattr(sys, "platform", "linux")
    args = Mock()
    args.verbose = 0
    args.func.return_value = 0
    parser_mock.return_value.parse_args.return_value = args

    # WHEN
    retval = main()

    # THEN
    assert retval == 0
    basic_cfg_mock.assert_called_once_with(level=logging.INFO)


@patch("auditwheel.main.argparse.ArgumentParser")
@patch("auditwheel.main.logging.basicConfig")
def test_verbose_logging_verbose(basic_cfg_mock, parser_mock, monkeypatch):
    # GIVEN
    monkeypatch.setattr(sys, "platform", "linux")
    args = Mock()
    args.verbose = 1
    args.func.return_value = 0
    parser_mock.return_value.parse_args.return_value = args

    # WHEN
    retval = main()

    # THEN
    assert retval == 0
    basic_cfg_mock.assert_called_once_with(level=logging.DEBUG)


def test_help(monkeypatch, capsys):
    # GIVEN
    monkeypatch.setattr(sys, "platform", "linux")
    monkeypatch.setattr(sys, "argv", ["auditwheel"])

    # WHEN
    retval = main()

    # THEN
    assert retval is None
    captured = capsys.readouterr()
    assert "usage: auditwheel [-h] [-V] [-v] command ..." in captured.out

