import tkinter as tk
from tkinter import messagebox
import sqlite3
import datetime

# 初始化数据库
conn = sqlite3.connect('mood.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS moods
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              date TEXT, time TEXT, mood INTEGER, note TEXT)''')
conn.commit()
conn.close()


class CloudMoodApp:
    def __init__(self, root):
        self.root = root
        self.root.title("云朵心情日记")
        self.root.geometry("500x700")
        self.root.configure(bg='#e6f2ff')

        # 云朵颜色 (乌云到白云)
        self.cloud_colors = [
            "#4a4a4a", "#6a6a6a", "#8a8a8a", "#aaaaaa", "#bababa",
            "#cacaca", "#dadada", "#eaeaea", "#f5f5f5", "#ffffff"
        ]

        # 云朵描述
        self.cloud_texts = [
            "乌云密布", "阴云", "多云", "薄云", "少云",
            "晴间多云", "白云", "阳光白云", "明亮白云", "万里晴空"
        ]

        self.create_widgets()
        self.load_today_moods()

    def create_widgets(self):
        # 标题
        title = tk.Label(self.root, text="☁️ 云朵心情日记",
                         font=("微软雅黑", 24, "bold"), bg='#4a90e2', fg='white')
        title.pack(fill='x', pady=10)

        # 日期显示
        today = datetime.datetime.now().strftime("%Y年%m月%d日")
        date_label = tk.Label(self.root, text=f"📅 {today}",
                              font=("微软雅黑", 12), bg='#e6f2ff')
        date_label.pack(pady=5)

        # 云朵选择
        tk.Label(self.root, text="选择此刻心情:",
                 font=("微软雅黑", 12), bg='#e6f2ff').pack(pady=10)

        self.cloud_frame = tk.Frame(self.root, bg='#e6f2ff')
        self.cloud_frame.pack()

        self.mood_var = tk.IntVar(value=5)
        self.cloud_buttons = []

        for i in range(10):
            btn = tk.Button(self.cloud_frame, text="☁", font=("Arial", 18),
                            bg=self.cloud_colors[i], width=3, height=1,
                            command=lambda x=i: self.select_cloud(x))
            btn.grid(row=0, column=i, padx=2)
            self.cloud_buttons.append(btn)

        # 心情描述
        self.desc_label = tk.Label(self.root, text=self.cloud_texts[5],
                                   font=("微软雅黑", 10), bg='#e6f2ff')
        self.desc_label.pack(pady=5)

        # 文字记录
        tk.Label(self.root, text="记录想法 (可选):",
                 font=("微软雅黑", 12), bg='#e6f2ff').pack(pady=10)

        self.note_text = tk.Text(self.root, height=5, width=40,
                                 font=("微软雅黑", 10))
        self.note_text.pack()

        # 记录按钮
        tk.Button(self.root, text="记录心情", font=("微软雅黑", 14),
                  bg='#4a90e2', fg='white', command=self.save_mood,
                  width=15).pack(pady=20)

        # 今日记录标题
        tk.Label(self.root, text="今日心情记录:",
                 font=("微软雅黑", 12), bg='#e6f2ff').pack(pady=10)

        # 今日记录显示区域
        self.today_frame = tk.Frame(self.root, bg='white')
        self.today_frame.pack(fill='both', expand=True, padx=20, pady=5)

        # 功能按钮
        btn_frame = tk.Frame(self.root, bg='#e6f2ff')
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="查看历史", command=self.view_history,
                  bg='#34c759', fg='white', width=10).pack(side='left', padx=5)
        tk.Button(btn_frame, text="周总结", command=self.weekly_summary,
                  bg='#ff9500', fg='white', width=10).pack(side='left', padx=5)

    def select_cloud(self, index):
        self.mood_var.set(index)
        self.desc_label.config(text=self.cloud_texts[index])
        for i, btn in enumerate(self.cloud_buttons):
            if i == index:
                btn.config(relief='sunken')
            else:
                btn.config(relief='raised')

    def save_mood(self):
        mood = self.mood_var.get()
        note = self.note_text.get("1.0", tk.END).strip()
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M")

        conn = sqlite3.connect('mood.db')
        c = conn.cursor()
        c.execute("INSERT INTO moods (date, time, mood, note) VALUES (?, ?, ?, ?)",
                  (date, time, mood, note))
        conn.commit()
        conn.close()

        self.note_text.delete("1.0", tk.END)
        self.load_today_moods()
        messagebox.showinfo("成功", "心情已记录！")

    def load_today_moods(self):
        # 清空现有内容
        for widget in self.today_frame.winfo_children():
            widget.destroy()

        today = datetime.datetime.now().strftime("%Y-%m-%d")
        conn = sqlite3.connect('mood.db')
        c = conn.cursor()
        c.execute("SELECT time, mood, note FROM moods WHERE date = ? ORDER BY time DESC",
                  (today,))
        records = c.fetchall()
        conn.close()

        if not records:
            label = tk.Label(self.today_frame, text="今天还没有记录哦",
                             font=("微软雅黑", 10), bg='white', fg='gray')
            label.pack(pady=20)
            return

        # 显示记录
        canvas = tk.Canvas(self.today_frame, bg='white')
        scrollbar = tk.Scrollbar(self.today_frame, orient='vertical', command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg='white')

        scroll_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0, 0), window=scroll_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        for i, (time, mood, note) in enumerate(records):
            frame = tk.Frame(scroll_frame, bg='#f0f8ff', relief='solid', bd=1)
            frame.pack(fill='x', padx=5, pady=2)

            # 时间
            tk.Label(frame, text=f"🕒 {time}", bg='#f0f8ff',
                     font=("微软雅黑", 9)).pack(anchor='w', padx=5, pady=2)

            # 云朵和描述
            mood_frame = tk.Frame(frame, bg='#f0f8ff')
            mood_frame.pack(anchor='w', padx=5)

            tk.Label(mood_frame, text="🌞", font=("Arial", 12),
                     bg=self.cloud_colors[mood]).pack(side='left')
            tk.Label(mood_frame, text=self.cloud_texts[mood],
                     bg='#f0f8ff', font=("微软雅黑", 9)).pack(side='left', padx=5)

            # 文字记录
            if note:
                tk.Label(frame, text=f"🌞 {note}", bg='#f0f8ff',
                         font=("微软雅黑", 9), wraplength=350, justify='left'
                         ).pack(anchor='w', padx=5, pady=2)

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def view_history(self):
        history_win = tk.Toplevel(self.root)
        history_win.title("历史记录")
        history_win.geometry("500x600")

        # 获取所有日期
        conn = sqlite3.connect('mood.db')
        c = conn.cursor()
        c.execute("SELECT DISTINCT date FROM moods ORDER BY date DESC")
        dates = c.fetchall()

        # 显示日期列表
        for date_str, in dates:
            date_btn = tk.Button(history_win, text=date_str,
                                 command=lambda d=date_str: self.show_day(d, history_win),
                                 width=20)
            date_btn.pack(pady=2)

        conn.close()

    def show_day(self, date, parent):
        day_win = tk.Toplevel(parent)
        day_win.title(f"{date} 记录")
        day_win.geometry("400x500")

        conn = sqlite3.connect('mood.db')
        c = conn.cursor()
        c.execute("SELECT time, mood, note FROM moods WHERE date = ? ORDER BY time",
                  (date,))
        records = c.fetchall()

        # 计算平均心情
        moods = [r[1] for r in records]
        avg_mood = sum(moods) / len(moods) if moods else 0

        tk.Label(day_win, text=f"平均心情: {self.cloud_texts[int(avg_mood)]}",
                 font=("微软雅黑", 12)).pack(pady=10)

        for time, mood, note in records:
            frame = tk.Frame(day_win, bg='#f0f8ff', relief='solid', bd=1)
            frame.pack(fill='x', padx=10, pady=2)

            tk.Label(frame, text=f"{time}  {self.cloud_texts[mood]}",
                     bg='#f0f8ff').pack(anchor='w', padx=5)
            if note:
                tk.Label(frame, text=note, bg='#f0f8ff', wraplength=350,
                         justify='left').pack(anchor='w', padx=5)

        conn.close()

    def weekly_summary(self):
        # 计算最近7天
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=7)

        conn = sqlite3.connect('mood.db')
        c = conn.cursor()
        c.execute('''SELECT date, AVG(mood) FROM moods 
                     WHERE date BETWEEN ? AND ? GROUP BY date''',
                  (start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")))

        weekly_data = c.fetchall()
        conn.close()

        # 显示周总结
        summary_win = tk.Toplevel(self.root)
        summary_win.title("本周总结")
        summary_win.geometry("400x400")

        tk.Label(summary_win, text="📊 本周心情报告",
                 font=("微软雅黑", 16)).pack(pady=10)

        if weekly_data:
            for date, avg_mood in weekly_data:
                mood_index = int(avg_mood)
                tk.Label(summary_win,
                         text=f"{date}: {self.cloud_texts[mood_index]}",
                         font=("微软雅黑", 10)).pack(pady=2)

            # 建议
            tk.Label(summary_win, text="\n💡 小建议:",
                     font=("微软雅黑", 12)).pack(pady=10)
            tk.Label(summary_win, text="多记录美好时刻\n保持积极心态",
                     font=("微软雅黑", 10), wraplength=350).pack()
        else:
            tk.Label(summary_win, text="本周还没有记录哦",
                     font=("微软雅黑", 12)).pack(pady=50)


# 运行程序
if __name__ == "__main__":
    root = tk.Tk()
    app = CloudMoodApp(root)
    root.mainloop()