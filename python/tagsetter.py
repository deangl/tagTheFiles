"""
Tag Setter Application

一个用于管理和设置文件标签及描述信息的图形界面工具。
主要功能：
1. 通过文件路径参数启动，自动定位关联的 filetag.tag 文件
2. 提供界面用于编辑文件的标签（Tags）和详细说明（Description）
3. 支持保存修改到 tag 文件中
4. 支持键盘导航：Tab 键切换焦点，Enter 键触发按钮操作

具体用法示例：
1. 通过命令行直接调用（最常见用法）：
   python tagsetter.py "C:\\项目\\文档.txt"
   
2. 在文件管理器中对文件右键选择"设置标签"（需要与文件管理器集成）
   
3. 与其他脚本配合使用：
   import subprocess
   subprocess.run(['python', 'tagsetter.py', 'file_path.txt'])

4. 批量处理文件（循环调用）：
   for file in files:
       subprocess.run(['python', 'tagsetter.py', file])

界面操作说明：
- 标签框：输入以空格分隔的多个标签，例如：重要 项目 待审核
- 说明框：输入文件的详细描述信息，支持多行文本
- 保存按钮：点击保存或按Enter键（当按钮获得焦点时）
- 按Tab键在不同控件间切换焦点
- 按Escape键退出程序

依赖模块：
- tkinter: 用于构建图形用户界面
- pathlib: 用于路径操作
- tagutils: 自定义工具函数，处理 tag 文件的读写操作

文件格式：
tag 文件使用特定格式存储文件的标签和描述信息，支持转义字符处理
"""
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from tagutils import find_tag_file, get_relative_path, read_tag_file, write_tag_file

class TagSetter:
    def __init__(self, file_path):
        self.root = tk.Tk()
        self.root.title("Tag Setter")
        self.root.geometry("1000x1200")
        
        self.file_path = file_path
        self.tag_file = None
        self.all_tags = {}
        self.relative_path = None
        
        # 查找tag文件
        self.find_tag_file()
        
        if not self.tag_file:
            messagebox.showerror("错误", "找不到 filetag.tag")
            sys.exit(1)
        
        # 读取标签文件
        self.read_tag_file()
        
        # 创建界面
        self.create_widgets()
        
    def find_tag_file(self):
        """查找tag文件"""
        tag_file_path = find_tag_file(self.file_path)
        if tag_file_path:
            # Convert to Path object
            self.tag_file = Path(tag_file_path)
            # 计算相对路径，以tag文件所在目录为基准
            tag_dir = self.tag_file.parent
            self.relative_path = get_relative_path(self.file_path, tag_dir)
        else:
            self.tag_file = None
    
    def read_tag_file(self):
        """读取标签文件"""
        if not self.tag_file:
            return
        self.all_tags = read_tag_file(str(self.tag_file))
    
    def create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 文件路径 - 在同一行
        file_frame = ttk.Frame(main_frame)
        file_frame.pack(fill=tk.X, pady=(0, 20))
        ttk.Label(file_frame, text="文件：").pack(side=tk.LEFT)
        ttk.Label(file_frame, text=self.relative_path).pack(side=tk.LEFT, padx=5)
        
        # 标签
        ttk.Label(main_frame, text="Tags:").pack(anchor='w', pady=(0, 5))
        self.tag_entry = tk.Text(main_frame, height=5)
        self.tag_entry.pack(fill=tk.X, pady=(0, 20))
        # Bind Tab key to move focus to next widget
        self.tag_entry.bind('<Tab>', self.focus_next_widget)
        
        # 描述
        ttk.Label(main_frame, text="说明：").pack(anchor='w', pady=(0, 5))
        self.desc_entry = tk.Text(main_frame, height=15)
        self.desc_entry.pack(fill=tk.BOTH, expand=True)
        # Bind Tab key to move focus to next widget
        self.desc_entry.bind('<Tab>', self.focus_next_widget)
        
        # 设置现有值
        if self.relative_path in self.all_tags:
            tag_info = self.all_tags[self.relative_path]
            self.tag_entry.insert('1.0', tag_info['tag'])
            self.desc_entry.insert('1.0', tag_info['desc'])
        
        # 保存按钮
        self.save_button = ttk.Button(main_frame, text="保存", command=self.save)
        self.save_button.pack(pady=20)
        
        # tag文件位置 - 在同一行
        tag_file_frame = ttk.Frame(main_frame)
        tag_file_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(tag_file_frame, text="tag文件位置：").pack(side=tk.LEFT)
        ttk.Label(tag_file_frame, text=str(self.tag_file)).pack(side=tk.LEFT, padx=5)
        
        # 绑定事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.bind('<Escape>', lambda e: self.on_close())
        # 绑定回车键到当前焦点按钮
        self.root.bind('<Return>', self.on_return_pressed)
        
        # 为按钮绑定焦点事件
        self.save_button.bind('<FocusIn>', lambda e: self.set_current_focused_button(self.save_button))
    
    def save(self):
        """保存标签信息"""
        tag = self.tag_entry.get('1.0', 'end-1c').strip()
        desc = self.desc_entry.get('1.0', 'end-1c').strip()
        
        # 确保相对路径以.\开头
        relative_path = self.relative_path
        if not relative_path.startswith('.\\'):
            relative_path = '.\\' + relative_path
        
        # 直接存储原始内容，write_tag_file 会处理转义
        self.all_tags[relative_path] = {'tag': tag, 'desc': desc}
        
        # 写入文件，使用公共函数
        if write_tag_file(str(self.tag_file), self.all_tags):
            messagebox.showinfo("成功", "保存成功")
            self.root.destroy()
        else:
            messagebox.showerror("错误", "保存时出错")
    
    def on_close(self):
        """关闭窗口"""
        self.root.destroy()
        sys.exit(0)
    
    def focus_next_widget(self, event):
        """Move focus to next widget on Tab key press"""
        event.widget.tk_focusNext().focus()
        return "break"  # Prevent default Tab behavior
    
    def set_current_focused_button(self, button):
        """Set the currently focused button"""
        self.current_focused_button = button
    
    def on_return_pressed(self, event):
        """Handle Return key press to trigger the focused button's action"""
        # Get the currently focused widget
        focused_widget = self.root.focus_get()
        # If it's a button, invoke its command
        if isinstance(focused_widget, ttk.Button):
            focused_widget.invoke()
        return "break"
    
    def run(self):
        """运行应用程序"""
        self.root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        messagebox.showerror("错误", "请提供文件路径作为参数")
        sys.exit(1)
    
    app = TagSetter(sys.argv[1])
    app.run()
