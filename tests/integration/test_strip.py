import glob
import os
import shutil
import subprocess
import sys
import tempfile

from auditwheel.repair import repair_wheel
from auditwheel.wheeltools import InWheelCtx


def download_wheel(package_name, destination):
    destination.mkdir(exist_ok=True)

    with tempfile.TemporaryDirectory() as tempdir:
        subprocess.run([sys.executable, "-m", "pip", "--disable-pip-version-check",
                        "download", "--no-deps", package_name],
                       cwd=tempdir, check=True)
        downloaded_wheels = list(glob.glob(os.path.join(tempdir, "*.whl")))
        assert len(downloaded_wheels) == 1
        wheel_name = os.path.relpath(downloaded_wheels[0], start=tempdir)
        shutil.move(downloaded_wheels[0], destination)

    return os.path.join(destination, wheel_name)


def test_strip(tmp_path):
    cython_wheel = download_wheel("Cython==0.29.14", tmp_path)

    abi = "manylinux1_x86_64"
    lib_sdir = tmp_path / "library_source_dir"
    out_dir = tmp_path / "output"
    out_dir.mkdir(exist_ok=True)

    # Make sure there are symbols in the contained .so files
    with InWheelCtx(os.fspath(cython_wheel)) as wheel_ctx:
        for file in wheel_ctx.iter_files():
            if file.endswith(".so"):
                stdout = subprocess.check_output(["nm", file])
                assert len(stdout) > 1

    repair_wheel(os.fspath(cython_wheel), abi, lib_sdir, out_dir, update_tags=True,
                 strip=True)

    # Make sure no symbols are left in the contained .so files
    result_wheel = list(out_dir.glob("Cython*.whl"))[0]
    with InWheelCtx(os.fspath(result_wheel)) as wheel_ctx:
        for file in wheel_ctx.iter_files():
            if file.endswith(".so"):
                proc = subprocess.run(["nm", file], capture_output=True, text=True)
                assert not proc.stdout
                assert "no symbols" in proc.stderr
