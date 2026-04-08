# Create Desktop Shortcut for CNC Image Tool
$WScriptShell = New-Object -ComObject WScript.Shell
$Desktop = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $Desktop "CNC Image Tool.lnk"

$Shortcut = $WScriptShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = Join-Path $PSScriptRoot "launch.bat"
$Shortcut.WorkingDirectory = $PSScriptRoot
$Shortcut.Description = "CNC Image Preparation Tool for Wood Carving"
$Shortcut.Save()

Write-Host "Desktop shortcut created successfully!" -ForegroundColor Green
Write-Host "Location: $ShortcutPath" -ForegroundColor Cyan
