# src/eight_queens.py
def is_valid(positions: list[int], row: int, col: int) -> bool:
    """
    判断指定行/列放置皇后是否合法（无列/对角线冲突）
    
    参数:
        positions: 已放置皇后的位置，positions[i]表示第i行皇后的列索引
        row: 待放置皇后的行索引
        col: 待放置皇后的列索引
    
    返回:
        bool: 合法返回True，否则False
    """
    # 检查列冲突 + 对角线冲突
    for r in range(row):
        # 同列冲突或任一方向对角线冲突则不合法
        if positions[r] == col or abs(r - row) == abs(positions[r] - col):
            return False
    return True

def solve_eight_queens(n: int = 8) -> list[list[int]]:
    """
    求解n皇后问题（默认8皇后），返回所有合法摆放方案
    
    参数:
        n: 皇后数量（默认8）
    
    返回:
        list[list[int]]: 所有合法方案列表
    
    异常:
        ValueError: n<1时抛出
    """
    if n < 1:
        raise ValueError("皇后数量n必须≥1")
    
    solutions = []
    positions = [-1] * n  # 初始化位置（-1表示未放置）

    def backtrack(current_row: int):
        """回溯递归：逐行放置皇后"""
        if current_row == n:
            solutions.append(positions.copy())
            return
        
        # 遍历当前行所有列，尝试放置
        for col in range(n):
            if is_valid(positions, current_row, col):
                positions[current_row] = col
                backtrack(current_row + 1)
                positions[current_row] = -1  # 回溯
    
    backtrack(0)
    return solutions

# 本地运行测试
if __name__ == "__main__":
    results = solve_eight_queens()
    print(f"八皇后问题共有 {len(results)} 种合法方案")
    print(f"前3种方案：{results[:3]}")

