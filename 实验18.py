try:
    weight=float(input('请输入体重(KG):'))
    height=float(input('请输入身高(M):'))
    bmi=weight/(height**2)
except ValueError:
    print('Value Error,请输入有效数字')
except ZeroDivisionError:
    print('ZeroDvisionError,除数不能为0')
else:
    print('else字句:无异常,bmi值为:',bmi)
finally:
    print('finally字句:最后执行')
