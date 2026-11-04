# 2026-09-07 03:40:00 : 1.1.0 : ThemeManager.ps1
# 2026-09-07 03:40:00 : 1.1.0 : Upgraded with unified 5-styler Windhawk orchestration, macOS Tahoe dock mode, and Winstep Nexus Ultimate integration
# MilaCore ThemeManager - Universal Portable Engine (Windows OS, 5-Styler Windhawk, and Applications)

param(
    [string]$Apply = "",
    [switch]$List,
    [switch]$Revert,
    [switch]$Gui,
    [switch]$TahoeDock,
    [switch]$Winstep
)

$ScriptDir = $PSScriptRoot
$WindhawkExe = Join-Path $ScriptDir "windhawk.exe"
if (-not (Test-Path $WindhawkExe)) {
    $WindhawkExe = "C:\Program Files\Windhawk\windhawk.exe"
}
$WinstepExe = "C:\Program Files (x86)\Winstep\Nexus-Ultimate.exe"

$MilaDir = Join-Path $ScriptDir "Presets_MilaUniverse"
$LinkVegasDir = Join-Path $ScriptDir "Presets_LinkVegas"

function Get-AllThemes {
    $themes = @()
    
    # 1. MilaCore Universe Presets
    if (Test-Path $MilaDir) {
        Get-ChildItem -Directory $MilaDir | ForEach-Object {
            $cfgPath = Join-Path $_.FullName "config.json"
            if (Test-Path $cfgPath) {
                $c = Get-Content $cfgPath -Raw | ConvertFrom-Json
                $themes += @{
                    Id              = $c.Id
                    Name            = $c.Name
                    Category        = "MilaCore Signature Universe"
                    Path            = $_.FullName
                    Description     = $c.Description
                    Accent          = $c.Accent
                    Background      = $c.Background
                    Border          = $c.Border
                    IsWindowsNative = $false
                }
            }
        }
    }

    # 2. LinkVegas Community Presets
    if (Test-Path $LinkVegasDir) {
        Get-ChildItem -Directory $LinkVegasDir | ForEach-Object {
            $cfgPath = Join-Path $_.FullName "config.json"
            if (Test-Path $cfgPath) {
                $c = Get-Content $cfgPath -Raw | ConvertFrom-Json
                $themes += @{
                    Id              = $c.Id
                    Name            = $c.Name
                    Category        = "LinkVegas Community Overhauls"
                    Path            = $_.FullName
                    Description     = $c.Description
                    Accent          = $c.Accent
                    Background      = $c.Background
                    Border          = $c.Border
                    IsWindowsNative = $false
                }
            }
        }
    }

    # 3. Native Windows 11 Desktop System Themes
    $winThemePaths = @(
        "C:\Windows\Resources\Themes",
        (Join-Path $env:LOCALAPPDATA "Microsoft\Windows\Themes")
    )
    foreach ($wtp in $winThemePaths) {
        if (Test-Path $wtp) {
            Get-ChildItem -Path $wtp -Filter "*.theme" | ForEach-Object {
                $themes += @{
                    Id              = "Win_" + $_.BaseName
                    Name            = "Windows 11 ($($_.BaseName))"
                    Category        = "Windows 11 Native System Themes"
                    Path            = $_.FullName
                    Description     = "Official Microsoft Windows 11 Desktop and Shell Theme Pack"
                    Accent          = "#0078D4"
                    Background      = "#0B0E14"
                    Border          = "#38BDF8"
                    IsWindowsNative = $true
                }
            }
        }
    }

    return $themes
}

$allThemes = Get-AllThemes

if ($List) {
    Write-Host ""
    Write-Host "=================================================================" -ForegroundColor Cyan
    Write-Host "   MILA CORE UNIVERSAL THEME ENGINE - WINDOWS OS & APP PRESETS" -ForegroundColor Cyan
    Write-Host "=================================================================" -ForegroundColor Cyan
    
    $grouped = $allThemes | Group-Object { $_["Category"] }
    foreach ($g in $grouped) {
        $count = $g.Group.Count
        Write-Host ""
        Write-Host "Category: $($g.Name) ($count Themes)" -ForegroundColor Yellow
        Write-Host "-----------------------------------------------------------------" -ForegroundColor DarkGray
        foreach ($t in $g.Group) {
            Write-Host ("  [{0,-28}] - {1}" -f $t["Id"], $t["Name"]) -ForegroundColor Green
            Write-Host ("      {0}" -f $t["Description"]) -ForegroundColor DarkGray
        }
    }
    Write-Host ""
    Write-Host "To apply a theme across all 5 Windhawk stylers and MilaCore Apps, run:" -ForegroundColor Cyan
    Write-Host "  .\ThemeManager.ps1 -Apply macOSTahoe" -ForegroundColor White
    Write-Host "  .\ThemeManager.ps1 -Apply LiquidGlassUltimate -TahoeDock" -ForegroundColor White
    Write-Host "  .\ThemeManager.ps1 -Apply IronManGlossy -Winstep" -ForegroundColor White
    Write-Host ""
    Write-Host "To launch the GUI Theme Selector, run:" -ForegroundColor Cyan
    Write-Host "  .\ThemeManager.ps1 -Gui" -ForegroundColor White
    Write-Host ""
    exit 0
}

