Dim answer
Dim objShell

' Create a WScript.Shell object
Set objShell = CreateObject("WScript.Shell")

' Display the message box
answer = MsgBox("Do you have Python?", vbOKCancel, "Python Check")

' Check the user's response
If answer = vbCancel Then
    ' User clicked "Cancel"
    ' Open a .txt file
    objShell.Run "notepad.exe assets\file.txt"
Else
    ' User clicked "OK"
    ' Run the batch file
    objShell.Run "assets\main.bat"
End If

' Clean up
Set objShell = Nothing

