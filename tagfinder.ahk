#singleinstance
#Include .\toolFunc.ahk
; #Include .\json2.ahk
#Include .\tagfileops.ahk

global rOnly := 1
global rsltList := []
global tags := {}
; tags := json2("filetag.json")

Gui, New
Gui, Add, Text, y10 r1 x3 vTag , ����:
Gui, Add, Edit, y10 r1 x+10 w200 vToSearch ys 
Gui, Add, Button, y10 gCheckS +default ys, ����

Gui, Add, ListView,x3 W720 r30 +AltSubmit gResultList, shadowID|·��|tags

LV_ModifyCol(1,0)
LV_ModifyCol(2,500)
LV_ModifyCol(3,200)


Gui, Add, Text, x3 r1 vTF , �����ļ���:
Gui, Add, Text, x+20 vTagFileName, %A_WorkingDir%
Gui, Add, Text, y10 x750 r1, �ļ���
Gui, Add, Text, y10 x+20 r1 w200 vShowFileName, 
Gui, Add, Text, y+10 x750 r1, Tags:
Gui, Add, Edit, y+5 x750 r5 w300 readOnly vChosenTag, 
Gui, Add, Text, y+20 x750 r1, ˵����
Gui, Add, Edit, y+5 x750 r25 w300 readOnly vChosenDesc, 

Gui, Add, Button, y+5 gToggleEdit, �༭\ȡ��
Gui, Add, Button, x+100 gSave,����

Gui, Show
return

lockEdit(){
	global rOnly
	guicontrol, +readOnly,ChosenTag
	guicontrol, +readOnly,ChosenDesc
	rOnly := 1
	return
}


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
			if (InStr(k, searchTag) or InStr(v["tag"], searchTag))
			{
				rsltList.push([k, v["tag"], v["desc"]])
			}
		}
	}
	gosub FillList
	return

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
				LV_GetText(tag, rowN, 3)
				LV_GetText(desc, rowN, 1)
				LV_GetText(thepath, rowN, 2)

				guicontrol, , showFileName, %thepath%
				guicontrol, , chosenTag, %tag%
				guicontrol, , chosenDesc, %desc%
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
	; msgbox bye
	ExitApp
	return

GuiEscape:
	ExitApp
	return

getFiles(folder){
	allFile := []
	loop,Files ,%folder%\*.*, D
	{
		if (substr(A_LoopFileName,1,1) != "."){
			r := getFiles(A_LoopFileFullPath)
			for k,v in r
			{
				allFile.push(v)
			}
		}
	}
	loop,Files ,%folder%\*.*, F
	{
		r = %folder%\%A_LoopFileName%
		allFile.push(r)
	}
	return allFile
}

getTags(){
	; tags := json2("filetag.json")
	global tags
	tags := readTagFile("filetag.tag")
	return tags
}
saveTags(){
	global tags
	writeTagFile("filetag.tag", tags)
	return
}

makeList(){
	f := getFiles(A_WorkingDir)
	t := getTags()
	rslt := {}
	for k,v in f
	{
		v := pathrelativepathto( A_WorkingDir,v)
		rslt[v] := t[v]
	}
	return rslt
}