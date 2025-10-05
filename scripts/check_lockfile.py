#!/usr/bin/env python3
"""
Check if uv.lock is consistent with pyproject.toml
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], cwd: Path | None = None) -> tuple[int, str, str]:
    """Run a command and return exit code, stdout, stderr"""
    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout, result.stderr


def main() -> None:
    """Main function to check lock file consistency"""
    project_root = Path(__file__).parent.parent

    print("🔍 Checking uv.lock consistency with pyproject.toml...")

    # Check if uv.lock exists
    lock_file = project_root / "uv.lock"
    if not lock_file.exists():
        print("❌ uv.lock file not found!")
        print("💡 Run 'uv lock' to generate it")
        sys.exit(1)

    # Run uv lock --check
    exit_code, stdout, stderr = run_command(["uv", "lock", "--check"], cwd=project_root)

    if exit_code == 0:
        print("✅ uv.lock is consistent with pyproject.toml")
    else:
        print("❌ uv.lock is outdated or inconsistent!")
        print("\n📋 uv output:")
        if stdout:
            print(stdout)
        if stderr:
            print(stderr)
        print("\n💡 To fix this issue:")
        print("   1. Run 'uv lock' to update uv.lock")
        print("   2. Commit the updated uv.lock file")
        sys.exit(1)


if __name__ == "__main__":
    main()
