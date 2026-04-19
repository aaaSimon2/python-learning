#第一，二题
gen=(x**3 for x in range(1,11) if x % 2 == 0)
print('next()获取的元素:')
print(next(gen))
print(next(gen))
print(next(gen))
#第三题
print('for循环遍历剩余元素:')
for num in gen:
    print(num)
#第四题
gen_new=(x**3 for x in range(1,11)if x % 2 == 0)
result_tuple=tuple(gen_new)
print('转换后的元组:',result_tuple)
