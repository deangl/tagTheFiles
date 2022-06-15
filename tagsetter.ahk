#Include .\toolFunc.ahk
#Include .\tagfileops.ahk

global filePath
global allTags


filePath = %1%
tagFile := findTagFile(filePath)
SplitPath, tagFile, OutFileName, tagFileFolder, 


if tagFile {
	global allTags
	allTags := readTagFile(tagFile)
	filePath := pathrelativepathto(tagFileFolder,filePath)
	tag := allTags[filePath]["tag"]
	desc := allTags[filePath]["desc"]

	Gui, New
	Gui, Add, Text, y10 x10 r1, 文件：
	Gui, Add, Text, y10 x+20 r1 w200 vShowFileName, %filePath%
	Gui, Add, Text, y+10 x10 r1, Tags:
	Gui, Add, Edit, y+5 x10 r5 w300  vChosenTag, %tag%
	Gui, Add, Text, y+20 x10 r1, 说明：
	Gui, Add, Edit, y+5 x10 r25 w300 vChosenDesc, %desc%
	Gui, Add, Button, y+5 gSave +default,保存
	gui,add,Text, y+5 x10, tag文件位置：
	gui,add,text,x+10,%tagFile%
	Gui, Show
	return
}else{
	msgbox 找不到 filetag.tag
	return
}


GuiClose:
	; msgbox bye
	ExitApp
	return

GuiEscape:
	ExitApp
	return


Save:
	global allTags
	guicontrolget,thepath,,showFileName
	guicontrolget,tag,,chosenTag
	guicontrolget,desc,,chosenDesc
	allTags[thepath] := {tag:tag, desc:desc}
	writeTagFile(tagFile, allTags)
	ExitApp
	return

findTagFile(filePath){
	pathArr := strsplit(filePath, "\")

	N := pathArr.length()

	loop, %N%
	{
		w := joinPath(pathArr, N-A_index) . "filetag.tag"
		if fileexist(w){
			return w
		}
	}
	return 0
}

joinPath(pathArr, N){
	r := ""
	loop, %N%
	{
		r := r . pathArr[A_index] . "\"
	}
	return r
}

