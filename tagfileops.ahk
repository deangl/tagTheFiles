
; v1 :={	c:{tag:"3",desc:"d3"},	a:{tag:"1",desc:"d1"}}
; a := writeTagFile("tagfile.tag", v1)
; msgbox wrote
; v2 := readTagFile("tagfile.tag")

; for k,v in v2
; {
; 	s := k . ":" . v.tag . ";" v.desc
; 	msgbox %s%
; }

; v2.b := {tag:"2", desc:"d2"}

; a := writeTagFile("tagfile.tag", v2)

readTagFile(fileName){
	rslt := {}
	Loop{
		fileReadLine, v,  %fileName%, %A_Index%
		if ErrorLevel
			break

		v := StrReplace(v, ">>>>", "")
		v := StrReplace(v, "@n@", "`n")

		if(strlen(v) > 1){
			d :=StrSplit(v, "{<>}")
			fileName:=d[1]
			tag:=d[2]
			desc := d[3]

			rslt[fileName] := {tag:tag, desc:desc}
		}
	}
	return rslt
}

writeTagFile(fileName, data){
	keyList := []
	for k,v in data{
		keyList.push(k)
	}
	Sort,keyList
	raw := ""
	for i,k in keyList{
		; msgbox % k
		raw := raw . k . "{<>}" . strreplace(data[k]["tag"], "`n", "@n@") . "{<>}" . strreplace(data[k]["desc"], "`n", "@n@") . ">>>>`n"
 		; msgbox % raw
	}
	msgbox 更新完成
	filedelete, %fileName%
	fileappend, %raw%, %fileName% 

	return
}



