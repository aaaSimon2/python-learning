import random
import time
from datetime import datetime
def guess_number_game():
    while True:
        start_choice = input("是否开始游戏（输入 y 开始，n 退出）：").strip().lower()
        if start_choice == 'n':
            print("游戏退出，再见！")
            break
        elif start_choice != 'y':
            print("输入无效，请重新输入！")
            continue
        target = random.randint(0, 99)
        start_time = time.time()
        start_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"游戏开始时间：{start_datetime}")
        guess_count = 0
        while True:
            try:
                guess = int(input("请猜一个 0-99 之间的整数："))
                guess_count += 1
                if guess < target:
                    print("大一点")
                elif guess > target:
                    print("小一点")
                else:
                    end_time = time.time()
                    elapsed = end_time - start_time
                    end_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    if elapsed < 5:
                        grade = "S"
                    elif elapsed < 10:
                        grade = "A"
                    elif elapsed < 20:
                        grade = "B"
                    elif elapsed < 30:
                        grade = "C"
                    else:
                        grade = "D"
                    print(f"恭喜猜对！目标数字是 {target}，共猜了 {guess_count} 次")
                    print(f"游戏结束时间：{end_datetime}")
                    print(f"总耗时：{elapsed:.2f} 秒，评级：{grade}")
                    break
            except ValueError:
                print("输入无效，请输入整数！")


if __name__ == '__main__':
    guess_number_game()