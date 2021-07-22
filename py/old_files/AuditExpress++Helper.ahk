#SingleInstance force
;IniRead, ps, CONFIG, AHK, pss
;ps := %A_Index%
;Global pwd := %ps%
FormatTime, TimeString, HH:mm, HH:mm
SetTimer, exitScript, 1000
exitScript:
	IfWinNotExist, AuditExpress
		ExitApp
	return
;
; RESET
;
F19 & 0:: 
if WinExist("ahk_class SunAwtFrame")
	{
	WinActivate
	send !c
	send !x
	sleep, 5
	send !c
	send !x
	sleep, 5
	send !c
	sleep, 5
	send !c
	sleep, 5
	send !c
	return
	}else{
	MsgBox, Opera must be open!
	return
	}
;
; INIT
;
F20 & 0::
if WinExist("ahk_class SunAwtFrame")
	{
	InputBox, password, Enter Your Opera Password, (Input will be hidden), hide
	return
	}else{
	MsgBox, Opera must be open!
	return
	}
;
; Print Cashier audit
;
F20 & 1::
if WinExist("ahk_class SunAwtFrame")
	{
	WinActivate
	send !m
	sleep, 50
	WinActivate
	send r
	sleep, 501
	WinActivate
	send cashier audit
	sleep, 50
	WinActivate
	send {enter}
	sleep, 50
	WinActivate
	send !o
	sleep, 50
	WinActivate
	send !P
	sleep, 50
	WinActivate
	send !c
	return
	}else{
	MsgBox, Opera must be open!
	return
	}
;
; Print Guests in house rate check
;
F20 & 2::
if WinExist("ahk_class SunAwtFrame")
	{
	WinActivate
	send !m
	sleep, 50
	WinActivate
	send r
	sleep, 50
	WinActivate
	send guests in house rate check
	sleep, 50
	WinActivate
	send {enter}
	sleep, 50
	WinActivate
	send !o
	sleep, 50
	WinActivate
	send !p
	sleep, 50
	WinActivate
	send !c
	return
	}else{
	MsgBox, Opera must be open!
	return
	}
;
; Print credit limit all payment types
;
F20 & 3::
if WinExist("ahk_class SunAwtFrame")
	{
	WinActivate
	send !m
	sleep, 50
	WinActivate
	send r
	sleep, 50
	WinActivate
	send credit limit all payment types
	sleep, 50
	WinActivate
	send {enter}
	sleep, 50
	WinActivate
	send !o
	sleep, 50
	WinActivate
	send !p
	sleep, 50
	WinActivate
	send !c
	return
	}else{
	MsgBox, Opera must be open!
	return
	}
;
;Print credit card reconciliation
;
F20 & 4::
if WinExist("ahk_class SunAwtFrame")
	{
	WinActivate
	send !m
	sleep, 50
	WinActivate
	send r
	sleep, 50
	WinActivate
	send credit card reconciliation
	sleep, 50
	WinActivate
	send {enter}
	sleep, 50
	WinActivate
	send !o
	sleep, 50
	WinActivate
	send !p
	sleep, 50
	WinActivate
	send !c
	return
	}else{
	MsgBox, Opera must be open!
	return
	}
;
;Print downtime reports (4)
;
F20 & 5::
if WinExist("ahk_class SunAwtFrame")
	{
	WinActivate
	send !m
	sleep, 50
	WinActivate
	send r
	sleep, 50
	WinActivate
	send downtime reports (4)
	sleep, 50
	WinActivate
	send {enter}
	sleep, 50
	WinActivate
	send !o
	sleep, 50
	WinActivate
	send !p
	sleep, 50
	WinActivate
	send !c
	return
	}else{
	MsgBox, Opera must be open!
	return
	}
;
;Print downtime reports (13)
;
F20 & 6::
if WinExist("ahk_class SunAwtFrame")
	{
	WinActivate
	send !m
	sleep, 50
	WinActivate
	send r
	sleep, 50
	WinActivate
	send downtime reports (13)
	sleep, 50
	WinActivate
	send {enter}
	sleep, 50
	WinActivate
	send !o
	sleep, 50
	WinActivate
	send !p
	sleep, 50
	WinActivate
	send !c
	return
	}else{
	MsgBox, Opera must be open!
	return
	}
