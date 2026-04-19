def cacculate(length,width,height):
    volume=length*width*height
    return volume
length=float(input('请输入长度:'))
width=float(input('请输入宽度:'))
height=1
volume=cacculate(length,width,height)
print(f'长方体体积为:{volume}')