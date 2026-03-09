# tests/test_eight_queens.py
import pytest
from src.eight_queens import is_valid, solve_eight_queens

def test_is_valid_column_conflict():
    """测试列冲突场景"""
    positions = [0, 1, -1, -1, -1, -1, -1, -1]
    assert is_valid(positions, 2, 0) is False

def test_is_valid_diagonal_conflict():
    """测试对角线冲突场景"""
    positions = [0, -1, -1, -1, -1, -1, -1, -1]
    assert is_valid(positions, 1, 1) is False

def test_is_valid_valid_case():
    """测试合法放置场景"""
    positions = [0, 4, 7, 5, -1, -1, -1, -1]
    assert is_valid(positions, 4, 2) is True

def test_solve_eight_queens_8_queens():
    """验证8皇后解数为92"""
    assert len(solve_eight_queens(8)) == 92

def test_solve_eight_queens_edge_cases():
    """测试边界场景：n=1（有解）、n=2（无解）"""
    assert solve_eight_queens(1) == [[0]]
    assert solve_eight_queens(2) == []

def test_solve_eight_queens_invalid_n():
    """测试n<1时抛出异常"""
    with pytest.raises(ValueError) as exc:
        solve_eight_queens(0)
    assert "皇后数量n必须≥1" in str(exc.value)
