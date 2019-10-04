from unittest.mock import patch

from auditwheel.repair import repair_wheel


@patch("auditwheel.repair.copylib")
@patch("auditwheel.repair.InWheelCtx")
@patch("auditwheel.repair.get_wheel_elfdata")
def test_repair_strip(get_wheel_elfdata_mock, wheelctx_mock, copylib_mock):
    repair_wheel(wheel_path="/fakepath", abi="manylinux1_x86", lib_sdir="/fakepath",
                 out_dir="/fakepath", update_tags=False, strip=True, strip_args=["-s"])
    assert True
