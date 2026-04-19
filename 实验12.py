def reverse_string(s):
    """
    递归实现字符串倒序
    :param s: 待倒序的字符串
    :return: 倒序后的字符串
    """
    if len(s) <= 1:
        return s
    return reverse_string(s[1:]) + s[0]
input_str = "abcde"
result = reverse_string(input_str)
print(f"输入字符串：{input_str}")
print(f"倒序结果：{result}")
