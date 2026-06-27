' Silent startup for Email Summarizer backend
' This script runs the Python server without showing a console window

Dim shell
Set shell = CreateObject("WScript.Shell")
shell.Run "C:\Users\shall\AppData\Local\Programs\Python\Python312\python.exe C:\email-summarizer\backend\main.py", 0, False
Set shell = Nothing
