#!/usr/bin/env python3
#
# Copyright (C) 2026 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Setup Python virtual environment for simpleperf tests.")
    parser.add_argument("action", nargs="?", choices=[
                        "clean"], help="Clean the virtual environment.")
    args: argparse.Namespace = parser.parse_args()

    script_dir: Path = Path(__file__).resolve().parent
    venv_dir: Path = script_dir / "venv"

    if args.action == "clean":
        if venv_dir.exists():
            print(f"Cleaning up existing virtual environment at {venv_dir}...")
            shutil.rmtree(venv_dir)
            print("Cleaned successfully.")
        else:
            print("No virtual environment to clean.")
        return 0

    print(f"Creating virtual environment in {venv_dir} if it doesn't exist...")
    if not venv_dir.exists():
        # Use sys.executable to ensure we use the same Python interpreter to create the venv
        try:
            subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: Failed to create venv: {e}", file=sys.stderr)
            return 1

    # Determine paths to python and pip executables in the venv
    venv_python: Path
    venv_pip: Path
    if os.name == "nt":
        venv_python = venv_dir / "Scripts" / "python.exe"
        venv_pip = venv_dir / "Scripts" / "pip.exe"
    else:
        venv_python = venv_dir / "bin" / "python"
        venv_pip = venv_dir / "bin" / "pip"

    requirements_txt: Path = script_dir / "requirements.txt"
    if requirements_txt.exists():
        print("Installing required Python packages...")
        try:
            subprocess.run([str(venv_python), "-m", "pip", "install",
                           "-r", str(requirements_txt)], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: Pip install failed: {e}", file=sys.stderr)
            return 1
    else:
        print("Notice: No requirements.txt found. Skipping package installation.")

    # Calculate PYTHONPATH paths (absolute paths)
    test_dir: Path = script_dir
    scripts_dir: Path = script_dir.parent

    # Format PYTHONPATH correctly for the platform
    path_sep: str = ";" if os.name == "nt" else ":"
    pythonpath: str = f"{test_dir}{path_sep}{scripts_dir}"

    print("\nEnvironment set up successfully!\n")
    print(f"PYTHONPATH is now: {pythonpath}\n")

    # Display activation instructions based on OS
    if os.name == "nt":
        print("\nFor Command Prompt (cmd.exe):")
        print(f"    \"{venv_dir}\\Scripts\\activate.bat\"")
        print(
            f"    if defined PYTHONPATH (set \"PYTHONPATH={pythonpath};%PYTHONPATH%\") else (set \"PYTHONPATH={pythonpath}\")")

        print("\nFor PowerShell:")
        print(f"    & \"{venv_dir}\\Scripts\\Activate.ps1\"")
        print(
            f"    if ($env:PYTHONPATH) {{ $env:PYTHONPATH = \"{pythonpath};$env:PYTHONPATH\" }} else {{ $env:PYTHONPATH = \"{pythonpath}\" }}")

        print("\nFor Git Bash / MinGW:")
        # Normalize backslashes to forward slashes for the Bash source command
        venv_bash_dir = str(venv_dir).replace('\\', '/')
        print(f"    source \"{venv_bash_dir}/Scripts/activate\"")
        # Uses Bash syntax but maintains the Windows semicolon separator
        print(f"    export PYTHONPATH=\"{pythonpath}${{PYTHONPATH:+;$PYTHONPATH}}\"")
    else:
        print("To activate the virtual environment and set PYTHONPATH, run:")
        print(f"    source \"{venv_dir}/bin/activate\"")
        print(f"    export PYTHONPATH=\"{pythonpath}${{PYTHONPATH:+:$PYTHONPATH}}\"")

    print("\n")

    # Warn about ANDROID_BUILD_TOP
    if "ANDROID_BUILD_TOP" in os.environ:
        print("WARNING: If you are doing an NDK release you need to unset ANDROID_BUILD_TOP\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
