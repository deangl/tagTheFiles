#singleinstance
#Include .\toolFunc.ahk
#Include .\tagfileops.ahk

global rOnly := 1
global rsltList := []
global tags := {}
global allFiles := []



Gui, New
Gui, Add, Text, y10 r1 x3 vTag , 内容:
Gui, Add, Edit, y10 r1 x+10 w200 vToSearch ys 
Gui, Add, Button, y10 gCheckS +default ys, 查找
Gui, Add, Text, y10 x+5 vTF , 查找文件夹:
Gui, Add, Text, y10 x+20 vTagFileName, %A_WorkingDir%
Gui, Add, ListView,x3 W720 r30 +AltSubmit gResultList, shadowID|路径|tags

LV_ModifyCol(1,0)
LV_ModifyCol(2,500)
LV_ModifyCol(3,200)


Gui, Add, Text, y+5, 状态:
Gui, Add, Text, x+5 vStats w700
Gui, Add, Text, y10 x750 r1, 文件：
Gui, Add, Text, y10 x+20 r1 w200 vShowFileName, 
Gui, Add, Text, y+10 x750 r1, Tags:
Gui, Add, Edit, y+5 x750 r5 w300 readOnly vChosenTag, 
Gui, Add, Text, y+20 x750 r1, 说明：
Gui, Add, Edit, y+5 x750 r25 w300 readOnly vChosenDesc, 


Gui, Add, Button, y+5 gToggleEdit, 编辑\取消
Gui, Add, Button, x+100 gSave,保存
Gui, Add, Button, x+50 gRefresh,刷新文件

Gui, Show
return

lockEdit(){
	global rOnly
	guicontrol, +readOnly,ChosenTag
	guicontrol, +readOnly,ChosenDesc
	rOnly := 1
	return
}



Refresh:
	global Allfiles
	_ :=  getFiles(A_WorkingDir)
	return
Save:
	lockEdit()
	guicontrolget,thepath,,showFileName
	guicontrolget,tag,,chosenTag
	guicontrolget,desc,,chosenDesc
	global tags
	tags[thepath] := {tag:tag, desc:desc}
	_:=saveTags()
	gosub CheckS
	return

CheckS:
	guicontrol, , Stats, 查询结果中
	lockEdit()
	global rsltList

	rOnly := 1
	l:=makeList()
	guicontrolget,searchTag,,ToSearch
	rsltList := []
	if (strlen(searchTag)>0)
	{
		for k,v in l
		{
			if(matchTag(searchTag, k) or matchTag(searchTag, v["tag"]))
			{
				rsltList.push([k, v["tag"], v["desc"]])
			}
		}
	}
	gosub FillList
	guicontrol, , Stats, 查询完成
	return

matchTag(searchStr, Where){
	; searchStr的语法是 str1&str2&str3|str4&str5|str6&str1 这样的；含义是先算“且”，再算“或”
	orList := strsplit(searchStr, "|")
	for iOr, orStr in orList{
		andList := strsplit(orStr, "&")
		o := True
		for iAnd, andStr in andList{
			if ( not(InStr(Where, andStr))){
				o:=False
				break
			}
		}
		if o{
			return True
		}
	}
	return False
}


FillList:
	global rsltList
	Gui, ListView, ResultList
	LV_Delete()
	for i,v in rsltList
	{
		LV_Add("",v[3], v[1],v[2])
	}

	return


ResultList:
	{
		If NOT ErrorLevel
		{
			if (A_GuiEvent == "Normal" or A_GuiEvent == "K")
			{
				rowN := LV_GetNext()
				if (rowN != 0){
					LV_GetText(tag, rowN, 3)
					LV_GetText(desc, rowN, 1)
					LV_GetText(thepath, rowN, 2)

					guicontrol, , showFileName, %thepath%
					guicontrol, , chosenTag, %tag%
					guicontrol, , chosenDesc, %desc%
				}
			}
			if (A_GuiEvent == "DoubleClick")
			{
				LV_GetText(thepath, A_EventInfo, 2)
				run, %thepath%
			}
		}

	}
	return



ToggleEdit:
	global rOnly
	if rOnly
	{
		guicontrol, -readOnly,ChosenTag
		guicontrol, -readOnly,ChosenDesc
		rOnly := 0
	}else
	{
		guicontrol, +readOnly,ChosenTag
		guicontrol, +readOnly,ChosenDesc
		rOnly := 1
	}
	return


GuiClose:
	ExitApp
	return

GuiEscape:
	ExitApp
	return

getFiles(folder){
	guicontrol, , Stats, 查询文件列表中
	global allFiles
	allFiles := []
	RunWait %ComSpec% /c dir /a-D /S /B %folder% | findstr /v /i "\.git\\" > tmptmp, ,hide
	Loop{
		fileReadLine, v,  tmptmp, %A_Index%
		if ErrorLevel
			break
		allFiles.push(v)
	}
	FileDelete, tmptmp
	guicontrol, , Stats, 查询文件列表完成
	return allFiles
}


getTags(){
	guicontrol, , Stats, 查询标签列表中
	global tags

	tags := readTagFile("filetag.tag")

	guicontrol, , Stats, 查询标签列表完成
	return tags
}

saveTags(){
	guicontrol, , Stats, 保存中
	global tags

	writeTagFile("filetag.tag", tags)

	guicontrol, , Stats, 保存完成
	return
}

makeList(){
	guicontrol, , Stats, 合并数据中
	f := allFiles		;如果allFiles有数，就不要重新查了
	if f.length() == 0
		f:= getFiles(A_WorkingDir)


	t := getTags()
	rslt := {}
	for k,v in f
	{
		v := pathrelativepathto( A_WorkingDir . "\_",v)
		rslt[v] := t[v]
	}
	guicontrol, , Stats, 合并数据完成
	return rslt
}