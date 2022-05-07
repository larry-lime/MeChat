#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
; Execute a script if ^\ is pressed and windows terminal is active

^F10::
;#IfWinExist ahk_exe "c:\Users\larry\AppData\Local\Microsoft\WindowsApps\wt.exe"
send, {u Down}
send, {u Up}
send, {p Down}
send, {p Up}
send, {c Down}
send, {c Up}
send, {Enter Down}
send, {Enter Up}
sleep, 300
send, {d Down}
send, {d Up}
send, {d Down}
send, {d Up}
send, {Enter Down}
send, {Enter Up}
return

^F9::
;#IfWinExist ahk_exe "c:\Users\larry\AppData\Local\Microsoft\WindowsApps\wt.exe"
send, {u Down}
send, {u Up}
send, {p Down}
send, {p Up}
send, {c Down}
send, {c Up}
send, {Enter Down}
send, {Enter Up}
sleep, 300
send, {c Down}
send, {c Up}
send, {c Down}
send, {c Up}
send, {Enter Down}
send, {Enter Up}
sleep, 1000
send, {c Down}
send, {c Up}
send, {Space Down}
send, {Space Up}
send, {d Down}
send, {d Up}
send, {d Down}
send, {d Up}
send, {Enter Down}
send, {Enter Up}
return
