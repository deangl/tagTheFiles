import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

class TagSetter:
    def __init__(self, file_path):
        self.root = tk.Tk()
        self.root.title("Tag Setter")
        self.root.geometry("500x600")
        
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
        current_path = Path(self.file_path)
        # 从文件所在目录开始向上查找
        for parent in [current_path.parent] + list(current_path.parents):
            tag_file_path = parent / "filetag.tag"
            if tag_file_path.exists():
                self.tag_file = tag_file_path
                # 计算相对路径，以tag文件所在目录为基准
                try:
                    # 相对路径应该相对于tag文件所在目录
                    self.relative_path = os.path.relpath(self.file_path, parent)
                    # 确保路径使用.\前缀
                    if not self.relative_path.startswith('.\\'):
                        # 如果路径不是以.\开头，检查是否需要添加
                        # 如果路径已经是相对路径，但可能不是相对于当前目录
                        # 我们想要相对于tag文件所在目录的路径
                        # 为了与tagfinder.py保持一致，使用.\前缀
                        self.relative_path = '.\\' + self.relative_path
                except ValueError:
                    # 如果在不同驱动器上，使用绝对路径
                    self.relative_path = self.file_path
                break
    
    def read_tag_file(self):
        """读取标签文件"""
        if not self.tag_file:
            return
        
        try:
            # 使用Windows默认编码，与tagfinder.py保持一致
            with open(self.tag_file, 'r', encoding='mbcs') as f:
                content = f.read()
            
            for line in content.split('\n'):
                line = line.strip()
                if not line or not line.endswith('>>>>'):
                    continue
                
                # Remove the >>>> ending
                line = line[:-4]
                # Split by the separator
                parts = line.split('{<>}')
                if len(parts) >= 3:
                    file_path = parts[0]
                    # 确保路径以.\开头
                    if not file_path.startswith('.\\'):
                        # 如果路径不是以.\开头，检查是否需要转换
                        # 这里我们假设所有路径都应该相对于tag文件所在目录
                        # 所以添加.\前缀
                        file_path = '.\\' + file_path
                    tag = parts[1]
                    desc = parts[2]
                    # Restore newlines
                    tag = tag.replace('@n@', '\n')
                    desc = desc.replace('@n@', '\n')
                    self.all_tags[file_path] = {'tag': tag, 'desc': desc}
        except Exception as e:
            messagebox.showerror("错误", f"读取标签文件时出错: {str(e)}")
    
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
        ttk.Button(main_frame, text="保存", command=self.save).pack(pady=20)
        
        # tag文件位置 - 在同一行
        tag_file_frame = ttk.Frame(main_frame)
        tag_file_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(tag_file_frame, text="tag文件位置：").pack(side=tk.LEFT)
        ttk.Label(tag_file_frame, text=str(self.tag_file)).pack(side=tk.LEFT, padx=5)
        
        # 绑定事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.bind('<Escape>', lambda e: self.on_close())
    
    def save(self):
        """保存标签信息"""
        tag = self.tag_entry.get('1.0', 'end-1c').strip()
        desc = self.desc_entry.get('1.0', 'end-1c').strip()
        
        # 更新标签信息
        # 转义换行符
        tag_escaped = tag.replace('\n', '@n@')
        desc_escaped = desc.replace('\n', '@n@')
        
        # 确保相对路径以.\开头
        relative_path = self.relative_path
        if not relative_path.startswith('.\\'):
            relative_path = '.\\' + relative_path
        self.all_tags[relative_path] = {'tag': tag_escaped, 'desc': desc_escaped}
        
        # 写入文件，与tagfinder.py保持一致
        try:
            # 使用Windows默认编码
            with open(self.tag_file, 'w', encoding='mbcs') as f:
                for path, info in sorted(self.all_tags.items()):
                    # 确保路径以.\开头
                    if not path.startswith('.\\'):
                        path = '.\\' + path
                    tag_content = info.get('tag', '')
                    desc_content = info.get('desc', '')
                    line = f"{path}{{<>}}{tag_content}{{<>}}{desc_content}>>>>\n"
                    f.write(line)
            messagebox.showinfo("成功", "保存成功")
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("错误", f"保存时出错: {str(e)}")
    
    def on_close(self):
        """关闭窗口"""
        self.root.destroy()
        sys.exit(0)
    
    def focus_next_widget(self, event):
        """Move focus to next widget on Tab key press"""
        event.widget.tk_focusNext().focus()
        return "break"  # Prevent default Tab behavior
    
    def run(self):
        """运行应用程序"""
        self.root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        messagebox.showerror("错误", "请提供文件路径作为参数")
        sys.exit(1)
    
    app = TagSetter(sys.argv[1])
    app.run()
