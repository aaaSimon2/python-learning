student_list=[]
num=input('请输入姓名:')
name=input('请输入学号:')
sex=input('请输入性别:')
cla=input('请输入班级:')
phone=input('请输入电话:')
def student_inf:
    while True:
        begin=input('按1添加信息,按2删除信息,按3查看所有人信息，按4查看指定人的信息:')
        if begin==1:
            def stu_append(num,name,sex,cla,phone):
            print(f'学号: {num}',f'姓名:{name}',f'性别:{sex}',f'班级:{cla}',f'电话:{phone}')
        f=open('student.txt','a',encoding='utf-8')
        for line in f:
            print(stu_append,end=' ')
        f.close()
