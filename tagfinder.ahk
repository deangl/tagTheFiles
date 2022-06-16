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
Gui, Add, Text, y10 x+5 vTF , �����ļ���:
Gui, Add, Text, y10 x+20 vTagFileName, %A_WorkingDir%
Gui, Add, ListView,x3 W720 r30 +AltSubmit gResultList, shadowID|·��|tags

LV_ModifyCol(1,0)
LV_ModifyCol(2,500)
LV_ModifyCol(3,200)


Gui, Add, Text, y+5, ״̬:
Gui, Add, Text, x+5 vStats w700
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
	guicontrol, , Stats, ��ѯ�����
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
	guicontrol, , Stats, ��ѯ���
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
	RunWait %ComSpec% /c dir /a-D /S /B %folder% | findstr /v /i "\.git\\" > tmptmp, ,hide
	FileRead, raw, tmptmp
	FileDelete, tmptmp
	allFile := strsplit(raw, "`n")
	return allFile
}


getTags(){
	; tags := json2("filetag.json")
	guicontrol, , Stats, ��ѯ��ǩ�б���
	global tags
	tags := readTagFile("filetag.tag")
	; for k,v in tags{
	; 	; t:=v["tag"]
	; 	; msgbox % k . ":" . t
	; }
	guicontrol, , Stats, ��ѯ��ǩ�б����
	return tags
}
saveTags(){
	guicontrol, , Stats, ������
	global tags
	writeTagFile("filetag.tag", tags)
	guicontrol, , Stats, �������
	return
}

makeList(){
	guicontrol, , Stats, �ϲ�������
	guicontrol, , Stats, ��ѯ�ļ��б���
	f := getFiles(A_WorkingDir)
	guicontrol, , Stats, ��ѯ�ļ��б����
	t := getTags()
	for k,v in t{
		j:=v["tag"]
		msgbox % k . ":" . j
	}
	rslt := {}
	for k,v in f
	{
		v := pathrelativepathto( A_WorkingDir . "\",v)
		; msgbox % v
		; r := t[v]["tag"]
		; msgbox % r
		rslt[v] := t[v]
	}
	guicontrol, , Stats, �ϲ��������
	return rslt
}