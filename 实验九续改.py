def validate_name(name):
    """验证姓名：2-6位中文"""
    if 2 <= len(name) <= 6 and all('\u4e00' <= char <= '\u9fa5' for char in name):
        return True
    return False

def validate_id_card(id_card):
    """验证身份证号码：18位，前17位为数字，最后1位为数字或字母X（不区分大小写）"""
    if len(id_card) != 18:
        return False
    front_17 = id_card[:17]
    last_char = id_card[-1].upper()
    if front_17.isdigit() and (last_char.isdigit() or last_char == 'X'):
        return True
    return False

def validate_phone(phone):
    """验证手机号码：11位纯数字"""
    return len(phone) == 11 and phone.isdigit()

def validate_email(email):
    """验证邮箱：包含@符号，且@后包含.符号"""
    at_index = email.find('@')
    if at_index == -1:
        return False
    dot_index = email.find('.', at_index)
    return dot_index != -1

def get_valid_input(prompt, validator, error_msg, max_attempts=3):
    """获取有效输入，带验证和重试机制"""
    attempts = 0
    while attempts < max_attempts:
        user_input = input(prompt)
        if validator(user_input):
            return user_input
        else:
            attempts += 1
            print(error_msg)
    print("超过最大重试次数，程序结束。")
    exit()

# 主程序
print("请输入以下信息（共3次错误机会）：")
name = get_valid_input("请输入姓名（2-6位中文）：", validate_name, "姓名格式错误，请重新输入！")
id_card = get_valid_input("请输入身份证号码：", validate_id_card, "身份证号码格式错误，请重新输入！")
phone = get_valid_input("请输入手机号码：", validate_phone, "手机号码格式错误，请重新输入！")
email = get_valid_input("请输入邮箱：", validate_email, "邮箱格式错误，请重新输入！")

print("\n所有信息格式正确！")
print(f"姓名：{name}")
print(f"身份证号码：{id_card}")
print(f"手机号码：{phone}")
print(f"邮箱：{email}")