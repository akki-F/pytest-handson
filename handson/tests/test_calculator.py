import pytest
import time
from typing import List, Generator
from datetime import datetime

from src.calculator import Calculator


# 基本的な3Aパターン (Arrange-Act-Assert)
class TestCalculator3A:
    def test_add_3a_pattern(self):
        # Arrange（準備）
        calc = Calculator()
        x, y = 1, 2
        expected = 3

        # Act（実行）
        result = calc.add(x, y)

        # Assert（検証）
        assert result == expected


# 例外テスト
class TestCalculatorExceptions:
    def test_divide_by_zero(self):
        calc = Calculator()
        with pytest.raises(ZeroDivisionError) as excinfo:
            calc.divide(1, 0)
        assert str(excinfo.value) == "division by zero"

    def test_invalid_input(self):
        calc = Calculator()
        with pytest.raises(ValueError) as excinfo:
            calc.add("1", 2)
        assert "Invalid input" in str(excinfo.value)


# パラメトライズドテスト
class TestCalculatorParametrized:
    @pytest.mark.parametrize(
        "x, y, expected", [(1, 2, 3), (-1, 1, 0), (0, 0, 0), (10, -5, 5)]
    )
    def test_add_parametrized(self, x, y, expected):
        calc = Calculator()
        assert calc.add(x, y) == expected

    @pytest.mark.parametrize(
        "x, y, expected", [(6, 2, 3), (10, 2, 5), (0, 1, 0), (-6, 2, -3)]
    )
    def test_divide_parametrized(self, x, y, expected):
        calc = Calculator()
        assert calc.divide(x, y) == expected


# setup/teardownパターン
class TestCalculatorWithSetup:
    def setup_method(self):
        """各テストメソッドの前に実行"""
        self.calc = Calculator()
        self.test_values = [1, 2, 3]
        print("\nSetup method called")

    def teardown_method(self):
        """各テストメソッドの後に実行"""
        self.test_values = []
        print("\nTeardown method called")

    def test_add_with_setup(self):
        result = self.calc.add(self.test_values[0], self.test_values[1])
        assert result == 3

    def test_subtract_with_setup(self):
        result = self.calc.subtract(self.test_values[2], self.test_values[1])
        assert result == 1


# フィクスチャを使用したテスト
class TestCalculatorWithFixtures:
    @pytest.fixture
    def calc_fixture(self):
        """Calculatorインスタンスを提供するフィクスチャ"""
        calc = Calculator()
        yield calc
        # クリーンアップコードがあれば、ここに記述

    @pytest.fixture
    def test_data(self):
        """テストデータを提供するフィクスチャ"""
        return [(1, 2, 3), (4, 5, 9), (7, 8, 15)]

    def test_add_with_fixture(self, calc_fixture, test_data):
        for x, y, expected in test_data:
            assert calc_fixture.add(x, y) == expected


# モック/スタブを使用したテスト
class TestCalculatorWithMocks:
    def test_add_with_mock(self, mocker):
        calc = Calculator()
        # モックメソッドを作成
        mock_method = mocker.patch.object(calc, "add", return_value=10)

        result = calc.add(5, 5)

        assert result == 10
        mock_method.assert_called_once_with(5, 5)


# 前提条件のスキップ
class TestCalculatorWithSkip:
    @pytest.mark.skip(reason="このテストは一時的にスキップ")
    def test_skipped(self):
        assert False

    @pytest.mark.skipif(1 + 1 == 2, reason="条件に基づいてスキップ")
    def test_conditional_skip(self):
        assert False


# 新しいフィクスチャの定義
@pytest.fixture(scope="session")
def global_data():
    """セッション全体で使用するデータ"""
    return {"start_time": datetime.now()}


@pytest.fixture(scope="class")
def class_data():
    """クラス内で共有するデータ"""
    return {"data": [1, 2, 3]}


@pytest.fixture(scope="function", autouse=True)
def function_setup():
    """各テスト関数で自動的に実行"""
    print("\nTest function setup")
    yield
    print("\nTest function cleanup")


# フィクスチャの継承と依存関係
class TestFixtureInheritance:
    @pytest.fixture
    def parent_fixture(self):
        return {"parent": "data"}

    @pytest.fixture
    def child_fixture(self, parent_fixture):
        parent_fixture.update({"child": "data"})
        return parent_fixture

    def test_fixture_inheritance(self, child_fixture):
        assert child_fixture == {"parent": "data", "child": "data"}


# マーク（tags）を使用したテスト
class TestWithMarks:
    @pytest.mark.slow
    def test_slow_operation(self):
        time.sleep(1)
        assert True

    @pytest.mark.smoke
    def test_smoke(self):
        assert True

    @pytest.mark.integration
    def test_integration(self):
        assert True


# パラメータ化されたフィクスチャ
class TestParametrizedFixtures:
    @pytest.fixture(params=[1, 2, 3])
    def numbers(self, request):
        return request.param

    def test_with_parametrized_fixture(self, numbers):
        assert numbers in [1, 2, 3]


# 非同期テスト
class TestAsync:
    @pytest.mark.asyncio
    async def test_async_operation(self):
        async def async_add(x, y):
            return x + y

        result = await async_add(1, 2)
        assert result == 3


# テストの依存関係
class TestDependencies:
    @pytest.mark.dependency()
    def test_a(self):
        assert True

    @pytest.mark.dependency(depends=["TestDependencies::test_a"])
    def test_b(self):
        assert True


# カスタムマーカー
pytestmark = pytest.mark.custom_mark

# プロパティベーステスト
from hypothesis import given, strategies as st


class TestPropertyBased:
    @given(st.integers(), st.integers())
    def test_add_properties(self, x, y):
        calc = Calculator()
        result = calc.add(x, y)
        assert result == x + y
        assert isinstance(result, (int, float))


# コンテキストマネージャを使用したテスト
class TestWithContext:
    @pytest.fixture
    def managed_resource(self):
        class Resource:
            def __enter__(self):
                print("\nResource acquired")
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                print("\nResource released")

        return Resource()

    def test_with_context(self, managed_resource):
        with managed_resource:
            assert True

# カスタムフィクスチャファクトリー
@pytest.fixture
def create_test_data():
    def _create_data(size: int) -> List[int]:
        return list(range(size))

    return _create_data


class TestFixtureFactory:
    def test_with_factory(self, create_test_data):
        data = create_test_data(5)
        assert len(data) == 5


# テストのグループ化とネスト
class TestGroup:
    class TestSubGroup:
        def test_nested(self):
            assert True

    def test_in_main_group(self):
        assert True
