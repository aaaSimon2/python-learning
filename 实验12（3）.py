a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
square_func = lambda x: x ** 2
result1 = list(map(square_func, a))
result2 = [lambda x: x ** 2 for x in a]
print("方式1结果：", result1)
print("方式2结果：", result2) 