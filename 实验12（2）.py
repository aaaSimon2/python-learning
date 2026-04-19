def count_ways(n):
    """
    递归计算上n个台阶的方法数（一步最多上3个台阶）
    :param n: 台阶总数
    :return: 上台阶的方法数
    """
    if n == 0:
        return 1
    if n < 0:
        return 0
    return count_ways(n - 1) + count_ways(n - 2) + count_ways(n - 3)
result = count_ways(15)
print(f"上15个台阶的方法数为：{result}")