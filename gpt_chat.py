from gpt_chat import OpenAI
import os

# ===================== 配置区域 =====================
# 方式1：直接填写API密钥（快速测试用）
API_KEY = "你的OpenAI API密钥"
# 方式2：从系统环境变量读取（更安全，推荐）
# API_KEY = os.getenv("OPENAI_API_KEY")

# 模型选择（gpt-3.5-turbo/gpt-4等）
MODEL = "gpt-3.5-turbo"
# 系统角色设定（定义AI的行为）
SYSTEM_PROMPT = "你是一个友好的AI助手，回答简洁明了，用中文沟通。"
# ====================================================

def init_openai_client():
    """初始化OpenAI客户端"""
    try:
        client = OpenAI(api_key=API_KEY)
        # 测试连接（可选）
        client.models.list()
        print("✅ OpenAI客户端初始化成功！")
        return client
    except Exception as e:
        print(f"❌ 客户端初始化失败：{str(e)}")
        return None

def chat_with_gpt(client, messages):
    """调用GPT API进行对话"""
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.7,  # 回答随机性，0-2之间
            max_tokens=1000   # 最大生成令牌数
        )
        # 提取AI的回复
        ai_reply = response.choices[0].message.content.strip()
        return ai_reply, messages
    except Exception as e:
        error_msg = f"❌ API调用失败：{str(e)}"
        print(error_msg)
        return error_msg, messages

def main():
    """主函数：交互式对话"""
    # 初始化客户端
    client = init_openai_client()
    if not client:
        return

    # 初始化对话历史（包含系统角色）
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    print("🎉 GPT对话窗口已打开，输入'退出'可结束对话\n")

    # 循环接收用户输入
    while True:
        user_input = input("我：")
        if user_input.strip() in ["退出", "q", "quit"]:
            print("👋 对话结束！")
            break
        if not user_input.strip():
            print("⚠️ 请输入有效内容！")
            continue

        # 添加用户消息到对话历史
        messages.append({"role": "user", "content": user_input})
        # 调用GPT获取回复
        ai_reply, messages = chat_with_gpt(client, messages)
        # 打印AI回复并添加到对话历史
        print(f"GPT-4：{ai_reply}\n")
        messages.append({"role": "assistant", "content": ai_reply})

if __name__ == "__main__":
    main()