#第一题
score_tuple=('语文',92,'数学',88,'英语',95,'物理',85)
print(score_tuple[3])
#第二题
score_only=score_tuple[1::2]
print(score_only)
#第三题
for i in range(0,len(score_tuple),2):
    subject=score_tuple[i]
    score=score_tuple[i+1]
    print(f'{subject}:{score}')

