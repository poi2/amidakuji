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

    # Check if --check flag is supported by running uv lock --help
    help_code, help_stdout, help_stderr = run_command(
        ["uv", "lock", "--help"], cwd=project_root
    )

    if help_code == 0 and "--check" in help_stdout:
        # Use --check if available (newer uv versions)
        print("🔍 Using uv lock --check...")
        exit_code, stdout, stderr = run_command(
            ["uv", "lock", "--check"], cwd=project_root
        )

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
    else:
        # Fallback method for older uv versions
        print("🔄 Using fallback method (older uv version)...")

        # Create a backup of current lock file
        import shutil

        backup_path = lock_file.with_suffix(".lock.backup")
        shutil.copy2(lock_file, backup_path)

        try:
            # Generate new lock file
            exit_code, stdout, stderr = run_command(["uv", "lock"], cwd=project_root)

            if exit_code != 0:
                print("❌ Failed to regenerate lock file!")
                if stderr:
                    print(stderr)
                sys.exit(1)

            # Compare old and new lock files
            with open(lock_file, "r") as f:
                new_content = f.read()
            with open(backup_path, "r") as f:
                old_content = f.read()

            if new_content == old_content:
                print("✅ uv.lock is consistent with pyproject.toml")
            else:
                print("❌ uv.lock is outdated or inconsistent!")
                print("\n💡 To fix this issue:")
                print("   1. Run 'uv lock' to update uv.lock")
                print("   2. Commit the updated uv.lock file")
                # Restore original lock file
                shutil.move(backup_path, lock_file)
                sys.exit(1)
        finally:
            # Clean up backup file if it exists
            if backup_path.exists():
                backup_path.unlink()


if __name__ == "__main__":
    main()
