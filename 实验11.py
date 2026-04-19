def caculate(a,b):
    addtion=a+b
    subtraction=a-b
    multiplication=a*b
    division=a/b
    return addtion,subtraction,multiplication,division
num1=float(input('请输入数字:'))
num2=float(input('请输入数字:'))
add,sub,mul,div=caculate(num1,num2)
print(f'Addtion result:{add}')
print(f'Subtraction result:{sub}')
print(f'Multiplication result:{mul}')
print(f'Division result:{div}')

