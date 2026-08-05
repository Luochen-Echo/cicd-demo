"""math_utils —— 一个用于练习 CI/CD 的最小数学工具包。"""


def add(a: float, b: float) -> float:
    """返回两个数之和。"""
    return a + b


def subtract(a: float, b: float) -> float:
    """返回 a 减 b。"""
    return a - b


def multiply(a: float, b: float) -> float:
    """返回两个数之积。"""
    return a * b


def divide(a: float, b: float) -> float:
    """返回 a 除以 b，b 为 0 时抛出 ValueError。"""
    if b == 0:
        raise ValueError("除数不能为 0")
    return a / b
