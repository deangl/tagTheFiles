; tests

; msgbox % PathRelativePathTo( "C:\1\2\3\41", "C:\1\2\3\4\5\6" )
; msgbox % PathRelativePathTo( "C:\1\2\3\4\", "C:\1\2\3\4\5\6" )
; msgbox % PathRelativePathTo( "C:\1\2\3\4", "C:\1\2\3\5" )


PathRelativePathTo(from,to){
	; from 和 to 都只能是文件, 虽然文件夹也能用，但可能会理解有误
	f_list := strSplit(from, "\")
	t_list := strSplit(to, "\")

	f_n := f_list.length()-1

	same_l := f_n

	loop %f_n%
	{
		if (f_list[A_Index] != t_list[A_Index]){
			same_l := A_Index -1
			break
		}
	}

	up_n := f_n - same_l
	rslt := ""

	if up_n{
		loop %up_n%{
			rslt := rslt . "..\"
		}
	}else{
		rslt := ".\"
	}
	rslt := SubStr(rslt, 1, strlen(rslt)-1)

	follow_n := t_list.length()-same_l
	loop %follow_n%{
		rslt := rslt . "\" . t_list[A_Index+same_l]
	}
	return rslt

}