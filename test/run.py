#!/usr/bin/env python3

import os
import subprocess
import tempfile
import platform
import sys

if platform.system() == "Windows":
    import _winapi

    exeext = ".exe"
else:
    exeext = ""

blender_command = sys.argv[1] if len(sys.argv) > 1 else "blender" + exeext
repository_root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
user_scripts_dir = tempfile.mkdtemp()
os.mkdir(os.path.join(user_scripts_dir, "addons"))
addon_dir = os.path.join(user_scripts_dir, "addons", "io_scene_vrm_saturday06")
if platform.system() == "Windows":
    _winapi.CreateJunction(repository_root_dir, addon_dir)
else:
    os.symlink(repository_root_dir, addon_dir)


def run_script(script, *args):
    env = os.environ.copy()
    env["BLENDER_USER_SCRIPTS"] = user_scripts_dir
    subprocess.run(
        [
            blender_command,
            "-noaudio",  # sound system to None (less output on stdout)
            "--factory-startup",  # factory settings
            "--addons",
            "io_scene_vrm_saturday06",  # enable the addon
            "--python-exit-code",
            "1",
            "--background",
            "--python",
            os.path.join(repository_root_dir, "test", script),  # run the test script
            "--",
            *args,
        ],
        env=env,
        check=True,
    )


test_vrm_dir = os.environ.get(
    "BLENDER_VRM_TEST_VRM_DIR", os.path.join(repository_root_dir, "test", "vrm")
)
test_temp_vrm_dir = os.path.join(test_vrm_dir, "temp")
test_in_vrm_dir = os.path.join(test_vrm_dir, "in")
test_out_vrm_dir = os.path.join(test_vrm_dir, "out")
test_out2_vrm_dir = os.path.join(test_vrm_dir, "out2")

os.makedirs(test_temp_vrm_dir, exist_ok=True)

run_script(
    "basic_armature.py",
    os.path.join(test_in_vrm_dir, "basic_armature.vrm"),
    test_temp_vrm_dir,
)

for vrm in [f for f in os.listdir(test_in_vrm_dir) if f.endswith(".vrm")]:
    run_script(
        "io.py",
        os.path.join(test_in_vrm_dir, vrm),
        os.path.join(test_out_vrm_dir, vrm),
        test_temp_vrm_dir,
    )
    if os.path.exists(os.path.join(test_out2_vrm_dir, vrm)):
        run_script(
            "io.py",
            os.path.join(test_out_vrm_dir, vrm),
            os.path.join(test_out2_vrm_dir, vrm),
            test_temp_vrm_dir,
        )
        run_script(
            "io.py",
            os.path.join(test_out2_vrm_dir, vrm),
            os.path.join(test_out2_vrm_dir, vrm),
            test_temp_vrm_dir,
        )
    else:
        run_script(
            "io.py",
            os.path.join(test_out_vrm_dir, vrm),
            os.path.join(test_out_vrm_dir, vrm),
            test_temp_vrm_dir,
        )
