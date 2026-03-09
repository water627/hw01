# src/queen_solver.py

def solve_queen(n):
    solutions = []  # 存储所有解
    def place_queen(row, cols, diagonals1, diagonals2):
        # 如果所有行都已放置皇后
        if row == n:
            solutions.append(cols)  # 记录解
            return
        for col in range(n):
            # 检查列、对角线是否已被占用
            if col in cols or (row - col) in diagonals1 or (row + col) in diagonals2:
                continue
            # 尝试在当前位置放置皇后
            place_queen(row + 1, cols + [col], diagonals1 + [row - col], diagonals2 + [row + col])

    place_queen(0, [], [], [])  # 从第一行开始放置皇后
    return solutions

# 测试：输出八皇后问题的解
if __name__ == "__main__":
    result = solve_queen(8)
    print(f"Found {len(result)} solutions.")
    for solution in result:
        print(solution)
