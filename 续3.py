import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime


class ScrollableFrame(tk.Frame):
    """可滚动的Frame容器 - 修复版本"""
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


class MoodTrackerApp:
    """心情追踪器主应用"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("心情记录系统")
        self.root.geometry("600x810")

        self.color_palette = [
            ("C01", "#145b7d"), ("C02", "#8e453f"), ("C03", "#6a6da9"),
            ("C04", "#867892"), ("C05", "#7C8577"), ("C06", "#da765b"),
            ("C07", "#77ac98"), ("C08", "#ca8687"), ("C09", "#73b9a2"),
            ("C10", "#fcaf17"), ("C11", "#afb4db"), ("C12", "#abc88b"),
            ("C13", "#d5c59f"), ("C14", "#ffce7b"), ("C15", "#f0dc70"),
            ("C16", "#feeeed")
        ]

        self.data_file = "mood_data.json"
        self.records = self.load_records()
        self.record_window = None
        self.record_rows = []

        self.setup_ui()

    def load_records(self):
        """加载记录，兼容所有缺失字段的旧数据"""
        if not os.path.exists(self.data_file):
            return []
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                records = json.load(f)
                for record in records:
                    if "time" not in record:
                        record["time"] = "2024-01-01 00:00"
                    if "mood" not in record:
                        record["mood"] = 5
                    if "color_name" not in record:
                        record["color_name"] = "C01"
                    if "color_code" not in record:
                        record["color_code"] = "#145b7d"
                    if "note" not in record:
                        record["note"] = ""
                return records
        except Exception as e:
            messagebox.showerror("加载失败", f"读取记录出错：{str(e)}")
            return []

    def save_records(self):
        """保存记录到文件"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.records, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            messagebox.showerror("保存失败", f"保存记录出错：{str(e)}")
            return False

    def setup_ui(self):
        """设置主界面"""
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        tk.Label(main_frame, text="心情记录系统", font=("微软雅黑", 16, "bold")).pack(pady=(0, 20))

        input_section = tk.LabelFrame(main_frame, text="新增记录", padx=15, pady=15)
        input_section.pack(fill="x", pady=(0, 15))

        # 心情值
        tk.Label(input_section, text="心潮高度(1-10):", width=15, anchor="w").grid(row=0, column=0, pady=5, sticky="w")
        self.mood_var = tk.IntVar(value=5)
        tk.Scale(input_section, from_=1, to=10, orient="horizontal",
                 variable=self.mood_var, length=300).grid(row=0, column=1, columnspan=3, pady=5, sticky="w")

        # 颜色选择
        tk.Label(input_section, text="内心投色:", width=15, anchor="w").grid(row=1, column=0, pady=10, sticky="nw")
        color_select_frame = tk.Frame(input_section)
        color_select_frame.grid(row=1, column=1, columnspan=3, sticky="w", pady=10)
        self.color_var = tk.StringVar(value="C01")

        for i, (name, code) in enumerate(self.color_palette):
            row = i // 4
            col = i % 4
            color_cell = tk.Frame(color_select_frame)
            color_cell.grid(row=row, column=col, padx=3, pady=3)
            tk.Label(color_cell, bg=code, width=6, height=2, relief="solid", borderwidth=1).pack()
            tk.Radiobutton(color_cell, text="", variable=self.color_var, value=name).pack()

        # 备注
        tk.Label(input_section, text="随笔:", width=15, anchor="w").grid(row=2, column=0, pady=10, sticky="nw")
        self.note_text = tk.Text(input_section, width=40, height=4)
        self.note_text.grid(row=2, column=1, columnspan=3, pady=10, sticky="w")

        # 按钮
        tk.Button(input_section, text="添加记录", command=self.add_record,
                  bg="#4CAF50", fg="white", width=15).grid(row=3, column=0, columnspan=2, pady=10, padx=5)
        tk.Button(input_section, text="查看所有记录", command=self.show_records,
                  width=15).grid(row=3, column=2, columnspan=2, pady=10, padx=5)

    def add_record(self):
        """添加新记录"""
        mood_value = self.mood_var.get()
        color_name = self.color_var.get()
        note_content = self.note_text.get("1.0", "end-1c").strip()

        if not 1 <= mood_value <= 10:
            messagebox.showwarning("输入错误", "心情值必须在1-10之间")
            return

        color_code = dict(self.color_palette)[color_name]
        new_record = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "mood": mood_value,
            "color_name": color_name,
            "color_code": color_code,
            "note": note_content
        }

        self.records.append(new_record)
        if self.save_records():
            messagebox.showinfo("成功", "记录已保存")
            self.note_text.delete("1.0", "end")

    def show_records(self):
        """显示所有记录"""
        if not self.records:
            messagebox.showinfo("提示", "还没有任何记录")
            return

        if self.record_window and self.record_window.winfo_exists():
            self.record_window.destroy()

        self.record_window = tk.Toplevel(self.root)
        self.record_window.title("所有心情记录")
        self.record_window.geometry("800x550")

        self.record_window.grid_rowconfigure(1, weight=1)
        self.record_window.grid_columnconfigure(0, weight=1)

        # 搜索区域
        search_frame = tk.Frame(self.record_window, padx=10, pady=10)
        search_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        tk.Label(search_frame, text="搜索时间:").grid(row=0, column=0, sticky="w")
        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var, width=25).grid(row=0, column=1, padx=5)
        tk.Button(search_frame, text="搜索", command=self.search_by_time,
                  bg="#2196F3", fg="white").grid(row=0, column=2, padx=2)
        tk.Button(search_frame, text="清除高亮", command=self.clear_highlight).grid(row=0, column=3, padx=2)

        # 滚动框架
        scroll_frame = ScrollableFrame(self.record_window)
        scroll_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        # 表格区域
        self.record_rows = []
        col_widths = [150, 80, 120, 250, 100]

        # 表头（替换为中文）
        header_frame = tk.Frame(scroll_frame.scrollable_frame, bg="#f0f0f0", height=35)
        header_frame.grid(row=0, column=0, columnspan=5, sticky="ew")
        for col, width in enumerate(col_widths):
            header_frame.grid_columnconfigure(col, minsize=width)
            scroll_frame.scrollable_frame.grid_columnconfigure(col, minsize=width)

        # 中文表头
        headers = ["时间", "心情值", "颜色", "备注", "操作"]
        for col, text in enumerate(headers):
            tk.Label(header_frame, text=text, bg="#f0f0f0",
                     font=("微软雅黑", 10, "bold")).grid(row=0, column=col, sticky="w", padx=5)

        # 显示记录
        for row_idx, record in enumerate(self.records):
            row_frame = tk.Frame(scroll_frame.scrollable_frame, height=40)
            row_frame.grid(row=row_idx + 1, column=0, columnspan=5, sticky="ew", pady=2)
            self.record_rows.append(row_frame)

            for col, width in enumerate(col_widths):
                row_frame.grid_columnconfigure(col, minsize=width)

            # 时间列
            tk.Label(row_frame, text=record["time"], anchor="w").grid(
                row=0, column=0, sticky="wens", padx=5, pady=5)

            # 心情值列
            tk.Label(row_frame, text=str(record["mood"]), anchor="center").grid(
                row=0, column=1, sticky="wens", padx=5, pady=5)

            # 颜色块列
            color_cell = tk.Frame(row_frame)
            color_cell.grid(row=0, column=2, sticky="wens", padx=3, pady=3)
            min_width = 20
            max_width = 100
            pixel_width = min_width + (record["mood"] - 1) * (max_width - min_width) // 9
            tk.Frame(color_cell, bg=record["color_code"],
                     width=pixel_width, height=25).pack(side="left", padx=4, pady=4)

            # 备注列
            note_frame = tk.Frame(row_frame)
            note_frame.grid(row=0, column=3, sticky="wens", padx=2, pady=2)
            note_text = record["note"] if record["note"] else "无备注"
            if len(note_text) > 50:
                note_text = note_text[:50] + "..."
            note_label = tk.Label(note_frame, text=note_text, anchor="w",
                                  wraplength=col_widths[3] - 20,
                                  justify="left", cursor="hand2", fg="blue")
            note_label.pack(fill="both", expand=True, padx=5, pady=5)
            note_label.bind("<Button-1>", lambda e, i=row_idx: self.edit_record(i))

            # 操作列（Delete改为删除）
            btn_frame = tk.Frame(row_frame)
            btn_frame.grid(row=0, column=4, sticky="wens", padx=5, pady=5)
            tk.Button(btn_frame, text="删除", width=8,
                      command=lambda i=row_idx: self.delete_record(i),
                      bg="#f44336", fg="white").pack()

    def search_by_time(self):
        """按时间搜索记录"""
        keyword = self.search_var.get().strip()
        if not keyword:
            messagebox.showwarning("提示", "请输入搜索关键词（如2025-05）")
            return

        self.clear_highlight()
        matches = [i for i, record in enumerate(self.records) if keyword in record["time"]]

        if not matches:
            messagebox.showinfo("无结果", f"未找到包含 '{keyword}' 的记录")
            return

        for idx in matches:
            if idx < len(self.record_rows):
                self.record_rows[idx].config(bg="#FFF9C4")

        messagebox.showinfo("搜索结果", f"找到 {len(matches)} 条匹配记录")

    def clear_highlight(self):
        """清除所有高亮"""
        if hasattr(self, 'record_rows'):
            for row in self.record_rows:
                try:
                    if row.winfo_exists():
                        row.config(bg="SystemButtonFace")
                except:
                    pass

    def edit_record(self, index):
        """编辑记录"""
        if index >= len(self.records):
            return

        record = self.records[index]
        edit_win = tk.Toplevel(self.root)
        edit_win.title("编辑记录")
        edit_win.geometry("500x500")

        # 心情值
        tk.Label(edit_win, text="心潮高度(1-10):", font=("微软雅黑", 11)).pack(anchor="w", padx=30, pady=(20, 5))
        mood_var = tk.IntVar(value=record["mood"])
        tk.Scale(edit_win, from_=1, to=10, orient="horizontal",
                 variable=mood_var, length=300).pack(padx=30)

        # 颜色选择
        tk.Label(edit_win, text="内心投色:", font=("微软雅黑", 11)).pack(anchor="w", padx=30, pady=(15, 5))
        color_frame = tk.Frame(edit_win)
        color_frame.pack(padx=30, pady=5)
        color_var = tk.StringVar(value=record["color_name"])

        for i, (name, code) in enumerate(self.color_palette):
            row = i // 8
            col = i % 8
            cell = tk.Frame(color_frame)
            cell.grid(row=row, column=col, padx=2, pady=2)
            tk.Label(cell, bg=code, width=4, height=1).pack()
            tk.Radiobutton(cell, text=name, variable=color_var,
                           value=name, font=("微软雅黑", 7)).pack()

        # 备注编辑
        tk.Label(edit_win, text="随笔:", font=("微软雅黑", 11)).pack(anchor="w", padx=30, pady=(15, 5))
        note_text = tk.Text(edit_win, width=50, height=8)
        note_text.pack(padx=30, pady=5)
        note_text.insert("1.0", record["note"])

        # 保存按钮
        def save_changes():
            self.records[index]["mood"] = mood_var.get()
            self.records[index]["color_name"] = color_var.get()
            self.records[index]["color_code"] = dict(self.color_palette)[color_var.get()]
            self.records[index]["note"] = note_text.get("1.0", "end-1c").strip()

            if self.save_records():
                messagebox.showinfo("成功", "记录已更新")
                edit_win.destroy()
                if self.record_window and self.record_window.winfo_exists():
                    self.record_window.destroy()
                    self.show_records()

        tk.Button(edit_win, text="保存修改", command=save_changes,
                  bg="#4CAF50", fg="white", width=20).pack(pady=20)

    def delete_record(self, index):
        """删除记录"""
        if not messagebox.askyesno("确认", "确定要删除这条记录吗？"):
            return

        del self.records[index]
        self.save_records()
        if self.record_window and self.record_window.winfo_exists():
            self.record_window.destroy()
            self.show_records()


def main():
    """程序主入口"""
    app = MoodTrackerApp()
    app.root.mainloop()


if __name__ == "__main__":
    main()