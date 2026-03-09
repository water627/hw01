import unittest
from src.queen_solver import solve_queen

class TestQueenSolver(unittest.TestCase):
    def test_solution(self):
        solutions = solve_queen(8)
        self.assertEqual(len(solutions), 92)  # 八皇后问题的解有92种

if __name__ == "__main__":
    unittest.main()
