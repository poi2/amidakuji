# Migration to uv.lock

## Execute in Dev Container:

```bash
# Generate uv.lock file
uv lock

# Test dependency check script
python scripts/check_lockfile.py

# Test new workflow
uv sync
uv run pytest tests/ -v
```

## Benefits after migration

- ✅ **Complete reproducibility**: Strict dependency management with hash values
- ✅ **Automatic checks**: Verify uv.lock consistency in CI
- ✅ **Modern tooling**: Leverage latest uv features
- ✅ **Security**: Detect tampering of dependencies

## CI behavior

1. **Lock file check**: Verify uv.lock is consistent with pyproject.toml
2. **On failure**: Display clear error message and fix instructions
3. **On success**: Execute normal test flow
