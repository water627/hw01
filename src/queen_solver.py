# src/queen_solver.py

def solve_queen(n):
    solutions = []
    
    def place_queen(row, cols, diagonals1, diagonals2):
        if row == n:
            solutions.append(cols)  # 记录解
            return
        
        for col in range(n):
            if col in cols or (row - col) in diagonals1 or (row + col) in diagonals2:
                continue
            place_queen(row + 1, cols + [col], diagonals1 + [row - col], diagonals2 + [row + col])

    place_queen(0, [], [], [])  # 从第一行开始放置皇后
    return solutions
