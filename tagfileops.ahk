readTagFile(fileName){
	rslt := {}
	fileRead, f, %fileName%
	raw := strSplit(f, "`n")
	for i,v in raw {
		v := substr(v, 1, strlen(v)-1) ;ȥ����ĩ��^M
		v := StrReplace(v, ">>>>", "")
		v := StrReplace(v, "@n@", "`n")

		d :=StrSplit(v, "{<>}")
		fileName:=d[1]
		tag:=d[2]
		desc := d[3]
		if tag{
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
		if strlen(k) > 1{
			raw := raw . k . "{<>}" . strreplace(data[k]["tag"], "`n", "@n@") . "{<>}"
			if data[k]["desc"]{
				t := data[k]["desc"]
				d := strreplace(data[k]["desc"], "`n", "@n@")
				raw := raw . d
			}
			raw := raw . ">>>>`n"
		}
	}
	msgbox �������
	filedelete, %fileName%
	fileappend, %raw%, %fileName% 

	return
}



