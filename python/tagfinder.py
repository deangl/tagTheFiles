import os
import re
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import json
from pathlib import Path

class TagFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("Tag Finder")
        self.root.geometry("1200x800")
        
        # Variables
        self.r_only = True
        self.rslt_list = []
        self.tags = {}
        self.all_files = []
        self.current_working_dir = os.getcwd()
        
        # Create GUI
        self.create_widgets()
        
        # Load initial data
        self.load_data()
    
    def create_widgets(self):
        # Search frame
        search_frame = ttk.Frame(self.root)
        search_frame.pack(pady=10, padx=10, fill=tk.X)
        
        ttk.Label(search_frame, text="内容:").grid(row=0, column=0, sticky=tk.W)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        self.search_entry.grid(row=0, column=1, padx=5)
        # Bind Enter key to trigger search
        self.search_entry.bind('<Return>', lambda event: self.check_search())
        
        ttk.Button(search_frame, text="查找", command=self.check_search).grid(row=0, column=2, padx=5)
        
        ttk.Label(search_frame, text="查找文件夹:").grid(row=0, column=3, padx=(20, 5))
        self.dir_label = ttk.Label(search_frame, text=self.current_working_dir)
        self.dir_label.grid(row=0, column=4, padx=5)
        
        # Main content frame with list on left and details on right
        main_frame = ttk.Frame(self.root)
        main_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # List view on the left
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        columns = ("shadowID", "路径", "tags")
        self.list_view = ttk.Treeview(list_frame, columns=columns, show="headings", height=20)
        self.list_view.heading("shadowID", text="shadowID")
        self.list_view.heading("路径", text="路径")
        self.list_view.heading("tags", text="tags")
        self.list_view.column("shadowID", width=0, stretch=False)
        self.list_view.column("路径", width=500)
        self.list_view.column("tags", width=200)
        
        # Add scrollbar to list view
        list_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.list_view.yview)
        self.list_view.configure(yscrollcommand=list_scrollbar.set)
        
        self.list_view.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.list_view.bind("<Double-1>", self.on_double_click)
        self.list_view.bind("<Button-3>", self.on_right_click)
        self.list_view.bind("<<TreeviewSelect>>", self.on_select)
        
        # Details frame on the right
        details_frame = ttk.Frame(main_frame)
        details_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        # File info
        file_frame = ttk.Frame(details_frame)
        file_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(file_frame, text="文件:").pack(side=tk.LEFT)
        self.file_var = tk.StringVar()
        self.file_label = ttk.Label(file_frame, textvariable=self.file_var, wraplength=300)
        self.file_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Tags
        tag_frame = ttk.Frame(details_frame)
        tag_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(tag_frame, text="Tags:").pack(side=tk.TOP, anchor=tk.W)
        # Add scrollbar to tag text
        tag_text_frame = ttk.Frame(tag_frame)
        tag_text_frame.pack(fill=tk.BOTH, expand=True)
        self.tag_text = tk.Text(tag_text_frame, height=5, width=30)
        tag_scrollbar = ttk.Scrollbar(tag_text_frame, orient=tk.VERTICAL, command=self.tag_text.yview)
        self.tag_text.configure(yscrollcommand=tag_scrollbar.set)
        self.tag_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tag_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Description
        desc_frame = ttk.Frame(details_frame)
        desc_frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(desc_frame, text="说明:").pack(side=tk.TOP, anchor=tk.W)
        # Add scrollbar to description text
        desc_text_frame = ttk.Frame(desc_frame)
        desc_text_frame.pack(fill=tk.BOTH, expand=True)
        self.desc_text = tk.Text(desc_text_frame, height=10, width=30)
        desc_scrollbar = ttk.Scrollbar(desc_text_frame, orient=tk.VERTICAL, command=self.desc_text.yview)
        self.desc_text.configure(yscrollcommand=desc_scrollbar.set)
        self.desc_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        desc_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons
        button_frame = ttk.Frame(details_frame)
        button_frame.pack(pady=(10, 0))
        ttk.Button(button_frame, text="编辑/取消", command=self.toggle_edit).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="保存", command=self.save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="刷新文件", command=self.refresh).pack(side=tk.LEFT, padx=5)
        
        # Status at the bottom
        status_frame = ttk.Frame(self.root)
        status_frame.pack(pady=5, padx=10, fill=tk.X)
        ttk.Label(status_frame, text="状态:").pack(side=tk.LEFT)
        self.status_var = tk.StringVar(value="就绪")
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var)
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # Set initial read-only state
        self.lock_edit()
    
    def lock_edit(self):
        self.tag_text.config(state=tk.DISABLED, background='#f0f0f0')
        self.desc_text.config(state=tk.DISABLED, background='#f0f0f0')
        self.r_only = True
    
    def unlock_edit(self):
        self.tag_text.config(state=tk.NORMAL, background='white')
        self.desc_text.config(state=tk.NORMAL, background='white')
        self.r_only = False
    
    def toggle_edit(self):
        if self.r_only:
            self.unlock_edit()
        else:
            self.lock_edit()
    
    def load_data(self):
        # Load tags and files in background
        def load_thread():
            self.status_var.set("正在加载数据...")
            self.get_files()
            self.get_tags()
            self.status_var.set("就绪")
        
        threading.Thread(target=load_thread, daemon=True).start()
    
    def get_files(self):
        self.status_var.set("查询文件列表中")
        self.all_files = []
        for root, dirs, files in os.walk(self.current_working_dir):
            if '.git' in root.split(os.sep):
                continue
            for file in files:
                file_path = os.path.join(root, file)
                self.all_files.append(file_path)
        self.status_var.set(f"找到 {len(self.all_files)} 个文件")
    
    def get_tags(self):
        self.status_var.set("查询标签列表中")
        tag_file = os.path.join(self.current_working_dir, "filetag.tag")
        self.tags = self.read_tag_file(tag_file)
        self.status_var.set("标签加载完成")
    
    def read_tag_file(self, filename):
        tags = {}
        if not os.path.exists(filename):
            return tags
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
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
                    tags[file_path] = {'tag': tag, 'desc': desc}
        except Exception as e:
            messagebox.showerror("错误", f"读取标签文件时出错: {str(e)}")
        
        return tags
    
    def check_search(self):
        search_text = self.search_var.get().strip()
        if not search_text:
            return
        
        self.status_var.set("查询结果中")
        self.lock_edit()
        
        # Filter results based on search
        self.rslt_list = []
        file_list = self.make_list()
        
        for file_path, info in file_list.items():
            if isinstance(info, str):
                if self.match_tag(search_text, file_path):
                    self.rslt_list.append([file_path, "", ""])
            else:
                if (self.match_tag(search_text, file_path) or 
                    self.match_tag(search_text, info.get('tag', ''))):
                    self.rslt_list.append([file_path, info.get('tag', ''), info.get('desc', '')])
        
        self.fill_list()
        self.status_var.set("查询完成")
    
    def match_tag(self, search_str, where):
        where_str = str(where)
        or_list = search_str.split('|')
        for or_item in or_list:
            and_list = or_item.split('&')
            match_all = True
            for and_item in and_list:
                if and_item.strip() not in where_str:
                    match_all = False
                    break
            if match_all:
                return True
        return False
    
    def fill_list(self):
        # Clear the list
        for item in self.list_view.get_children():
            self.list_view.delete(item)
        
        # Add results
        for i, item in enumerate(self.rslt_list):
            self.list_view.insert("", "end", values=(i, item[0], item[1]))
    
    def on_select(self, event):
        selection = self.list_view.selection()
        if not selection:
            return
        
        item = self.list_view.item(selection[0])
        values = item['values']
        if len(values) >= 3:
            file_path = values[1]
            self.file_var.set(file_path)  # Path
            
            # Get the actual tag and description from the tags dictionary
            # The file path in the list is relative to the working directory
            tag_info = self.tags.get(file_path, {})
            tag = tag_info.get('tag', '')
            desc = tag_info.get('desc', '')
            
            # Enable text widgets to update content
            self.tag_text.config(state=tk.NORMAL)
            self.desc_text.config(state=tk.NORMAL)
            self.tag_text.delete(1.0, tk.END)
            self.tag_text.insert(1.0, tag)
            self.desc_text.delete(1.0, tk.END)
            self.desc_text.insert(1.0, desc)
            self.lock_edit()
    
    def on_double_click(self, event):
        selection = self.list_view.selection()
        if not selection:
            return
        
        item = self.list_view.item(selection[0])
        values = item['values']
        if len(values) >= 2:
            file_path = values[1]
            try:
                os.startfile(file_path)
            except:
                messagebox.showerror("错误", f"无法打开文件: {file_path}")
    
    def on_right_click(self, event):
        item = self.list_view.identify_row(event.y)
        if not item:
            return
        
        self.list_view.selection_set(item)
        item_data = self.list_view.item(item)
        values = item_data['values']
        if len(values) >= 2:
            file_path = values[1]
            folder_path = os.path.dirname(file_path)
            try:
                os.startfile(folder_path)
            except:
                messagebox.showerror("错误", f"无法打开文件夹: {folder_path}")
    
    def save(self):
        self.lock_edit()
        file_path = self.file_var.get()
        tag = self.tag_text.get(1.0, tk.END).strip()
        desc = self.desc_text.get(1.0, tk.END).strip()
        
        if file_path:
            self.tags[file_path] = {'tag': tag, 'desc': desc}
            self.save_tags()
            self.check_search()
    
    def save_tags(self):
        self.status_var.set("保存中")
        tag_file = os.path.join(self.current_working_dir, "filetag.tag")
        
        try:
            with open(tag_file, 'w', encoding='utf-8') as f:
                for file_path, info in sorted(self.tags.items()):
                    tag = info.get('tag', '').replace('\n', '@n@')
                    desc = info.get('desc', '').replace('\n', '@n@')
                    line = f"{file_path}{{<>}}{tag}{{<>}}{desc}>>>>\n"
                    f.write(line)
            self.status_var.set("保存完成")
        except Exception as e:
            messagebox.showerror("错误", f"保存标签时出错: {str(e)}")
            self.status_var.set("保存失败")
    
    def refresh(self):
        def refresh_thread():
            self.get_files()
            self.check_search()
        
        threading.Thread(target=refresh_thread, daemon=True).start()
    
    def make_list(self):
        self.status_var.set("合并数据中")
        result = {}
        
        for file_path in self.all_files:
            # Make path relative to current working directory
            try:
                rel_path = os.path.relpath(file_path, self.current_working_dir)
            except:
                rel_path = file_path
            result[rel_path] = self.tags.get(rel_path, "")
        
        self.status_var.set("合并数据完成")
        return result

if __name__ == "__main__":
    root = tk.Tk()
    app = TagFinder(root)
    root.mainloop()
