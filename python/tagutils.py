import os
from pathlib import Path
from tkinter import messagebox

def find_tag_file(file_path):
    """查找tag文件"""
    current_path = Path(file_path)
    # 从文件所在目录开始向上查找
    for parent in [current_path.parent] + list(current_path.parents):
        tag_file_path = parent / "filetag.tag"
        if tag_file_path.exists():
            return tag_file_path
    return None

def get_relative_path(file_path, base_dir):
    """获取相对于base_dir的路径，确保以.\开头"""
    try:
        rel_path = os.path.relpath(file_path, base_dir)
        # 确保路径以.\开头
        if not rel_path.startswith('.\\'):
            rel_path = '.\\' + rel_path
        return rel_path
    except ValueError:
        # 如果在不同驱动器上，使用绝对路径
        return file_path

def read_tag_file(filename):
    """读取标签文件"""
    tags = {}
    if not os.path.exists(filename):
        return tags
    
    try:
        # Use Windows default encoding
        with open(filename, 'r', encoding='mbcs') as f:
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
                # Ensure path starts with .\
                if not file_path.startswith('.\\'):
                    file_path = '.\\' + file_path
                tag = parts[1]
                desc = parts[2]
                # Restore newlines
                tag = tag.replace('@n@', '\n')
                desc = desc.replace('@n@', '\n')
                tags[file_path] = {'tag': tag, 'desc': desc}
    except Exception as e:
        messagebox.showerror("错误", f"读取标签文件时出错: {str(e)}")
    return tags

def write_tag_file(filename, tags):
    """写入标签文件"""
    try:
        # Use Windows default encoding
        with open(filename, 'w', encoding='mbcs') as f:
            for file_path, info in sorted(tags.items()):
                # Ensure path starts with .\
                if not file_path.startswith('.\\'):
                    file_path = '.\\' + file_path
                tag = info.get('tag', '').replace('\n', '@n@')
                desc = info.get('desc', '').replace('\n', '@n@')
                line = f"{file_path}{{<>}}{tag}{{<>}}{desc}>>>>\n"
                f.write(line)
        return True
    except Exception as e:
        messagebox.showerror("错误", f"保存标签时出错: {str(e)}")
        return False
