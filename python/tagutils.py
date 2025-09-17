import os
from pathlib import Path
from tkinter import messagebox

def find_tag_file(file_path):
    """查找tag文件"""
    # Convert to absolute path first
    if not os.path.isabs(file_path):
        # If it's a relative path, make it absolute
        abs_file_path = os.path.abspath(file_path)
    else:
        abs_file_path = file_path
    
    current_path = Path(abs_file_path)
    
    # Check if the path exists
    if not current_path.exists():
        return None
    
    # If it's a file, start from its parent directory
    # If it's a directory, start from the directory itself
    if current_path.is_file():
        start_path = current_path.parent
    else:
        start_path = current_path
    
    # 从文件所在目录开始向上查找
    for parent in [start_path] + list(start_path.parents):
        tag_file_path = parent / "filetag.tag"
        if tag_file_path.exists():
            return str(tag_file_path)
    return None

def get_relative_path(file_path, base_dir):
    """获取相对于base_dir的路径，确保以.\开头"""
    try:
        # Make sure both paths are absolute
        if not os.path.isabs(file_path):
            abs_file_path = os.path.abspath(file_path)
        else:
            abs_file_path = file_path
        
        if not os.path.isabs(base_dir):
            abs_base_dir = os.path.abspath(base_dir)
        else:
            abs_base_dir = base_dir
        
        rel_path = os.path.relpath(abs_file_path, abs_base_dir)
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
        with open(filename, 'r', encoding='gbk') as f:
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
        with open(filename, 'w', encoding='gbk') as f:
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
