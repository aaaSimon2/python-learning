students = ("小明", "小红", "小刚", "小芳")
chinese_scores = (88,95,78,85)
math_scores = (92,89,90,87)
#第一题
print('学生列表:')
for idx, name in enumerate(students, start=1):
    print(f"第{idx}名：{name}")
#第二题
student_score_pairs = tuple(zip(students, chinese_scores, math_scores))
print("\n组合后的元组：", student_score_pairs)
#第三题
def get_total(chinese, math):
    return chinese + math
total_scores = tuple(map(get_total, chinese_scores, math_scores))
print("\n学生总分：", total_scores)