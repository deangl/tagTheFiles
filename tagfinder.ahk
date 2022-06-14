#singleinstance
#Include .\toolFunc.ahk
#Include .\json2.ahk

; tags := json2("filetag.json")

Gui, New


Gui, Add, Text, r1 x3 vTag , 内容:
Gui, Add, Edit, r1 x+10 w200 ys 
Gui, Add, Button, gCheckS ys, 查找

Gui, Add, ListView,x3 W720 r30 gResultList, shadowID|路径|tags

LV_ModifyCol(1,0)
LV_ModifyCol(2,500)
LV_ModifyCol(3,200)


Gui, Add, Text, x3 r1 vTF , tagfile:
Gui, Add, Text, x+20 vTagFileName, filename
Gui, Add, Text, y10 x750 r1, Tags:
Gui, Add, Edit, y+5 x750 r5 w300, 1111
Gui, Add, Text, y+20 x750 r1, 说明：
Gui, Add, Edit, y+5 x750 r30 w300, 瞒瞒上

Gui, Show

CheckS:
	return

ResultList:
	return

GuiClose:
	; msgbox bye
	ExitApp
	return