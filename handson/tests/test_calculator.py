import sys
import platform
import pytest
import time
from typing import List
from datetime import datetime
import asyncio

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

    def test_exception_attributes(self):
        calc = Calculator()
        with pytest.raises(ValueError) as excinfo:
            calc.add("invalid", 2)
        # 例外オブジェクトの詳細な検証
        assert excinfo.type == ValueError
        assert excinfo.value.args[0] == "Invalid input"

    def test_multiple_exceptions(self):
        calc = Calculator()
        # 複数の例外をまとめて検証
        with pytest.raises((ValueError, TypeError)):
            # TypeError発生
            calc.complex_operation("invalid")

        with pytest.raises((ValueError, TypeError)):
            # ValueError発生
            calc.complex_operation(-5)


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


# 複数パラメータのパラメトライズ
class TestMultipleParameters:
    @pytest.mark.parametrize("x", [1, 2, 3])
    @pytest.mark.parametrize("y", [10, 20])
    def test_multiply_combinations(self, x, y):
        calc = Calculator()
        assert calc.multiply(x, y) in [10, 20, 30, 40, 60]


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


# クラスレベルのSetup/Teardown
class TestClassSetup:
    @classmethod
    def setup_class(cls):
        """クラス内の全テスト前に1回実行"""
        print("\nClass Setup: Creating shared resources")
        cls.shared_resource = {"base": 100}

    @classmethod
    def teardown_class(cls):
        """クラス内の全テスト後に1回実行"""
        print("\nClass Teardown: Cleaning up shared resources")
        cls.shared_resource = None

    def test_using_shared_resource(self):
        print("\nfunction executed")
        assert self.shared_resource["base"] == 100

    def test_using_shared_resource2(self):
        print("\nfunction2 executed")
        assert self.shared_resource["base"] == 100


class TestSetupOrder:
    @classmethod
    def setup_class(cls):
        print("\n1. Class setup")

    def setup_method(self):
        print("\n2. Method setup")

    def test_first(self):
        print("\n3. Test execution")
        assert True

    def teardown_method(self):
        print("\n4. Method teardown")

    @classmethod
    def teardown_class(cls):
        print("\n5. Class teardown")


# モック/スタブを使用したテスト
class TestCalculatorWithMocks:
    def test_add_with_mock(self, mocker):
        calc = Calculator()
        # モックメソッドを作成
        mock_method = mocker.patch.object(calc, "add", return_value=10)

        result = calc.add(5, 5)

        assert result == 10
        mock_method.assert_called_once_with(5, 5)


# 高度なモック例
class TestAdvancedMocking:
    def test_mock_with_side_effect(self, mocker):
        def side_effect(x, y):
            if x < 0 or y < 0:
                raise ValueError("Negative values not allowed")
            return x + y

        calc = Calculator()
        mock_add = mocker.patch.object(calc, "add", side_effect=side_effect)

        # 正常系
        assert calc.add(1, 2) == 3
        # 異常系
        with pytest.raises(ValueError):
            calc.add(-1, 2)

    def test_mock_attributes(self, mocker):
        mock = mocker.Mock()
        mock.attribute = 42
        mock.method.return_value = "mocked"

        assert mock.attribute == 42
        assert mock.method() == "mocked"


# spy
class TestWithSpies:
    def test_with_spy(self, mocker):
        calc = Calculator()
        spy = mocker.spy(calc, "add")

        result = calc.add(2, 3)

        assert result == 5  # 実際の結果を検証
        spy.assert_called_once_with(2, 3)  # 呼び出しを検証


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


@pytest.fixture(scope="session")
def global_data():
    """セッション全体で使用するデータ"""
    print("\nSession fixture: setup")
    data = {"start_time": datetime.now()}
    yield data
    print("\nSession fixture: teardown")


@pytest.fixture(scope="module")
def module_data():
    """モジュール内で共有するデータ"""
    print("\nModule fixture: setup")
    data = {"module": "test"}
    yield data
    print("\nModule fixture: teardown")


@pytest.fixture(scope="class")
def class_data():
    """クラス内で共有するデータ"""
    print("\nClass fixture: setup")
    data = {"class": "TestClass"}
    yield data
    print("\nClass fixture: teardown")


@pytest.fixture(scope="function")
def function_data():
    """各テスト関数で個別のデータ"""
    print("\nFunction fixture: setup")
    data = {"function": "test"}
    yield data
    print("\nFunction fixture: teardown")


# @pytest.fixture(scope="function", autouse=True)
def auto_fixture():
    """全テストで自動的に実行されるフィクスチャ"""
    print("\nAuto fixture: setup")
    yield
    print("\nAuto fixture: teardown")


class TestFixtureScopes:
    def test_combined_fixtures(
        self, global_data, module_data, class_data, function_data
    ):
        print("\nTest execution")
        assert global_data["start_time"]
        assert module_data["module"] == "test"
        assert class_data["class"] == "TestClass"
        assert function_data["function"] == "test"


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


# 前提条件のスキップ
class TestCalculatorWithSkip:
    @pytest.mark.skip(reason="このテストは一時的にスキップ")
    def test_skipped(self):
        assert False

    @pytest.mark.skipif(1 + 1 == 2, reason="条件に基づいてスキップ")
    def test_conditional_skip(self):
        assert False


class TestPlatformSpecific:
    @pytest.mark.skipif(sys.platform != "win32", reason="Windows専用のテスト")
    def test_windows_only(self):
        # Windowsでのみ実行されるテスト
        assert True

    @pytest.mark.skipif(
        tuple(map(int, platform.python_version_tuple())) > (3, 11),
        reason="Python 3.11以上なら",
    )
    def test_newer_python(self):
        # Python 3.11以下でのみ実行
        assert True

    @pytest.mark.skip(reason="Issue #123の修正待ち")
    def test_pending_feature(self):
        # 未実装機能のテスト
        pass


# 非同期テスト
class TestAsync:
    @pytest.mark.asyncio
    async def test_async_operation(self):
        async def async_add(x, y):
            await asyncio.sleep(1.1)  # 非同期処理をシミュレート
            return x + y

        result = await async_add(1, 2)
        assert result == 3


class TestAsyncFixtures:
    @pytest.fixture
    async def async_fixture(self):
        # セットアップ
        await asyncio.sleep(0.1)
        yield "async data"
        # クリーンアップ
        await asyncio.sleep(0.1)

    @pytest.mark.asyncio
    async def test_with_async_fixture(self, async_fixture):
        async for data in async_fixture:
            assert data == "async data"


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


# パラメータ化されたフィクスチャ
class TestParametrizedFixtures:
    @pytest.fixture(params=[1, 2, 3])
    def numbers(self, request):
        return request.param

    def test_with_parametrized_fixture(self, numbers):
        assert numbers in [1, 2, 3]


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
