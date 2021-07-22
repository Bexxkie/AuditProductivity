#SingleInstance force
FormatTime, TimeString, HH:mm, HH:mm
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
	}
;
; INIT
;
F20 & 0::
InputBox, password, Enter Your Opera Password, (Input will be hidden), hide
return
;
; Print Cashier audit
;
F20 & 1::
if WinExist("ahk_class SunAwtFrame")
	{
	WinActivate
	send !m
	sleep, 50
	send r
	sleep, 50
	send cashier audit
	sleep, 50
	send {enter}
	sleep, 50
	send !o
	sleep, 50
	send !P
	sleep, 50
	send !c
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
	send r
	sleep, 50
	send guests in house rate check
	sleep, 50
	send {enter}
	sleep, 50
	send !o
	sleep, 50
	send !p
	sleep, 50
	send !c
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
	send r
	sleep, 50
	send credit limit all payment types
	sleep, 50
	send {enter}
	sleep, 50
	send !o
	sleep, 50
	send !p
	sleep, 50
	send !c
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
	send r
	sleep, 50
	send credit card reconciliation
	sleep, 50
	send {enter}
	sleep, 50
	send !o
	sleep, 50
	send !p
	sleep, 50
	send !c
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
	send r
	sleep, 50
	send downtime reports (4)
	sleep, 50
	send {enter}
	sleep, 50
	send !o
	sleep, 50
	send !p
	sleep, 50
	send !c
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
	send r
	sleep, 50
	send downtime reports (13)
	sleep, 50
	send {enter}
	sleep, 50
	send !o
	sleep, 50
	send !p
	sleep, 50
	send !c
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
	send r
	sleep, 10
	send departures
	sleep, 10
	send {enter}
	sleep, 10
	send !o
	sleep, 10
	today = %a_now%
	If TimeString <24:00 ;is it before 12am?
	{
		If TimeString >03:00
		{
			today += +1,days ; it is, so add one day to the date
		}
	}
	FormatTime, today, %today%, MM/dd/yy
	SendInput %today%
	sleep, 10
	Send {tab}
	sleep, 10
	SendInput %today%
	sleep, 10
	send !p
	
	return
	}
;
; Load batch folios
;
F20 & 8::
if WinExist("ahk_class SunAwtFrame")
	{
	WinActivate
	sleep, 10
	send !c
	sleep, 50
	send f
	sleep, 50
	send o
	sleep, 50
	send %password%
	sleep, 50
	send {enter}
	sleep, 50
	send !x
	sleep, 50
	send !a
	sleep, 50
	send !x
	sleep, 50
	send !x
	sleep, 50
	send !x
	sleep, 50
	send !r
	sleep, 50
	send !z
	sleep, 50
	send !x
	sleep, 50
	send !b
	sleep, 50
	send !x
	return
	}
;
;load IHG reports
;
F20 & 9::
	Run, chrome.exe "https://reporting.ihg.com/index.html?tm=1562841160878"
	WinWait, InterContinental Hotels Group - Google Chrome
	;send %user%
	;send {tab}
	;send %pass%
	;send {enter}
	return
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
	}

;
; Quick checkout
;
F19 & 1::
	if WinExist("ahk_class SunAwtFrame")
	{
	WinActivate
	send !c
	sleep, 10
	send q
	sleep, 10
	send %password%
	sleep, 10
	send {enter}
	return
	}

F19 & 2::
	if WinExist("ahk_class SunAwtFrame")
	{
	WinActivate
	send !m
	sleep, 10
	send r
	sleep, 10
	send guests in-house by room
	sleep, 10
	send {enter}
	sleep, 10
	send !o
	sleep, 10
	send !p
	}
;
; Quit
;
F20 & x::ExitApp