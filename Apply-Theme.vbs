' MilaCore Theme Engine — Silent Launcher
' Adheres strictly to Rule #8: Zero console window flashing

Set objFSO = CreateObject("Scripting.FileSystemObject")
Set objShell = CreateObject("WScript.Shell")

strScriptDir = objFSO.GetParentFolderName(WScript.ScriptFullName)
strSelectorExe = objFSO.BuildPath(strScriptDir, "MilaThemeSelector.exe")
strPsScript = objFSO.BuildPath(strScriptDir, "ThemeManager.ps1")

If WScript.Arguments.Count = 0 Then
    ' Launch the modern GUI Theme Selector
    objShell.Run """" & strSelectorExe & """", 1, False
Else
    strArgs = ""
    For i = 0 To WScript.Arguments.Count - 1
        strArgs = strArgs & " """ & WScript.Arguments(i) & """"
    Next
    strCmd = "powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File """ & strPsScript & """" & strArgs
    objShell.Run strCmd, 0, False
End If
