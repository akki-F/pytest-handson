# conftest.py
import pytest

# @pytest.fixture(scope="session", autouse=True)
def global_setup():
    # グローバルセットアップ
    print("\nGlobal setup")
    yield
    # グローバルクリーンアップ
    print("\nGlobal cleanup")