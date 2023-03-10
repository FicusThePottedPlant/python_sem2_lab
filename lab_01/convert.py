import math


def int_to2(num: int) -> int:
    """Перевод целого 10-го числа в 2-ую"""
    num = int(num)
    res = ''
    while num > 0:
        res = str(num % 2) + res
        num //= 2
    return res if res else 0


def int_to10(num: int) -> int:
    """Перевод целого 2-го числа в 10-ую"""
    num = int(num)
    return int(str(num), 2)


def trunc_float_to2(truncated):
    """Перевод дробной части вещественного 10-го числа в 2-ую"""
    res = ''
    truncated = float(f'0.{truncated}')
    while truncated and len(res) != 10:
        truncated *= 2
        res += str(math.trunc(truncated))
        truncated = truncated - math.trunc(truncated)
    return res


def float_to2(num: str) -> str:
    """Перевод вещественного 10-го числа в 2-ую"""
    if num.isalnum():
        return str(int_to2(num))
    num, truncated = num.split('.')
    num2 = int_to2(num)
    res = trunc_float_to2(truncated)
    return f'{num2}.{res}' if res else f'{num2}'


def trunc_float_to10(truncated):
    """Перевод дробной части вещественного 2-го числа в 10-ую"""
    res = 0
    for i, j in enumerate(str(truncated)):
        res += (2 ** (-i - 1) * int(j))
    return res


def float_to10(num: str) -> str:
    """Перевод вещественного 2-го числа в 10-ую"""
    if num.isalnum():
        return str(int_to10(num))
    num, truncated = num.split('.')
    num10 = int_to10(num)
    res = trunc_float_to10(truncated)
    return str(num10 + res)
