import time
from datetime import datetime
FILE_PATH='emotion_list.txt'
times=1
def load_emotion():
    emotion = []
    try:
        with open(FILE_PATH,'r',encoding='utf-8')as f:
            for line in f:
                if line:
                    day,num,color=line.strip().split(',')
                    emotion.append({'day':day,
                                    'num':num,
                                   'color':color})
    except FileNotFoundError:
        pass
    return emotion
def save_emotion(emotion):
    with open(FILE_PATH,'w',encoding='UTF-8')as f:
        for emo in emotion:
            line=f'{emo['day']},{emo["num"]},{emo["color"]}\n'
            f.write(line)
def add_emotion(emotion):
    global times
    try:
        start_time = time.time()
        start_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        emotion=load_emotion()
        day=input('请输入今天天数:')
        num=int(input('请输入从1-10的数字，数字越高代表情绪越激动:'))
        color=input('请输入颜色,红色代表积极，蓝色消极，黄色为中性:')
        emotion.append({'day':day,
                        'num':num,
                        'color':color})
        save_emotion(emotion)
        print('添加成功')
        print(f'开始记录的时间为:{start_datetime}')
        times+=1
    except ValueError:
        print('请输入有效值')
def del_emotion(emotion):
    emotion=load_emotion()
    day=input('请输入要删除的天数:')
    for i in emotion[:]:
        if i['day']==day:
            emotion.remove(i)
            save_emotion(emotion)
            print('删除成功')
            return
        print('今天空空如也......')
def del_emotion_all(emotion):
    emotion=load_emotion()
    emotion.clear()
    save_emotion(emotion)
    print('从零开始')
def show_emotion(emotion):
    end_datetime = datetime.now().strftime("%Y-%m-%d{times} %H:%M:%S")
    print(end_datetime)
    if not emotion:
        print('暂无心情变化')
        return
    print('==心情变化==')
    print(f"{'天数':<6}{'情绪波动数字':<8}{'当天心情':<8}")
    for emo in emotion:
        emotion=load_emotion()
        print(f"{emo['day']:<6}{emo['num']:<8}{emo['color']:<8}")
        print("-" * 30)
def main():
    while True:
        print('\n==情绪记录系统==')
        print('1.写下本次的心情吧')
        print('2.看看一周的心情变化吧')
        print('3.忘却吗?')
        print('4.那是一次错误的记录')
        print('5.退出这次记录')
        choice=input('请输入编号:')
        if choice=='1':
            add_emotion(load_emotion())
        elif choice=='2':
            show_emotion(load_emotion())
        elif choice=='3':
            del_emotion_all(load_emotion())
        elif choice=='4':
            del_emotion(load_emotion())
        elif choice=='5':
            print('系统结束，希望你有美好的一天')
            break
        elif times>=7:
            print('七天已过，自动退出')
            break
        else:
            print('请输入有效数字')
if __name__ == "__main__":
    main()


