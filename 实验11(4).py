def caculate_average(*args):
    if not args:
        return 0
    return sum(args)/len(args)

print(f'平均数为:{caculate_average(1,2,4,88)}')