;
;load Departures list
;
F20 & 7::
if WinExist("ahk_class SunAwtFrame")
	{
	WinActivate
	send !m
	sleep, 10
	WinActivate
	send r
	sleep, 10
	WinActivate
	send departures
	sleep, 10
	WinActivate
	send {enter}
	sleep, 10
	WinActivate
	send !o
	sleep, 10
	WinActivate
	today = %a_now%
	If TimeString <24:00 ;is it before 12am?
		{
		If TimeString >03:00
			{
			today += +1,days ; it is, so add one day to the date
			}
		}
	FormatTime, today, %today%, MM/dd/yy
	WinActivate
	SendInput %today%
	sleep, 10
	WinActivate
	Send {tab}
	sleep, 10
	WinActivate
	SendInput %today%
	sleep, 10
	WinActivate
	send !p
	
	return
	}else{
	MsgBox, Opera must be open!
	return
	}
;
; Load batch folios
;
F20 & 8::
if WinExist("ahk_class SunAwtFrame")
	{
	;password = %pwd%
	WinActivate
	sleep, 10
	WinActivate
	send !c
	sleep, 50
	WinActivate
	send f
	sleep, 50
	WinActivate
	send o
	sleep, 50
	WinActivate
	send %password%
	sleep, 50
	WinActivate
	send {enter}
	sleep, 50
	WinActivate
	send !x
	sleep, 50
	WinActivate
	send !a
	sleep, 50
	WinActivate
	send !x
	sleep, 50
	WinActivate
	send !x
	sleep, 50
	WinActivate
	send !x
	sleep, 50
	WinActivate
	send !r
	sleep, 50
	WinActivate
	send !z
	sleep, 50
	WinActivate
	send !x
	sleep, 50
	WinActivate
	send !b
	sleep, 50
	WinActivate
	send !x
	return
	}else{
	MsgBox, Opera must be open!
	return
	}
;
;print occupancy graph
;
F20 & F19::
if WinExist("ahk_class SunAwtFrame")
	{
	WinActivate
	send !o
	send g
	Sleep, 10
	send !p
	Sleep, 1000
	send !s
	Sleep, 10
	send !l
	Sleep, 10
	send {enter}
	sleep, 10
	send !c
	return
	}else{
	MsgBox, Opera must be open!
	return
	}

;
; Quick checkout
;
F19 & 1::
	if WinExist("ahk_class SunAwtFrame")
	{
	;password = %pwd%
	WinActivate
	send !c
	sleep, 10
	WinActivate
	send q
	sleep, 10
	WinActivate
	send %password%
	sleep, 10
	WinActivate
	send {enter}
	return
	}else{
	MsgBox, Opera must be open!
	return
	}
;
; guest in house by room
;
F19 & 2::
	if WinExist("ahk_class SunAwtFrame")
	{
	WinActivate
	send !m
	sleep, 10
	WinActivate
	send r
	sleep, 10
	WinActivate
	send guests in-house by room
	sleep, 10
	WinActivate
	send {enter}
	sleep, 10
	WinActivate
	send !o
	sleep, 10
	WinActivate
	send !p
	return
	}else{
	MsgBox, Opera must be open!
	return
	}
;
; print reg cards
;
F19 & 3::
	if WinExist("ahk_class SunAwtFrame")
	{
	WinActivate
	send !r
	sleep, 10
	send g
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	today = %a_now%	
	FormatTime, today, %today%, MM/dd/yy
	SendInput %today%
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {space}
	sleep, 10
	send {tab}
	sleep, 10
	send {space}
	sleep, 10
	send !p
	return
	}else{
	MsgBox, Opera must be open!
	return
	}
;
; print morning reports
;
F19 & 4::
	if WinExist("ahk_class SunAwtFrame")
	{
	WinActivate
	send !m
	sleep, 10
	send r
	sleep, 10
	send manager
	sleep, 10
	send {enter}
	sleep, 10
	send !o
	sleep, 10
	send !p
	sleep, 20
	WinActivate
	send !c
	sleep, 10
	send !c	
	sleep,10
	send !m
	sleep, 10
	send r
	sleep, 10
	send financ
	sleep, 10
	send {enter}
	sleep, 10
	send !o
	sleep, 10
	send !p
	return
	}else{
	MsgBox, Opera must be open!
	return
	}
F19 & 5::
	if WinExist("ahk_class SunAwtFrame")
	{
	WinActivate
	send !m
	sleep, 10
	send r
	sleep, 10
	send financ
	sleep, 10
	send {enter}
	sleep, 10
	send !o
	sleep, 10
	send !p
	return
	}else{
	MsgBox, Opera must be open!
	return
	}
	
