"""Temporary test file to generate 3 more failure types for Stage 2 development.

Will be removed once parse() is validated against all 4 failure types.
"""

# --- IMPORT failure ---
# 故意 import 一个不存在的包
import nonexistent_package_xyz


def test_import_failure() -> None:
    """This test exists only to trigger an ImportError in CI."""
    pass