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
                # 计算相对路径
                try:
                    self.relative_path = os.path.relpath(self.file_path, parent)
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
        # 文件路径
        ttk.Label(self.root, text="文件：").pack(pady=(10, 0), padx=10, anchor='w')
        ttk.Label(self.root, text=self.relative_path).pack(pady=(5, 20), padx=10, anchor='w')
        
        # 标签
        ttk.Label(self.root, text="Tags:").pack(pady=(0, 5), padx=10, anchor='w')
        self.tag_entry = tk.Text(self.root, height=5, width=50)
        self.tag_entry.pack(padx=10, fill='x')
        
        # 描述
        ttk.Label(self.root, text="说明：").pack(pady=(20, 5), padx=10, anchor='w')
        self.desc_entry = tk.Text(self.root, height=15, width=50)
        self.desc_entry.pack(padx=10, fill='both', expand=True)
        
        # 设置现有值
        if self.relative_path in self.all_tags:
            tag_info = self.all_tags[self.relative_path]
            self.tag_entry.insert('1.0', tag_info['tag'])
            self.desc_entry.insert('1.0', tag_info['desc'])
        
        # 保存按钮
        ttk.Button(self.root, text="保存", command=self.save).pack(pady=20)
        
        # tag文件位置
        ttk.Label(self.root, text="tag文件位置：").pack(pady=(0, 5), padx=10, anchor='w')
        ttk.Label(self.root, text=str(self.tag_file)).pack(pady=(0, 20), padx=10, anchor='w')
        
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
        self.all_tags[self.relative_path] = {'tag': tag_escaped, 'desc': desc_escaped}
        
        # 写入文件，与tagfinder.py保持一致
        try:
            # 使用Windows默认编码
            with open(self.tag_file, 'w', encoding='mbcs') as f:
                for path, info in sorted(self.all_tags.items()):
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
    
    def run(self):
        """运行应用程序"""
        self.root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        messagebox.showerror("错误", "请提供文件路径作为参数")
        sys.exit(1)
    
    app = TagSetter(sys.argv[1])
    app.run()