if ($Revert) {
    Write-Host "Reverting Windows 11 and Windhawk styling to stock defaults..." -ForegroundColor Yellow
    
    # Apply default aero.theme
    $aero = "C:\Windows\Resources\Themes\aero.theme"
    if (Test-Path $aero) {
        Start-Process "rundll32.exe" -ArgumentList ('themecpl.dll,OpenThemeAction "{0}"' -f $aero)
    }

    $revertScript = @'
$stylers = @(
    "windows-11-taskbar-styler",
    "windows-11-start-menu-styler",
    "windows-11-settings-styler",
    "windows-11-notification-center-styler",
    "windows-11-file-explorer-styler"
)
foreach ($s in $stylers) {
    Remove-Item "HKLM:\SOFTWARE\Windhawk\Engine\Mods\$s\Settings" -Recurse -ErrorAction SilentlyContinue
}
'@
    $tmpRevert = [System.IO.Path]::Combine($env:TEMP, "revert_windhawk.ps1")
    Set-Content -Path $tmpRevert -Value $revertScript -Encoding UTF8
    Start-Process powershell.exe -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$tmpRevert`"" -Verb RunAs -Wait -WindowStyle Hidden
    Remove-Item -Path $tmpRevert -Force -ErrorAction SilentlyContinue

    if (Test-Path $WindhawkExe) {
        Start-Process -FilePath $WindhawkExe -ArgumentList "-restart -tray-only" -WindowStyle Hidden
    }
    Write-Host "Reverted to stock Windows 11 theme and shell styles across all 5 stylers." -ForegroundColor Green
    exit 0
}

if ($Gui -or [string]::IsNullOrWhiteSpace($Apply)) {
    $guiExe = Join-Path $ScriptDir "MilaThemeSelector.exe"
    if (Test-Path $guiExe) {
        Start-Process -FilePath $guiExe -WorkingDirectory $ScriptDir
        exit 0
    }
}

$target = $allThemes | Where-Object { 
    $_["Id"] -ieq $Apply -or 
    $_["Name"] -ieq $Apply -or 
    $_["Id"] -ieq ("Win_" + $Apply) 
} | Select-Object -First 1

if (-not $target) {
    Write-Error ("Theme '{0}' not found. Run .\ThemeManager.ps1 -List to see all available IDs." -f $Apply)
    exit 1
}

Write-Host ("Applying Theme: [{0}] ({1})..." -f $target["Name"], $target["Category"]) -ForegroundColor Cyan

# 1. Native Windows 11 Theme Pack Application
if ($target["IsWindowsNative"]) {
    Write-Host "Activating native Windows .theme pack..." -ForegroundColor DarkGray
    Start-Process "rundll32.exe" -ArgumentList ('themecpl.dll,OpenThemeAction "{0}"' -f $target["Path"])
}
else {
    # 2. Custom Theme: Apply Windows 11 Dark/Light Mode and Accent Color
    try {
        $bg = $target["Background"]
        $cleanBg = $bg.TrimStart('#')
        $isDark = $true
        if ($cleanBg.Length -ge 6) {
            $r = [Convert]::ToByte($cleanBg.Substring(0, 2), 16)
            $g = [Convert]::ToByte($cleanBg.Substring(2, 2), 16)
            $b = [Convert]::ToByte($cleanBg.Substring(4, 2), 16)
            $lum = (0.299 * $r + 0.587 * $g + 0.114 * $b) / 255.0
            $isDark = ($lum -lt 0.55)
        }
        $darkVal = if ($isDark) { 0 } else { 1 }

        Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize" -Name "AppsUseLightTheme" -Value $darkVal -ErrorAction SilentlyContinue
        Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize" -Name "SystemUsesLightTheme" -Value $darkVal -ErrorAction SilentlyContinue

        $cleanHex = $target["Accent"].TrimStart('#')
        if ($cleanHex.Length -eq 6) { $cleanHex = "FF" + $cleanHex }
        $colorVal = [Convert]::ToUInt32($cleanHex, 16)
        Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\DWM" -Name "AccentColor" -Value $colorVal -ErrorAction SilentlyContinue
        Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\DWM" -Name "ColorizationColor" -Value $colorVal -ErrorAction SilentlyContinue
        Write-Host "Synchronized Windows 11 DWM accent palette and mode." -ForegroundColor DarkGray
    }
    catch { }

    # 2b. Synchronize Desktop Wallpaper
    $wpJpg = Join-Path $target["Path"] "wallpaper.jpg"
    $wpPng = Join-Path $target["Path"] "wallpaper.png"
    $activeWp = if (Test-Path $wpJpg) { $wpJpg } elseif (Test-Path $wpPng) { $wpPng } else { $null }

    if ($activeWp) {
        try {
            $setWpCode = @'
using System;
using System.Runtime.InteropServices;

public class DesktopWallpaperEngine {
    [DllImport("user32.dll", CharSet = CharSet.Auto)]
    public static extern int SystemParametersInfo(int uAction, int uParam, string lpvParam, int fuWinIni);
}
'@
            if (-not ([System.Management.Automation.PSTypeName]'DesktopWallpaperEngine').Type) {
                Add-Type -TypeDefinition $setWpCode -ErrorAction SilentlyContinue
            }
            [DesktopWallpaperEngine]::SystemParametersInfo(20, 0, $activeWp, 3) | Out-Null
            Set-ItemProperty -Path "HKCU:\Control Panel\Desktop" -Name "Wallpaper" -Value $activeWp -ErrorAction SilentlyContinue
            Write-Host ("Set desktop wallpaper to: {0}" -f (Split-Path $activeWp -Leaf)) -ForegroundColor DarkGray
        }
        catch {
            Write-Warning "Could not update desktop wallpaper: $_"
        }
    }

    # 3. Import Windhawk Registry Styler Configuration (Unified 5-Styler Engine)
    $regFile = Join-Path $target["Path"] "windhawk_settings.reg"
    $useTahoe = $TahoeDock -or ($target["Id"] -match "tahoe|mac")

    $applyScript = @"
if (Test-Path '$regFile') {
    Start-Process 'reg.exe' -ArgumentList 'import "$regFile"' -Wait -WindowStyle Hidden
}

# 5-Styler Enforcement
`$taskbarKey = 'HKLM:\SOFTWARE\Windhawk\Engine\Mods\windows-11-taskbar-styler\Settings'
if (-not (Test-Path `$taskbarKey)) { New-Item -Path `$taskbarKey -Force | Out-Null }
Set-ItemProperty -Path `$taskbarKey -Name 'theme' -Value 'TranslucentTaskbar' -Force
Set-ItemProperty -Path `$taskbarKey -Name 'clickThroughTaskbar' -Value 1 -Type DWord -Force
Set-ItemProperty -Path `$taskbarKey -Name 'xamlDiagnosticsHandling' -Value 'alert' -Force

# Disable duplicate taskbar-dock-animation to prevent icon hitbox collisions
Set-ItemProperty -Path 'HKLM:\SOFTWARE\Windhawk\Engine\Mods\taskbar-dock-animation' -Name 'Disabled' -Value 1 -Type DWord -Force

# Ensure Start Menu Styler
`$startKey = 'HKLM:\SOFTWARE\Windhawk\Engine\Mods\windows-11-start-menu-styler\Settings'
if (-not (Test-Path `$startKey)) { New-Item -Path `$startKey -Force | Out-Null }
`$curStart = (Get-ItemProperty -Path `$startKey -Name 'theme' -ErrorAction SilentlyContinue).theme
if ([string]::IsNullOrWhiteSpace(`$curStart)) {
    Set-ItemProperty -Path `$startKey -Name 'theme' -Value 'LiquidGlass2' -Force
    Set-ItemProperty -Path `$startKey -Name 'disableNewStartMenuLayout' -Value 'default' -Force
}

# Ensure Settings Styler
`$settingsKey = 'HKLM:\SOFTWARE\Windhawk\Engine\Mods\windows-11-settings-styler\Settings'
if (-not (Test-Path `$settingsKey)) { New-Item -Path `$settingsKey -Force | Out-Null }
`$curSettings = (Get-ItemProperty -Path `$settingsKey -Name 'theme' -ErrorAction SilentlyContinue).theme
if ([string]::IsNullOrWhiteSpace(`$curSettings)) {
    Set-ItemProperty -Path `$settingsKey -Name 'theme' -Value 'Translucent Settings11' -Force
}

# Ensure Notification Center Styler
`$notifKey = 'HKLM:\SOFTWARE\Windhawk\Engine\Mods\windows-11-notification-center-styler\Settings'
if (-not (Test-Path `$notifKey)) { New-Item -Path `$notifKey -Force | Out-Null }
`$curNotif = (Get-ItemProperty -Path `$notifKey -Name 'theme' -ErrorAction SilentlyContinue).theme
if ([string]::IsNullOrWhiteSpace(`$curNotif)) {
    Set-ItemProperty -Path `$notifKey -Name 'theme' -Value 'LiquidGlass' -Force
}

# Ensure File Explorer Styler
`$explorerKey = 'HKLM:\SOFTWARE\Windhawk\Engine\Mods\windows-11-file-explorer-styler\Settings'
if (-not (Test-Path `$explorerKey)) { New-Item -Path `$explorerKey -Force | Out-Null }
`$curExplorer = (Get-ItemProperty -Path `$explorerKey -Name 'theme' -ErrorAction SilentlyContinue).theme
if ([string]::IsNullOrWhiteSpace(`$curExplorer)) {
    Set-ItemProperty -Path `$explorerKey -Name 'theme' -Value 'OS26 Liquid Glass' -Force
    Set-ItemProperty -Path `$explorerKey -Name 'backgroundTranslucentEffect' -Value 'acrylic' -Force
    Set-ItemProperty -Path `$explorerKey -Name 'backgroundTranslucentEffectRegion' -Value 'entireWindow' -Force
}

# Broadcast SettingsChangeTime to trigger live hooks
`$now = [int][double]::Parse((Get-Date -UFormat %s))
`$mods = @('windows-11-taskbar-styler','windows-11-start-menu-styler','windows-11-settings-styler','windows-11-notification-center-styler','windows-11-file-explorer-styler')
foreach (`$m in `$mods) {
    Set-ItemProperty -Path `"HKLM:\SOFTWARE\Windhawk\Engine\Mods\`$m`" -Name 'SettingsChangeTime' -Value `$now -Type DWord -Force
}
"@

    $tmpScript = [System.IO.Path]::Combine($env:TEMP, "apply_theme_windhawk.ps1")
    Set-Content -Path $tmpScript -Value $applyScript -Encoding UTF8
    Start-Process powershell.exe -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$tmpScript`"" -Verb RunAs -Wait -WindowStyle Hidden
    Remove-Item -Path $tmpScript -Force -ErrorAction SilentlyContinue

    Write-Host "Orchestrated all 5 Windhawk stylers." -ForegroundColor DarkGray

    # 4. Reload Windhawk in tray-only mode silently
    if (Test-Path $WindhawkExe) {
        Start-Process -FilePath $WindhawkExe -ArgumentList "-restart -tray-only" -WindowStyle Hidden
        Write-Host "Windhawk shell mod reloaded silently." -ForegroundColor DarkGray
    }
}

# 5. Winstep Nexus Ultimate Companion Support
if ($Winstep -or ($target["Category"] -eq "MilaCore Signature Universe")) {
    if (Test-Path $WinstepExe) {
        $nexusProc = Get-Process "Nexus-Ultimate" -ErrorAction SilentlyContinue
        if (-not $nexusProc) {
            Start-Process -FilePath $WinstepExe -WindowStyle Hidden
            Write-Host "Winstep Nexus Ultimate dock activated for companion immersion." -ForegroundColor DarkGray
        }
    }
}

# 6. Synchronize MilaCore Applications
try {
    $mcKey = "HKCU:\Software\MilaCore"
    if (-not (Test-Path $mcKey)) { New-Item -Path $mcKey -Force | Out-Null }
    Set-ItemProperty -Path $mcKey -Name "ActiveTheme" -Value $target["Id"]
    Set-ItemProperty -Path $mcKey -Name "ActiveThemeName" -Value $target["Name"]
    Set-ItemProperty -Path $mcKey -Name "AccentColor" -Value $target["Accent"]
    Set-ItemProperty -Path $mcKey -Name "BackgroundColor" -Value $target["Background"]
    Write-Host "Synchronized MilaCore application theme settings." -ForegroundColor DarkGray
}
catch { }

Write-Host ("Theme [{0}] successfully applied to Windows OS, all 5 Windhawk stylers, and MilaCore applications!" -f $target["Name"]) -ForegroundColor Green

