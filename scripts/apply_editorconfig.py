#!/usr/bin/env python3
"""
Apply EditorConfig settings to existing files
"""

from pathlib import Path


def fix_line_endings(file_path: Path) -> bool:
    """Fix line endings to LF"""
    try:
        with open(file_path, "rb") as f:
            content = f.read()

        # Convert CRLF to LF
        if b"\r\n" in content:
            content = content.replace(b"\r\n", b"\n")
            with open(file_path, "wb") as f:
                f.write(content)
            return True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    return False


def ensure_final_newline(file_path: Path) -> bool:
    """Ensure file ends with newline"""
    try:
        with open(file_path, "rb") as f:
            content = f.read()

        if content and not content.endswith(b"\n"):
            content += b"\n"
            with open(file_path, "wb") as f:
                f.write(content)
            return True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    return False


def trim_trailing_whitespace(file_path: Path) -> bool:
    """Remove trailing whitespace from lines"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        modified = False
        new_lines = []
        for line in lines:
            new_line = line.rstrip() + "\n" if line.endswith("\n") else line.rstrip()
            if new_line != line:
                modified = True
            new_lines.append(new_line)

        if modified:
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(new_lines)

        return modified
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    return False


def apply_editorconfig_to_file(file_path: Path) -> None:
    """Apply EditorConfig settings to a single file"""
    print(f"Processing: {file_path}")

    changes = []

    # Fix line endings
    if fix_line_endings(file_path):
        changes.append("line endings")

    # Trim trailing whitespace (except .md files)
    if file_path.suffix != ".md":
        if trim_trailing_whitespace(file_path):
            changes.append("trailing whitespace")

    # Ensure final newline
    if ensure_final_newline(file_path):
        changes.append("final newline")

    if changes:
        print(f"  ✓ Fixed: {', '.join(changes)}")
    else:
        print("  ✓ No changes needed")


def main():
    """Main function"""
    project_root = Path(__file__).parent.parent

    # File patterns to process
    patterns = [
        "**/*.py",
        "**/*.json",
        "**/*.yml",
        "**/*.yaml",
        "**/*.toml",
        "**/*.md",
        "**/*.sh",
        ".gitignore",
        ".editorconfig",
    ]

    # Exclude patterns
    exclude_patterns = [
        "**/.*/**",  # Hidden directories
        "**/__pycache__/**",
        "**/.venv/**",
        "**/.git/**",
        "**/node_modules/**",
    ]

    print("Applying EditorConfig settings to existing files...")
    print(f"Project root: {project_root}")
    print()

    processed_files = 0

    for pattern in patterns:
        for file_path in project_root.glob(pattern):
            # Skip if matches exclude pattern
            should_exclude = False
            for exclude in exclude_patterns:
                if file_path.match(exclude):
                    should_exclude = True
                    break

            if should_exclude or not file_path.is_file():
                continue

            apply_editorconfig_to_file(file_path)
            processed_files += 1

    print()
    print(f"Processed {processed_files} files")
    print("✓ EditorConfig settings applied!")


if __name__ == "__main__":
    main()
