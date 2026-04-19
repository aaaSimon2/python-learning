def get_grade(score):
    if score>=90:
        return 'A'
    elif 80<=score<90:
        return 'B'
    elif 70<=score<80:
        return 'C'
    elif 60<=score<70:
        return 'D'
    else:
        return 'F'
score=float(input('请输入分数:'))
grade=get_grade(score)
print(f'分数:{score}等级：{grade}')