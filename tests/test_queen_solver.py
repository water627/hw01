# tests/test_queen_solver.py

import unittest
from src.queen_solver import solve_queen

class TestQueenSolver(unittest.TestCase):

    def test_solution(self):
        # 测试八皇后问题的解
        solutions = solve_queen(8)
        self.assertEqual(len(solutions), 92)  # 八皇后问题的解有92种

    def test_empty(self):
        # 测试没有棋盘的情况
        solutions = solve_queen(0)
        self.assertEqual(solutions, [])  # 0皇后没有解

if __name__ == "__main__":
    unittest.main()
