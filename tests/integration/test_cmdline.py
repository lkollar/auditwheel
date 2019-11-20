import pathlib
from unittest import mock

from auditwheel.main import main

HERE = pathlib.Path(__file__).parent
SNAPPY_WHEEL = HERE / "python_snappy-0.5.2-pp260-pypy_41-linux_x86_64.whl"


@mock.patch("auditwheel.repair.repair_wheel")
def test_cmdline(mock_repair_wheel):
    mock_repair_wheel.return_value = None
    args = ["auditwheel", "repair", "--strip", str(SNAPPY_WHEEL)]
    main(args)
    mock_repair_wheel.assert_called_once()
    assert mock_repair_wheel.call_args.kwargs['strip'] is True
    assert mock_repair_wheel.call_args.kwargs['strip_args'] == ["--strip-all"]
