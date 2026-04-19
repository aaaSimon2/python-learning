import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime


class ScrollableFrame(tk.Frame):
    """可滚动的Frame容器：解决内容太多显示不全的问题"""

    def __init__(self, container, *args, **kwargs):
        super().__init__(container,*args, **kwargs)

        # 创建画布（用来承载可滚动内容）和垂直滚动条
        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)

        # 真正装内容的内部Frame（放在画布上）
        self.scrollable_frame = tk.Frame(self.canvas)

        # 当内部Frame框架大小变化时，画布的滚动范围对应增大
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # 把内部Frame放到画布的左上角，后续可将内容填进内部框架
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        # 让画布和滚动条对应着滑动
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        #yscrollcommand：指定画布的垂直滚动回调函数
        #self.scrollbar.set：滚动条的set方法，作用是：当画布滚动时，同步更新滚动条的位置

        # 布局：画布占满左边，滚动条占右边
        self.canvas.grid(row=0, column=0, sticky="nsew")  # nsew=上下左右填满
        self.scrollbar.grid(row=0, column=1, sticky="ns")  # ns=上下填满，左右不填

        # 配置权重：让画布能随窗口拉伸
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


class MoodTrackerApp:
    """主程序"""

    def __init__(self):
        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("心情记录系统")  # 窗口标题
        self.root.geometry("517x760")  # 设置窗口初始大小
        self.deleting_in_progress = False  # 标记是否正在删除，防止重复点击删除按钮
        self.edit_window = set()  #标记是否已经点开，防止重复弹出一个编辑窗口

        # 16个可选的颜色（表示面向对象此刻的心情）
        self.color_palette = [
            "#2C003E", "#8B0000", "#0A2463", "#2F4F4F",
            "#C2185B", "#1A237E", "#2E7D32", "#4A148C",
            "#1976D2", "#FF8F00", "#D81B60", "#43A047",
            "#29B6F6", "#FF80AB", "#81C784", "#FFF176"
        ]

        # 保存记录的文件（json格式，方便读写）
        self.data_file = "mood_data.json"
        # 加载已保存的记录（首次运行没有文件则返回空列表）
        self.records = self.load_records()
        self.record_window = None  # 查看所有记录的窗口，初始为空
        self.record_rows = []  # 存储每条记录的行框架，用于搜索高亮显示（即提示为所搜的内容）

        # 初始化界面组件变量（后续进行赋值）
        self.mood_var = None
        self.color_var = None
        self.note_text = None
        self.search_var = None

        # 搭建主界面
        self.setup_ui()

    def load_records(self):
        """加载保存的记录：从json文件里读数据"""
        # 检查文件是否存在，不存在则返回空列表
        if not os.path.exists(self.data_file):
            return []
        try:
            # 打开文件并读取所有旧数据存给self.records（encoding='utf-8'防止中文乱码）
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)#把json数据转化为python数据
        # 异常：JSON文件格式错误（比如手动改了文件内容、文件损坏）
        except json.JSONDecodeError:
            tk.messagebox.showerror("错误", "文件遭到损坏，请重新进行记录。我们正在尽力修复丢失数据")
            return []
        # 异常：文件操作错误（比如权限不足、文件被删除、路径错误）
        except IOError:
            tk.messagebox.showerror("错误", "文件因权限不足、文件被"
                    "删除、路径错误等原因出现错误，请重新进行记录。我们正在尽力修复丢失数据")
            return []

    def save_records(self):
        """保存记录：把数据写入json文件"""
        try:
            # 打开文件并写入已完成更新的self.records内容
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.records, f,indent=2,ensure_ascii=False)#将python数据转化为json数据存入
            return True
        # 捕获文件操作和JSON序列化的异常
        except (IOError, TypeError, ValueError) as e:
            print(f"保存记录失败：{e}")
            return False

    def setup_ui(self):
        """搭建主界面"""
        # 主框架（把所有组件放里面，避免直接贴窗口边缘）
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)  # 填满窗口且允许拉伸

        # 标题
        tk.Label(main_frame, text="随意", font=("Arial", 16, "bold")).pack(pady=(0, 20))

        # 输入区域（带边框的框架）
        input_section = tk.LabelFrame(main_frame, padx=15, pady=15)
        input_section.pack(fill="x", pady=(0, 15))  # 只横向填满

        # 1. 心潮高度（滑动条，范围1-10）
        tk.Label(input_section, text="心潮高度(1-10):", width=15,anchor="w").grid(row=0, column=0, pady=5,sticky="w")
        self.mood_var = tk.IntVar(value=5)  # 初始值5
        tk.Scale(input_section, from_=1, to=10, orient="horizontal",
                 variable=self.mood_var, length=290).grid(row=0, column=1,columnspan=3, pady=5, sticky="w")

        # 2. 内心投色（16个颜色块+单选按钮）
        tk.Label(input_section, text="内心投色:", width=15, anchor="w").grid(row=1, column=0, pady=10, sticky="nw")
        color_select_frame = tk.Frame(input_section)
        color_select_frame.grid(row=1, column=1, columnspan=3, sticky="w", pady=10)

        self.color_var = tk.IntVar(value=0)  # 初始选中第0个颜色
        for i, code in enumerate(self.color_palette):
            # 每行放4个颜色：i//4=行号，取整，i%4=列号，取余(4X4排布)
            row = i // 4
            col = i % 4

            # 每个颜色的小框架（放颜色块+单选按钮）
            color_cell = tk.Frame(color_select_frame)
            color_cell.grid(row=row, column=col, padx=3, pady=3)

            # 用标签显示可选颜色块
            tk.Label(color_cell, bg=code, width=9, height=3, relief="solid", borderwidth=1).pack()
            # 单选按钮（后续通过索引获取对应颜色块并填进表格中）
            tk.Radiobutton(color_cell, variable=self.color_var, value=i).pack()

        # 3. 备注（创建多行文本框）
        tk.Label(input_section, text="随笔:", width=15, anchor="w").grid(row=2, column=0, pady=10, sticky="nw")
        self.note_text = tk.Text(input_section, width=40, height=4)
        self.note_text.grid(row=2, column=1, columnspan=3, pady=10, sticky="w")

        # 4. 按钮
        # 添加记录按钮
        tk.Button(input_section, text="添加记录", command=self.add_record,
                  bg="#4CAF50", fg="white", width=15).grid(row=3, column=0, columnspan=2, pady=10, padx=5)
        # 查看所有记录按钮
        tk.Button(input_section, text="查看所有记录", command=self.show_records,
                  width=15).grid(row=3, column=2, columnspan=2, pady=10, padx=5)


    def add_record(self):
        """添加入表格的功能函数"""
        # 获取用户输入的内容
        mood_value = self.mood_var.get()  # 滑动条的心情值
        color_index = self.color_var.get()  # 选中的颜色的索引
        # 备注文本：1.0=第1行第0列，end-1c=末尾去掉换行符，strip()去掉首尾空格(即从第头到尾获取所有文字内容)
        note_content = self.note_text.get("1.0", "end-1c").strip()

        # 根据索引获取颜色码
        color_code = self.color_palette[color_index]

        # 组装新记录（字典格式）
        new_record = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),  # 当前时间（年-月-日 时:分）
            "mood": mood_value,
            "color_index": color_index,
            "color_code": color_code,
            "note": note_content
        }

        # 把新记录加入列表，保存到文件
        self.records.append(new_record)
        if self.save_records():
            messagebox.showinfo("成功", "记录已保存")
            self.note_text.delete("1.0", "end")  # 清空备注框
            #添加之后，回归默认
            self.mood_var.set(5)
            self.color_var.set(0)

        if self.record_window and self.record_window.winfo_exists():
            self.record_window.destroy()  # 销毁旧窗口
            self.show_records()  #在主窗口点击添加按钮之后，子窗口同步刷新

    def show_records(self):
        """展示所有信息的功能函数"""
        # 没有记录则提示并返回
        if not self.records:
            messagebox.showinfo("提示", "还没有任何记录")
            return

        # 如果记录窗口已存在，先销毁（避免打开多个）
        if self.record_window and self.record_window.winfo_exists():
            self.record_window.destroy()


        # tk.Toplevel创建顶级子窗口存放记录
        self.record_window = tk.Toplevel(self.root)
        self.record_window.title("所有心情记录")
        self.record_window.geometry("800x550")

        # 配置窗口权重：为第1行的滚动框架预留拉伸空间，让设置的框架撑到定义的窗口的大小
        self.record_window.grid_rowconfigure(1, weight=1)
        self.record_window.grid_columnconfigure(0, weight=1)

        # 搜索区域
        search_frame = tk.Frame(self.record_window, padx=10, pady=10)
        search_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        tk.Label(search_frame, text="搜索时间:", height=1).grid(row=0, column=0, sticky="w")
        self.search_var = tk.StringVar()  # 搜索框的输入内容
        tk.Entry(search_frame, textvariable=self.search_var, width=35, borderwidth=2).grid(row=0, column=1, padx=5)

        # 搜索按钮
        tk.Button(search_frame, text="搜索", width=5, height=1, command=self.search_by_time,
                  bg="#2196F3", fg="white").grid(row=0, column=2, padx=2)
        # 清除高亮按钮
        tk.Button(search_frame, text="清除高亮", width=10, height=1, command=self.clear_highlight).grid(row=0, column=3, padx=2)

        # 创建滚动框架（用我们自定义的ScrollableFrame）（放入预留空间）
        scroll_frame = ScrollableFrame(self.record_window)
        scroll_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        #  绘制记录表格,后续存储每一行
        self.record_rows = []  # 清空之前的行记录

        # 表头框架
        header_frame = tk.Frame(scroll_frame.scrollable_frame, bg="#f0f0f0", height=35)
        header_frame.grid(row=0, column=0, columnspan=5, sticky="ew")

        # 列宽：时间、心情值、颜色块、随笔、删除按钮
        col_widths = [150, 80, 140, 230, 80]

        # 配置列宽（固定表头与其对应的具体内容的最小列宽）
        for col, width in enumerate(col_widths):
            header_frame.grid_columnconfigure(col, minsize=width)
            scroll_frame.scrollable_frame.grid_columnconfigure(col, minsize=width)

        # 表头文字设置
        headers = ["时间", "心潮高度", "内心投色", "备注（点击编辑）", "删除按钮"]
        for col, text in enumerate(headers):
            tk.Label(header_frame, text=text, bg="#f0f0f0",
                     font=("宋体",10, "bold")).grid(row=0, column=col, sticky="w", padx=5)

        # 逐行绘制记录
        for row_idx, record in enumerate(self.records):
            # 每行的框架
            row_frame = tk.Frame(scroll_frame.scrollable_frame, height=40)
            row_frame.grid(row=row_idx + 1, column=0, columnspan=5, sticky="ew", pady=2)
            self.record_rows.append(row_frame)  # 加入行列表

            # 配置每行的列宽
            for col, width in enumerate(col_widths):
                row_frame.grid_columnconfigure(col, minsize=width)

            # 第0列：时间
            tk.Label(row_frame, text=record["time"], anchor="w").grid(
                row=0, column=0, sticky="nsew", padx=5, pady=5)

            # 第1列：心情值
            tk.Label(row_frame, text=str(record["mood"]), anchor="center").grid(
                row=0, column=1, sticky="nsew", padx=5, pady=5)

            # 第2列：颜色块（宽度随心情值变化）
            color_cell = tk.Frame(row_frame)
            color_cell.grid(row=0, column=2, sticky="nsew", padx=3, pady=3)

            # 利用线性映射：计算出不同心潮高度下的颜色块宽度
            min_color_width = 30
            max_color_width = 110
            max_mood_level=10
            min_mood_level=1
            mix_width = (min_color_width + (record["mood"] - min_mood_level) *
                           (max_color_width -min_color_width) // max_mood_level-min_mood_level)
            # 绘制颜色块
            tk.Frame(color_cell, bg=record["color_code"],
                     width=mix_width, height=25).pack(side="left", padx=4, pady=4)

            # 第3列：设置备注简短显示
            note_frame = tk.Frame(row_frame)
            note_frame.grid(row=0, column=3, sticky="nsew", padx=2, pady=2)
            # 备注超过15字则截断，加省略号
            note_text = record["note"]
            if len(note_text) > 15:
                note_text = note_text[:15] + "..."
            # 备注标签设置
            note_label = tk.Label(note_frame, text=note_text, anchor="w",justify="left", fg="black")
            note_label.pack(fill="both", expand=True, padx=5, pady=5)
            # 绑定点击事件：点击简短备注打开编辑窗口,并查看备注具体详情（lambda传当前记录索引,调用函数弹出对应窗口）
            note_label.bind("<Button-1>", lambda e, i=row_idx: self.edit_record(i))


            # 第4列：创建删除按钮区域
            btn_frame = tk.Frame(row_frame)
            btn_frame.grid(row=0, column=4, sticky="nsew", padx=5, pady=5)
            # 删除按钮
            del_btn = tk.Button(btn_frame, text="删除", width=8,
                                bg="#f44336", fg="white", borderwidth=1)
            #每次点击获取该行对应索引并调用删除函数删除该行
            del_btn.config(command=lambda idx=row_idx, btn=del_btn: self.delete_record(idx, btn))
            del_btn.pack()

    def search_by_time(self):

        # 获取搜索关键词（搜索成功后有高亮显示）
        keyword = self.search_var.get().strip()
        if not keyword:  # 没输入关键词则返回
            return

        self.clear_highlight()  # 清除之前的高亮,避免用户错意

        # 找出所有包含关键词时间的记录
        matches = []
        for i, record in enumerate(self.records):
            if keyword in record["time"]:
                matches.append(i)

        # 没有匹配的结果则提示
        if not matches:
            messagebox.showinfo("无结果", f"未找到包含 '{keyword}' 的记录")
            return

        # 高亮匹配的行（浅黄色背景）
        for idx in matches:
            if idx < len(self.record_rows):
                self.record_rows[idx].config(bg="#FFF9C4")

        # 提示匹配数量
        messagebox.showinfo("搜索结果", f"找到 {len(matches)} 条匹配记录")

    def clear_highlight(self):

        # 检查是否有记录行，没有则返回
        if not hasattr(self, 'record_rows'):
            return
        # 遍历所有行，恢复默认背景色
        for row in self.record_rows:
            try:
                if row.winfo_exists():  # 检查行是否还存在（避免报错）
                    row.config(bg="SystemButtonFace")  # 恢复系统默认背景色
            except tk.TclError:
                pass

    def edit_record(self, index):
        # 若已点开，直接返回
        if index in self.edit_window:
            return

        # 索引越界（比如记录已删除）则返回
        if index >= len(self.records):
            return

        # 把索引加入集合（表示正在编辑）
        self.edit_window.add(index)

        # 获取要编辑的记录
        record = self.records[index]
        # 创建编辑窗口
        edit_win = tk.Toplevel(self.root)
        edit_win.title("编辑记录")
        edit_win.geometry("500x500")

        # 关闭窗口时，从集合移除索引
        def clear_editing_index():
            # 用discard避免索引不在集合里时报错
            self.edit_window.discard(index)
        # 关闭窗口时，先清除行索引再销毁窗口，用protocol调用两个函数
        edit_win.protocol("WM_DELETE_WINDOW", lambda: [clear_editing_index(), edit_win.destroy()])

        # 心情值（默认显示原有值）
        tk.Label(edit_win, text="心潮高度(1-10):", font=("Arial", 11)).pack(anchor="w",padx=30,  pady=(20, 5))
        mood_var = tk.IntVar(value=record["mood"])
        tk.Scale(edit_win, from_=1, to=10, orient="horizontal",
                 variable=mood_var, length=300).pack(padx=20)

        # 颜色选择（默认显示原有值）
        tk.Label(edit_win, text="内心投色:", font=("Arial", 11)).pack(anchor="w", padx=30, pady=(15, 5))
        color_frame = tk.Frame(edit_win)
        color_frame.pack(padx=30, pady=5)

        # 如果因特殊原因没有这个值，则默认返回0
        color_var = tk.IntVar(value=record.get("color_index", 0))
        for i, code in enumerate(self.color_palette):
            row = i // 8  # 每行放8个颜色
            col = i % 8
            cell = tk.Frame(color_frame)
            cell.grid(row=row, column=col, padx=2, pady=2)
            tk.Label(cell, bg=code, width=4, height=1).pack()
            tk.Radiobutton(cell, variable=color_var, value=i).pack()

        # 备注（默认填充原有内容）
        tk.Label(edit_win, text="随笔:", font=("Arial", 11)).pack(anchor="w", padx=30, pady=(15, 5))
        note_text = tk.Text(edit_win, width=50, height=8)
        note_text.pack(padx=30, pady=5)
        note_text.insert("1.0", record["note"])  # 插入原有备注

        # 保存修改（防连点处理：点击后禁用按钮，避免重复提交）
        def save_changes():
            # 禁用保存按钮
            save_btn.config(state="disabled")
            try:
                # 更新记录内容
                self.records[index]["mood"] = mood_var.get()
                color_index = color_var.get()
                self.records[index]["color_index"] = color_index
                self.records[index]["color_code"] = self.color_palette[color_index]
                self.records[index]["note"] = note_text.get("1.0", "end-1c").strip()

                # 保存到文件，成功则提示并更新记录窗口
                if self.save_records():
                    messagebox.showinfo("成功", "记录已更新")
                    self.edit_window.discard(index)
                    # 保存成功后，从集合移除索引
                    edit_win.destroy()  # 关闭编辑窗口
                    if self.record_window and self.record_window.winfo_exists():
                        self.record_window.destroy()
                        self.show_records()  # 重新显示记录
            finally:
                # 无论是否达成目的，只要按钮还存在就恢复可用（避免窗口销毁后报错）
                if save_btn.winfo_exists():
                    save_btn.config(state="normal")

        # 保存修改按钮
        save_btn = tk.Button(edit_win, text="保存修改", command=save_changes,
                  bg="#4CAF50", fg="white", width=20)
        save_btn.pack(pady=20)

    def delete_record(self, index, button=None):
        """删除记录：点击删除按钮执行"""
        # 正在删除中（比如还没点确认），则返回（防连点）
        if self.deleting_in_progress:
            return

        # 标记开始删除
        self.deleting_in_progress = True
        # 禁用删除按钮（防连点）
        if button:
            button.config(state="disabled")

        try:
            # 弹出确认框：点击“是”执行删除程序，“否”则结束函数
            if not messagebox.askyesno("确认", "确定要删除这条记录吗？"):
                return
            # 删除记录并保存
            del self.records[index]
            self.save_records()

            # 刷新记录窗口
            if self.record_window and self.record_window.winfo_exists():
                self.record_window.destroy()
                self.show_records()
        finally:
            # 无论是否达成目的，恢复状态
            self.deleting_in_progress = False
            # 如果按钮还存在，恢复按钮
            if button and button.winfo_exists():
                button.config(state="normal")

def main():
    app = MoodTrackerApp()  # 创建主程序实例
    app.root.mainloop()     # 启动窗口的消息循环

# 只有直接运行这个文件时，才执行main()
if __name__ == "__main__":
    main()

