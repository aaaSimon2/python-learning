attempts = 0
max_attempts = 3
while attempts < max_attempts:
    name = input("请输入姓名（2-6位中文）：")
    if not (2 <= len(name) <= 6 and all('\u4e00' <= c <= '\u9fa5' for c in name)):
        print("姓名格式错误，需2-6位中文！")
        attempts += 1
        continue
    id_card = input("请输入身份证号码：")
    if len(id_card) != 18 or not (id_card[:17].isdigit() and (id_card[-1].isdigit() or id_card[-1].upper() == 'X')):
        print("身份证格式错误，需18位，前17位数字，最后一位数字或X！")
        attempts += 1
        continue
    phone = input("请输入手机号码：")
    if not (len(phone) == 11 and phone.isdigit()):
        print("手机号格式错误，需11位纯数字！")
        attempts += 1
        continue
    email = input("请输入邮箱：")
    at_index = email.find('@')
    dot_index = email.find('.', at_index)
    if at_index == -1 or dot_index == -1:
        print("邮箱格式错误，需包含@和.，且.在@之后！")
        attempts += 1
        continue
    print(f"姓名：{name}")
    print(f"身份证号码：{id_card}")
    print(f"手机号码：{phone}")
    print(f"邮箱：{email}")
    break
else:
    print("超过最大重试次数，程序结束。")