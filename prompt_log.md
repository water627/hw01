# AI交互日志
## 一、初始状态
- 项目：八皇后问题求解器
- 环境：MacOS + Python 3.10 + pytest 7.4.3
- 初始代码：已实现回溯法求解器，单元测试全部通过（8皇后解数=92）

## 二、故意引入Bug
### 1. Bug植入位置
src/eight_queens.py 中 is_valid 函数的对角线冲突判断行：
- 原代码：`if positions[r] == col or abs(r - row) == abs(positions[r] - col):`
- 修改后：`if positions[r] == col or abs(r - row) == positions[r] - col:`（删除第二个abs()）

### 2. Bug复现日志
qinzhenzhen@jaeamMacBook-Air hw01 % pytest tests/ -v
============================= test session starts ==============================
platform darwin -- Python 3.12.8, pytest-9.0.2, pluggy-1.6.0 -- /Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12
cachedir: .pytest_cache
rootdir: /Users/qinzhenzhen/Desktop/hw01
plugins: anyio-4.11.0
collected 6 items                                                              

tests/test_queen_solver.py::test_is_valid_column_conflict PASSED         [ 16%]
tests/test_queen_solver.py::test_is_valid_diagonal_conflict FAILED       [ 33%]
tests/test_queen_solver.py::test_is_valid_valid_case PASSED              [ 50%]
tests/test_queen_solver.py::test_solve_eight_queens_8_queens FAILED      [ 66%]
tests/test_queen_solver.py::test_solve_eight_queens_edge_cases FAILED    [ 83%]
tests/test_queen_solver.py::test_solve_eight_queens_invalid_n PASSED     [100%]

=================================== FAILURES ===================================
_______________________ test_is_valid_diagonal_conflict ________________________

    def test_is_valid_diagonal_conflict():
        """测试对角线冲突场景"""
        positions = [0, -1, -1, -1, -1, -1, -1, -1]
>       assert is_valid(positions, 1, 1) is False
E       assert True is False
E        +  where True = is_valid([0, -1, -1, -1, -1, -1, ...], 1, 1)

tests/test_queen_solver.py:13: AssertionError
_______________________ test_solve_eight_queens_8_queens _______________________

    def test_solve_eight_queens_8_queens():
        """验证8皇后解数为92"""
>       assert len(solve_eight_queens(8)) == 92
E       assert 2113 == 92
E        +  where 2113 = len([[0, 1, 2, 3, 4, 5, ...], [0, 1, 2, 3, 4, 6, ...], [0, 1, 2, 3, 4, 7, ...], [0, 1, 2, 3, 5, 6, ...], [0, 1, 2, 3, 5, 7, ...], [0, 1, 2, 3, 6, 4, ...], ...])
E        +    where [[0, 1, 2, 3, 4, 5, ...], [0, 1, 2, 3, 4, 6, ...], [0, 1, 2, 3, 4, 7, ...], [0, 1, 2, 3, 5, 6, ...], [0, 1, 2, 3, 5, 7, ...], [0, 1, 2, 3, 6, 4, ...], ...] = solve_eight_queens(8)

tests/test_queen_solver.py:22: AssertionError
______________________ test_solve_eight_queens_edge_cases ______________________

    def test_solve_eight_queens_edge_cases():
        """测试边界场景：n=1（有解）、n=2（无解）"""
        assert solve_eight_queens(1) == [[0]]
>       assert solve_eight_queens(2) == []
E       AssertionError: assert [[0, 1]] == []
E         
E         Left contains one more item: [0, 1]
E         
E         Full diff:
E         - []
E         + [
E         +     [...
E         
E         ...Full output truncated (4 lines hidden), use '-vv' to show

tests/test_queen_solver.py:27: AssertionError
=========================== short test summary info ============================
FAILED tests/test_queen_solver.py::test_is_valid_diagonal_conflict - assert True is False
FAILED tests/test_queen_solver.py::test_solve_eight_queens_8_queens - assert 2113 == 92
FAILED tests/test_queen_solver.py::test_solve_eight_queens_edge_cases - AssertionError: assert [[0, 1]] == []
========================= 3 failed, 3 passed in 0.06s ==========================

## 三、AI交互过程
### 1. 发给AI的Prompt
### 1. Bug 位置

Bug 在 `is_valid` 的对角线冲突判断这一行（原代码第 16 行）：

```12:18:/Users/qinzhenzhen/Desktop/hw01/src/eight_queens.py
    # 检查列冲突 + 对角线冲突
    for r in range(row):
        if positions[r] == col or abs(r - row) == (positions[r] - col):
            return False
    return True
```

问题是只对行差取了绝对值，而列差没有取绝对值。

---

### 2. 为何从 92 变成 140

- **正确的对角线冲突条件**是：  
  若已有皇后在 \((r, positions[r])\)，候选位置为 \((row, col)\)，则  
  \[
  |r - row| = |positions[r] - col|
  \]
  时表示两皇后在同一条斜对角线上，有冲突。

- **你当前的代码**使用的是：
  \[
  |r - row| = positions[r] - col
  \]
  右边没有绝对值，只覆盖了一个对角方向（例如 “/” 方向），而另一方向（“\”）没有被正确判定为冲突。

- 结果：
  - 有一部分本应被判定为“对角线冲突”的摆放被误认为“合法”，于是被当作解记录下来。
  - 对 8 皇后问题来说，正确解数是 92，但是由于漏判对角线冲突，多算了一批非法棋局，总数变成了 140。

---

### 3. 修复后的完整代码

`src/eight_queens.py` 修复版本如下（关键在对角线条件加上 `abs`）：

```python
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
```

---

### 4. 如何验证问题已解决

你可以按以下两种方式验证：

- **方式一：运行单元测试（推荐）**

在项目根目录（`/Users/qinzhenzhen/Desktop/hw01`）下执行：

```bash
pytest -q
```

现在输出应为 6 个测试全部通过，例如：

```text
......                                                                   [100%]
6 passed in 0.02s
```

- **方式二：直接检查解的数量**

在命令行运行该模块：

```bash
python -m src.eight_queens
```

或直接在 Python 里：

```python
from src.eight_queens import solve_eight_queens
solutions = solve_eight_queens(8)
print(len(solutions))  # 应该输出 92
```

若输出为 **92**，并且 pytest 全绿，说明问题已修复。

### 2. AI的响应总结
- Bug定位：is_valid函数中缺少第二个abs()，导致对角线冲突校验不完整；
- Bug原因：仅检查了行差=列差的对角线（斜率1），未检查行差=-列差的对角线（斜率-1），非法方案被计入，解数从92增至140；
- 修复方案：恢复第二个abs()；
- 验证建议：重新执行pytest tests/ -v，确认所有用例通过。

### 3. AI修复后的核心代码
```python
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
        if positions[r] == col or abs(r - row) == abs(positions[r] - col):
            return False
    return True
