# Register the Email Summarizer backend to start on user login
# Run this script as Administrator (or the current user)

$taskName = "EmailSummarizerBackend"
$scriptPath = "C:\email-summarizer\start_backend.vbs"
$action = New-ScheduledTaskAction -Execute "wscript.exe" -Argument "`"$scriptPath`""
$trigger = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType S4U -RunLevel Limited

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Force

Write-Host "Auto-start registered. Backend will start automatically on next login."
Write-Host "You can also start it manually: wscript C:\email-summarizer\start_backend.vbs"