;
; begin RTC CHECK
;

F18 & 1::
	if WinExist("ahk_class SunAwtFrame")
	{
	WinActivate
	send !r
	sleep, 10
	send u
	sleep, 10
	send !a
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send IDAWV
	sleep,10
	send !h
	return
	}else{
	MsgBox, Opera must be open!
	return
	}
	
F18 & 2::
	if WinExist("ahk_class SunAwtFrame")
	{
	WinActivate
	send !r
	sleep, 10
	send u
	sleep, 10
	send !a
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send IDUWV
	sleep,10
	send !h
	return
	}else{
	MsgBox, Opera must be open!
	return
	}
	
F18 & 3::
	if WinExist("ahk_class SunAwtFrame")
	{
	WinActivate
	send !r
	sleep, 10
	send u
	sleep, 10
	send !a
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send IDHWV
	sleep,10
	send !h
	return
	}else{
	MsgBox, Opera must be open!
	return
	}
	
F18 & 4::
	if WinExist("ahk_class SunAwtFrame")
	{
	WinActivate
	send !r
	sleep, 10
	send u
	sleep, 10
	send !a
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send IDHNP
	sleep,10
	send !h
	return
	}else{
	MsgBox, Opera must be open!
	return
	}
	
F18 & 5::
	if WinExist("ahk_class SunAwtFrame")
	{
	WinActivate
	send !r
	sleep, 10
	send u
	sleep, 10
	send !a
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send IDHVC	
	sleep,10
	send !h
	return
	}else{
	MsgBox, Opera must be open!
	return
	}
	
F18 & 6::
	if WinExist("ahk_class SunAwtFrame")
	{
	WinActivate
	send !r
	sleep, 10
	send u
	sleep, 10
	send !a
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send IDH25
	sleep,10
	send !h
	return
	}else{
	MsgBox, Opera must be open!
	return
	}
	
F18 & 7::
	if WinExist("ahk_class SunAwtFrame")
	{
	WinActivate
	send !r
	sleep, 10
	send u
	sleep, 10
	send !a
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send IDIN2
	sleep,10
	send !h
	return
	}else{
	MsgBox, Opera must be open!
	return
	}
	
F18 & 8::
	if WinExist("ahk_class SunAwtFrame")
	{
	WinActivate
	send !r
	sleep, 10
	send u
	sleep, 10
	send !a
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send IDU00
	sleep,10
	send !h
	return
	}else{
	MsgBox, Opera must be open!
	return
	}
	
F18 & 9::
	if WinExist("ahk_class SunAwtFrame")
	{
	WinActivate
	send !r
	sleep, 10
	send u
	sleep, 10
	send !a
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send IDUVC
	sleep,10
	send !h
	return
	}else{
	MsgBox, Opera must be open!
	return
	}
	
F17 & 1::
	if WinExist("ahk_class SunAwtFrame")
	{
	WinActivate
	send !r
	sleep, 10
	send u
	sleep, 10
	send !a
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send IWU25
	sleep,10
	send !h
	return
	}else{
	MsgBox, Opera must be open!
	return
	}
	
F17 & 2::
	if WinExist("ahk_class SunAwtFrame")
	{
	WinActivate
	send !r
	sleep, 10
	send u
	sleep, 10
	send !a
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send IWH25
	sleep,10
	send !h
	return
	}else{
	MsgBox, Opera must be open!
	return
	}
	
F17 & 3::
	if WinExist("ahk_class SunAwtFrame")
	{
	WinActivate
	send !r
	sleep, 10
	send u
	sleep, 10
	send !a
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send IDU25
	sleep,10
	send !h
	return
	}else{
	MsgBox, Opera must be open!
	return
	}
	
F17 & 4::
	if WinExist("ahk_class SunAwtFrame")
	{
	WinActivate
	send !r
	sleep, 10
	send u
	sleep, 10
	send !a
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send IDU14
	sleep,10
	send !h
	return
	}else{
	MsgBox, Opera must be open!
	return
	}
	
F17 & 5::
	if WinExist("ahk_class SunAwtFrame")
	{
	WinActivate
	send !r
	sleep, 10
	send u
	sleep, 10
	send !a
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send {tab}
	sleep, 10
	send IDAX4
	sleep,10
	send !h
	return
	}else{
	MsgBox, Opera must be open!
	return
	}


!1::send %password%
!2::send PREPAID


;
; Quit
;
F20 & x::ExitApp
