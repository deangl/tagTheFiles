# tagTheFiles
我们总会保存很多文件，但过一段要找的时候可能忘了在哪；又或者反过来，看到一个文件，结果忘了这个文件是干什么的了。
本项目功能实现在Windows 下简单的给文件打标签，写上注释，之后可以按标签查找。
*PS.使用明文分行保存tag，以便通过版本管理软件共享* 

功能上可分两个部分：
1. 打标签部分，在每个文件上右键就可以改标签
2. 查标签部分，用标签查出来对应的文件

## 安装
* 复制tagFinder.exe、tagSetter.exe和regit.bat。
* 在需要查找的根文件夹建立一个文本文件，取名为filetag.tag，并把tagFinder.exe在根文件夹中放一份。
* 在保存tagSetter.exe的文件夹里运行一遍regit.bat，这样右键菜单会多出 *Tag This File*。

## 使用
### 查找
* 运行tagFinder.exe，输入要查找的tag。
* 查找的语法可以是 str1&str2&str3|str4&str5|str6&str1 这样的；含义是先算“且”，再算“或”。
* 将对tag中的文本和文件名查找。
* 单击查找结果可在右侧看到tag和说明。
* 双击结果可以打开文件。
### 设置tag
* 在要打tag的文件上右键，点击菜单中的 *Tag This File*，就可以编辑了。
* 选中tagFinder.exe的查找结果，右侧按 *编辑\取消*，也可以编辑。
