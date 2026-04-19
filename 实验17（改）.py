FILE_PATH = "student_list.txt"

def load_students():
    """从文件中读取学生信息，返回列表（每个元素是字典）"""
    students = []
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    sid, name, gender, cls, phone = line.split(",")
                    students.append({
                        "sid": sid,
                        "name": name,
                        "gender": gender,
                        "class": cls,
                        "phone": phone
                    })
    except FileNotFoundError:
        pass
    return students

def save_students(students):
    """将学生信息列表写入文件"""
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        for stu in students:
            line = f"{stu['sid']},{stu['name']},{stu['gender']},{stu['class']},{stu['phone']}\n"
            f.write(line)
def add_student():
    """添加学生信息"""
    students = load_students()
    sid = input("请输入学号：")
    for stu in students:
        if stu["sid"] == sid:
            print("该学号已存在！")
            return
    name = input("请输入姓名：")
    gender = input("请输入性别：")
    cls = input("请输入班级：")
    phone = input("请输入电话：")
    students.append({
        "sid": sid,
        "name": name,
        "gender": gender,
        "class": cls,
        "phone": phone
    })
    save_students(students)
    print("添加成功！")

def delete_student():
    """删除指定学号的学生信息"""
    students = load_students()
    sid = input("请输入要删除的学生学号：")
    for i, stu in enumerate(students):
        if stu["sid"] == sid:
            del students[i]
            save_students(students)
            print("删除成功！")
            return
    print("未找到该学号的学生！")

def show_all_students():
    """查看所有学生信息"""
    students = load_students()
    if not students:
        print("暂无学生信息！")
        return
    print(f"{'学号':<5} {'姓名':<5} {'性别':<3} {'班级':<3} {'电话':<11}")
    print("-" * 30)
    for stu in students:
        print(f"{stu['sid']:<5} {stu['name']:<5} {stu['gender']:<3} {stu['class']:<3} {stu['phone']:<11}")

def show_single_student():
    """查看指定学号的学生信息"""
    students = load_students()
    sid = input("请输入要查询的学生学号：")
    for stu in students:
        if stu["sid"] == sid:
            print("学生信息：")
            print(f"学号：{stu['sid']}")
            print(f"姓名：{stu['name']}")
            print(f"性别：{stu['gender']}")
            print(f"班级：{stu['class']}")
            print(f"电话：{stu['phone']}")
            return
    print("未找到该学号的学生！")

def main():
    """主菜单，实现交互式操作"""
    while True:
        print("\n=== 学生信息管理系统 ===")
        print("1. 添加学生信息")
        print("2. 删除学生信息")
        print("3. 查看所有学生信息")
        print("4. 查看指定学生信息")
        print("5. 退出系统")
        choice = input("请输入操作编号：")
        if choice == "1":
            add_student()
        elif choice == "2":
            delete_student()
        elif choice == "3":
            show_all_students()
        elif choice == "4":
            show_single_student()
        elif choice == "5":
            print("系统已退出！")
            break
        else:
            print("输入无效，请重新选择！")

if __name__ == "__main__":
    main()