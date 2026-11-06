using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text.Json;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;

namespace MilaThemeSelector
{
    public class ThemeItem
    {
        public string Id { get; set; } = "";
        public string Name { get; set; } = "";
        public string Category { get; set; } = "";
        public string Background { get; set; } = "#0B0F17";
        public string Accent { get; set; } = "#38BDF8";
        public string Border { get; set; } = "#1E293B";
        public int CornerRadius { get; set; } = 12;
        public bool IsFloating { get; set; } = true;
        public string Description { get; set; } = "";
        public string DirectoryPath { get; set; } = "";
        public string? NativeThemePath { get; set; }
        public bool IsNativeWindowsTheme => !string.IsNullOrEmpty(NativeThemePath);

        public Brush AccentBrush
        {
            get
            {
                try { return new SolidColorBrush((Color)ColorConverter.ConvertFromString(Accent)); }
                catch { return Brushes.Cyan; }
            }
        }
    }

    public partial class MainWindow : Window
    {
        [DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Auto)]
        private static extern IntPtr SendMessageTimeout(
            IntPtr hWnd,
            uint Msg,
            UIntPtr wParam,
            string lParam,
            uint fuFlags,
            uint uTimeout,
            out UIntPtr lpdwResult);

        [DllImport("user32.dll", CharSet = CharSet.Auto)]
        private static extern int SystemParametersInfo(int uAction, int uParam, string lpvParam, int fuWinIni);

        private const int SPI_SETDESKWALLPAPER = 20;
        private const int SPIF_UPDATEINIFILE = 0x01;
        private const int SPIF_SENDCHANGE = 0x02;

        private const uint HWND_BROADCAST = 0xffff;
        private const uint WM_SETTINGCHANGE = 0x001A;
        private const uint SMTO_ABORTIFHUNG = 0x0002;

        private List<ThemeItem> _allThemes = new();
        private ThemeItem? _selectedTheme;
        private string _portableRoot = "";

        public MainWindow()
        {
            var logPath = @"C:\Users\k69-admin\.gemini\MilaCore_ThemeEngine_Portable\selector_debug.log";
            try
            {
                File.WriteAllText(logPath, "Starting InitializeComponent...\n");
                InitializeComponent();
                File.AppendAllText(logPath, "InitializeComponent done. Resolving paths...\n");
                ResolvePaths();
                File.AppendAllText(logPath, $"Paths resolved: {_portableRoot}. Loading themes...\n");
                LoadThemes();
                File.AppendAllText(logPath, $"Themes loaded: {_allThemes.Count}\n");
            }
            catch (Exception ex)
            {
                File.AppendAllText(logPath, $"ERROR in constructor: {ex}\n");
            }
        }

        private void ResolvePaths()
        {
            var current = AppDomain.CurrentDomain.BaseDirectory;
            var candidates = new[]
            {
                current,
                Path.Combine(current, "..", "..", ".."),
                @"C:\Users\k69-admin\.gemini\MilaCore_ThemeEngine_Portable"
            };

            foreach (var c in candidates)
            {
                if (Directory.Exists(Path.Combine(c, "Presets_MilaUniverse")))
                {
                    _portableRoot = Path.GetFullPath(c);
                    break;
                }
            }

            if (string.IsNullOrEmpty(_portableRoot))
                _portableRoot = @"C:\Users\k69-admin\.gemini\MilaCore_ThemeEngine_Portable";
        }

        private void LoadThemes()
        {
            _allThemes.Clear();

            // 1. Mila Universe Themes
            var milaPath = Path.Combine(_portableRoot, "Presets_MilaUniverse");
            if (Directory.Exists(milaPath))
            {
                foreach (var dir in Directory.GetDirectories(milaPath))
                {
                    var cfg = Path.Combine(dir, "config.json");
                    if (File.Exists(cfg))
                    {
                        try
                        {
                            var json = File.ReadAllText(cfg);
                            var item = JsonSerializer.Deserialize<ThemeItem>(json, new JsonSerializerOptions { PropertyNameCaseInsensitive = true });
                            if (item != null)
                            {
                                item.DirectoryPath = dir;
                                item.Category = "🌟 MilaCore Universe";
                                _allThemes.Add(item);
                            }
                        }
                        catch { }
                    }
                }
            }

            // 2. LinkVegas Themes
            var lvPath = Path.Combine(_portableRoot, "Presets_LinkVegas");
            if (Directory.Exists(lvPath))
            {
                foreach (var dir in Directory.GetDirectories(lvPath))
                {
                    var cfg = Path.Combine(dir, "config.json");
                    if (File.Exists(cfg))
                    {
                        try
                        {
                            var json = File.ReadAllText(cfg);
                            var item = JsonSerializer.Deserialize<ThemeItem>(json, new JsonSerializerOptions { PropertyNameCaseInsensitive = true });
                            if (item != null)
                            {
                                item.DirectoryPath = dir;
                                item.Category = "🌐 LinkVegas Overhauls";
                                _allThemes.Add(item);
                            }
                        }
                        catch { }
                    }
                }
            }

            // 3. Windows 11 Native System Themes
            LoadWindowsNativeThemes();

            RefreshList();
        }

        private void LoadWindowsNativeThemes()
        {
            var searchPaths = new List<string>
            {
                @"C:\Windows\Resources\Themes",
                Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), @"Microsoft\Windows\Themes")
            };

            foreach (var sp in searchPaths)
            {
                if (!Directory.Exists(sp)) continue;

                foreach (var themeFile in Directory.GetFiles(sp, "*.theme"))
                {
                    var fn = Path.GetFileNameWithoutExtension(themeFile);
                    string displayName;
                    string accent = "#0078D4";
                    string bg = "#0B0E14";
                    string desc = "Native Windows 11 System Theme";

                    switch (fn.ToLower())
                    {
                        case "aero":
                            displayName = "Windows 11 Light (Aero Flow)";
                            accent = "#0078D4";
                            bg = "#F3F4F6";
                            desc = "Official Windows 11 default light mode aesthetic with Fluent glass.";
                            break;
                        case "dark":
                            displayName = "Windows 11 Dark Mode";
                            accent = "#60CDFF";
                            bg = "#111827";
                            desc = "Official Windows 11 dark mode theme with high-contrast acrylic blur.";
                            break;
                        case "spotlight":
                            displayName = "Windows Spotlight Dynamic";
                            accent = "#38BDF8";
                            bg = "#0F172A";
                            desc = "Dynamic daily photographic wallpaper curated by Bing and Windows Spotlight.";
                            break;
                        case "themea":
                            displayName = "Windows 11 Flow (Theme A)";
                            accent = "#0284C7";
                            bg = "#1E293B";
                            desc = "Windows 11 signature blue silk flow aesthetic.";
                            break;
                        case "themeb":
                            displayName = "Windows 11 Sunrise (Theme B)";
                            accent = "#F59E0B";
                            bg = "#292524";
                            desc = "Warm ambient solar sunrise tones on dark acrylic.";
                            break;
                        case "themec":
                            displayName = "Windows 11 Glow (Theme C)";
                            accent = "#8B5CF6";
                            bg = "#1E1B4B";
                            desc = "Vibrant violet and iridescent neon glow on midnight glass.";
                            break;
                        case "themed":
                            displayName = "Windows 11 Captured Motion (Theme D)";
                            accent = "#EC4899";
                            bg = "#271025";
                            desc = "Kinetic fluid motion with electric magenta and rose accents.";
                            break;
                        default:
                            displayName = $"Windows Custom ({fn})";
                            accent = "#38BDF8";
                            bg = "#111722";
                            desc = $"Custom installed Windows theme pack: {Path.GetFileName(themeFile)}";
                            break;
                    }

                    _allThemes.Add(new ThemeItem
                    {
                        Id = "Win_" + fn,
                        Name = displayName,
                        Category = "🪟 Windows System Themes",
                        Background = bg,
                        Accent = accent,
                        Border = accent,
                        CornerRadius = 12,
                        IsFloating = false,
                        Description = desc,
                        DirectoryPath = sp,
                        NativeThemePath = themeFile
                    });
                }
            }
        }

        private void RefreshList()
        {
            var isMilaTab = TabMila.IsChecked == true;
            var isLinkVegasTab = TabLinkVegas.IsChecked == true;
            var isWinTab = TabWinThemes.IsChecked == true;
            var search = TxtSearch.Text.Trim().ToLower();

            var filtered = _allThemes.Where(t =>
            {
                if (isWinTab && !t.IsNativeWindowsTheme) return false;
                if (isMilaTab && (!t.Category.Contains("MilaCore") || t.IsNativeWindowsTheme)) return false;
                if (isLinkVegasTab && (!t.Category.Contains("LinkVegas") || t.IsNativeWindowsTheme)) return false;

                if (!string.IsNullOrEmpty(search))
                {
                    return t.Name.ToLower().Contains(search) || t.Id.ToLower().Contains(search) || t.Description.ToLower().Contains(search);
                }
                return true;
            }).OrderBy(t => t.Name).ToList();

            LstThemes.ItemsSource = filtered;
            if (filtered.Count > 0 && (_selectedTheme == null || !filtered.Contains(_selectedTheme)))
            {
                LstThemes.SelectedIndex = 0;
            }
        }

        private void Category_Changed(object sender, RoutedEventArgs e)
        {
            if (IsLoaded) RefreshList();
        }

        private void TxtSearch_TextChanged(object sender, TextChangedEventArgs e)
        {
            TxtPlaceholder.Visibility = string.IsNullOrEmpty(TxtSearch.Text) ? Visibility.Visible : Visibility.Collapsed;
            RefreshList();
        }

        private void LstThemes_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (LstThemes.SelectedItem is ThemeItem item)
            {
                _selectedTheme = item;
                UpdatePreview(item);
            }
        }

        private void UpdatePreview(ThemeItem t)
        {
            LblThemeTitle.Text = t.Name;
            LblThemeCategory.Text = $"Category: {t.Category}";
            LblThemeDesc.Text = t.Description;

            try
            {
                var bgCol = (Color)ColorConverter.ConvertFromString(t.Background);
                var accentCol = (Color)ColorConverter.ConvertFromString(t.Accent);
                var borderCol = (Color)ColorConverter.ConvertFromString(t.Border);

                SwatchBg.Background = new SolidColorBrush(bgCol);
                TxtHexBg.Text = t.Background;

                SwatchAccent.Background = new SolidColorBrush(accentCol);
                TxtHexAccent.Text = t.Accent;

                SwatchBorder.Background = new SolidColorBrush(borderCol);
                TxtHexBorder.Text = t.Border;

                TxtRadiusInfo.Text = t.IsNativeWindowsTheme 
                    ? "Native Windows 11 Desktop Theme Pack" 
                    : $"Radius: {t.CornerRadius}px • {(t.IsFloating ? "Floating Dock" : "Standard Dock")}";

                // Update Preview Mockups
                PreviewWindow.Background = new SolidColorBrush(bgCol);
                PreviewWindow.BorderBrush = new SolidColorBrush(accentCol);
                TxtPreviewAccent.Foreground = new SolidColorBrush(accentCol);

                PreviewTaskbar.Background = new SolidColorBrush(bgCol);
                PreviewTaskbar.BorderBrush = new SolidColorBrush(accentCol);
                PreviewTaskbar.CornerRadius = new CornerRadius(t.CornerRadius);
            }
            catch { }
        }

        private void ApplyCustomWindowsTheme(ThemeItem t)
        {
            try
            {
                var isDark = !t.Background.StartsWith("#F", StringComparison.OrdinalIgnoreCase) && 
                             !t.Background.StartsWith("#E", StringComparison.OrdinalIgnoreCase);
                var mode = isDark ? "Dark" : "Light";

                // Parse hex color (e.g. "#FF1E42")
                var hex = t.Accent.TrimStart('#');
                if (hex.Length == 3)
                    hex = $"{hex[0]}{hex[0]}{hex[1]}{hex[1]}{hex[2]}{hex[2]}";
                if (hex.Length != 6) hex = "0078D4";

                byte r = Convert.ToByte(hex.Substring(0, 2), 16);
                byte g = Convert.ToByte(hex.Substring(2, 2), 16);
                byte b = Convert.ToByte(hex.Substring(4, 2), 16);

                // Windows DWM / Explorer expects ABGR (0xAABBGGRR)
                uint abgr = ((uint)0xFF << 24) | ((uint)b << 16) | ((uint)g << 8) | (uint)r;
                // ARGB for ColorizationColor / .theme file (0xAARRGGBB)
                uint argb = ((uint)0xFF << 24) | ((uint)r << 16) | ((uint)g << 8) | (uint)b;

                int abgrInt = unchecked((int)abgr);
                int argbInt = unchecked((int)argb);

                // Synthesize 32-byte AccentPalette (8 tiered RGBA colors)
                byte[] palette = new byte[32];
                double[] factors = { 1.6, 1.4, 1.2, 1.0, 0.8, 0.6, 0.4, 0.25 };
                for (int i = 0; i < 8; i++)
                {
                    double f = factors[i];
                    palette[i * 4 + 0] = (byte)Math.Min(255, Math.Max(0, (int)(r * f)));
                    palette[i * 4 + 1] = (byte)Math.Min(255, Math.Max(0, (int)(g * f)));
                    palette[i * 4 + 2] = (byte)Math.Min(255, Math.Max(0, (int)(b * f)));
                    palette[i * 4 + 3] = 0;
                }

                // Check for dedicated wallpaper
                string wallpaperPath = "";
                var possibleWallpapers = new[] {
                    Path.Combine(t.DirectoryPath, "wallpaper.jpg"),
                    Path.Combine(t.DirectoryPath, "wallpaper.png"),
                    Path.Combine(t.DirectoryPath, "background.jpg"),
                    Path.Combine(t.DirectoryPath, "background.png")
                };
                foreach (var wp in possibleWallpapers)
                {
                    if (File.Exists(wp))
                    {
                        wallpaperPath = wp;
                        break;
                    }
                }

                // Apply Wallpaper if found
                if (!string.IsNullOrEmpty(wallpaperPath))
                {
                    SystemParametersInfo(SPI_SETDESKWALLPAPER, 0, wallpaperPath, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE);
                }

                // 1. Direct registry synchronization for DWM, Personalize, and Explorer Accent
                using (var keyPers = Microsoft.Win32.Registry.CurrentUser.CreateSubKey(@"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"))
                {
                    keyPers?.SetValue("AppsUseLightTheme", isDark ? 0 : 1, Microsoft.Win32.RegistryValueKind.DWord);
                    keyPers?.SetValue("SystemUsesLightTheme", isDark ? 0 : 1, Microsoft.Win32.RegistryValueKind.DWord);
                    keyPers?.SetValue("ColorPrevalence", 1, Microsoft.Win32.RegistryValueKind.DWord);
                }

                using (var keyDwm = Microsoft.Win32.Registry.CurrentUser.CreateSubKey(@"Software\Microsoft\Windows\DWM"))
                {
                    keyDwm?.SetValue("AccentColor", abgrInt, Microsoft.Win32.RegistryValueKind.DWord);
                    keyDwm?.SetValue("ColorizationColor", argbInt, Microsoft.Win32.RegistryValueKind.DWord);
                    keyDwm?.SetValue("ColorPrevalence", 1, Microsoft.Win32.RegistryValueKind.DWord);
                }

                using (var keyAccent = Microsoft.Win32.Registry.CurrentUser.CreateSubKey(@"Software\Microsoft\Windows\CurrentVersion\Explorer\Accent"))
                {
                    keyAccent?.SetValue("AccentColorMenu", abgrInt, Microsoft.Win32.RegistryValueKind.DWord);
                    keyAccent?.SetValue("StartColorMenu", abgrInt, Microsoft.Win32.RegistryValueKind.DWord);
                    keyAccent?.SetValue("AccentPalette", palette, Microsoft.Win32.RegistryValueKind.Binary);
                }

                // Generate active .theme file
                var activeThemeFile = Path.Combine(_portableRoot, "MilaCore_Active.theme");
                var sb = new System.Text.StringBuilder();
                sb.AppendLine("; MilaCore Active Theme Engine Preset");
                sb.AppendLine("[Theme]");
                sb.AppendLine($"DisplayName=MilaCore - {t.Name}");
                sb.AppendLine("SetLogonBackground=0");
                sb.AppendLine();
                sb.AppendLine("[Control Panel\\Desktop]");
                if (!string.IsNullOrEmpty(wallpaperPath))
                    sb.AppendLine($"Wallpaper={wallpaperPath}");
                else
                    sb.AppendLine("Wallpaper=%SystemRoot%\\web\\wallpaper\\Windows\\img19.jpg");
                sb.AppendLine("TileWallpaper=0");
                sb.AppendLine("WallpaperStyle=10");
                sb.AppendLine();
                sb.AppendLine("[VisualStyles]");
                sb.AppendLine("Path=%ResourceDir%\\Themes\\Aero\\Aero.msstyles");
                sb.AppendLine("ColorStyle=NormalColor");
                sb.AppendLine("Size=NormalSize");
                sb.AppendLine("AutoColorization=0");
                sb.AppendLine($"ColorizationColor=0x{argb:X8}");
                sb.AppendLine($"SystemMode={mode}");
                sb.AppendLine($"AppMode={mode}");
                sb.AppendLine();
                sb.AppendLine("[MasterThemeSelector]");
                sb.AppendLine("MTSM=RJSPBS");

                File.WriteAllText(activeThemeFile, sb.ToString());

                // 2. Invoke Windows Theme Engine natively via rundll32
                var psi = new ProcessStartInfo(@"C:\windows\system32\rundll32.exe", $@"C:\windows\system32\themecpl.dll,OpenThemeAction ""{activeThemeFile}""")
                {
                    UseShellExecute = true
                };
                Process.Start(psi);

                // Broadcast system change
                SendMessageTimeout((IntPtr)HWND_BROADCAST, WM_SETTINGCHANGE, UIntPtr.Zero, "ImmersiveColorSet", SMTO_ABORTIFHUNG, 200, out _);
                SendMessageTimeout((IntPtr)HWND_BROADCAST, WM_SETTINGCHANGE, UIntPtr.Zero, "WindowsColorSet", SMTO_ABORTIFHUNG, 200, out _);
            }
            catch { }
        }

        private void ApplyWindhawkStyling(ThemeItem t)
        {
            try
            {
                string taskbarTheme = "TranslucentTaskbar";
                string startMenuTheme = "LiquidGlass2";
                string notifTheme = "LiquidGlass";
                string explorerTheme = "OS26 Liquid Glass";
                string settingsTheme = "Translucent Settings11";

                bool isMilaverse = t.Category.Contains("MilaCore", StringComparison.OrdinalIgnoreCase) ||
                                   t.Category.Contains("Universe", StringComparison.OrdinalIgnoreCase);

                if (isMilaverse)
                {
                    // For Milaverse themes: clean translucent taskbar, liquid glass controls across all 5 areas!
                    taskbarTheme = "TranslucentTaskbar";
                    startMenuTheme = "LiquidGlass2";
                    notifTheme = "LiquidGlass";
                    explorerTheme = "OS26 Liquid Glass";
                    settingsTheme = "Translucent Settings11";
                }
                else
                {
                    // For LinkVegas themes: Map to their specific creator design profiles
                    var id = t.Id.ToLowerInvariant();
                    if (id.Contains("rampage"))
                    {
                        taskbarTheme = "TranslucentTaskbar";
                        startMenuTheme = "LiquidGlass2";
                        notifTheme = "Matter";
                        explorerTheme = "Translucent Explorer11";
                        settingsTheme = "Translucent Settings11";
                    }
                    else if (id.Contains("tahoe") || id.Contains("macos"))
                    {
                        taskbarTheme = "TranslucentTaskbar";
                        startMenuTheme = "TranslucentStartMenu";
                        notifTheme = "TranslucentShell";
                        explorerTheme = "Translucent Explorer11";
                        settingsTheme = "Translucent Settings11";
                    }
                    else if (id.Contains("windows7") || id.Contains("win7"))
                    {
                        taskbarTheme = "Windows7";
                        startMenuTheme = "Windows10";
                        notifTheme = "10JumpLists";
                        explorerTheme = "MicaBar";
                        settingsTheme = "ClassicSearchBar";
                    }
                    else if (id.Contains("xp") || id.Contains("retroxp"))
                    {
                        taskbarTheme = "WinXP";
                        startMenuTheme = "Windows10";
                        notifTheme = "10JumpLists";
                        explorerTheme = "NoCommandBar";
                        settingsTheme = "ClassicSearchBar";
                    }
                    else if (id.Contains("liquidglass") || id.Contains("glass"))
                    {
                        taskbarTheme = "TranslucentTaskbar";
                        startMenuTheme = "LiquidGlass2";
                        notifTheme = "LiquidGlass";
                        explorerTheme = "OS26 Liquid Glass";
                        settingsTheme = "Translucent Settings11";
                    }
                    else
                    {
                        taskbarTheme = "TranslucentTaskbar";
                        startMenuTheme = "LiquidGlass2";
                        notifTheme = "LiquidGlass";
                        explorerTheme = "OS26 Liquid Glass";
                        settingsTheme = "Translucent Settings11";
                    }
                }

                // 1. Update Start Menu Styler
                using (var smKey = Microsoft.Win32.Registry.LocalMachine.CreateSubKey(@"SOFTWARE\Windhawk\Engine\Mods\windows-11-start-menu-styler\Settings"))
                {
                    smKey?.SetValue("theme", startMenuTheme);
                }

                // 2. Update Taskbar Styler
                using (var tbKey = Microsoft.Win32.Registry.LocalMachine.CreateSubKey(@"SOFTWARE\Windhawk\Engine\Mods\windows-11-taskbar-styler\Settings"))
                {
                    tbKey?.SetValue("theme", taskbarTheme);
                }

                // 3. Update Notification Center Styler
                using (var ncKey = Microsoft.Win32.Registry.LocalMachine.CreateSubKey(@"SOFTWARE\Windhawk\Engine\Mods\windows-11-notification-center-styler\Settings"))
                {
                    ncKey?.SetValue("theme", notifTheme);
                }

                // 4. Update File Explorer Styler
                using (var feKey = Microsoft.Win32.Registry.LocalMachine.CreateSubKey(@"SOFTWARE\Windhawk\Engine\Mods\windows-11-file-explorer-styler\Settings"))
                {
                    feKey?.SetValue("theme", explorerTheme);
                    feKey?.SetValue("backgroundTranslucentEffect", "acrylic");
                    feKey?.SetValue("backgroundTranslucentEffectRegion", "entireWindow");
                }

                // 5. Update Settings Styler
                using (var stKey = Microsoft.Win32.Registry.LocalMachine.CreateSubKey(@"SOFTWARE\Windhawk\Engine\Mods\windows-11-settings-styler\Settings"))
                {
                    stKey?.SetValue("theme", settingsTheme);
                }

                // Refresh running Settings process so it picks up the new styler
                foreach (var p in Process.GetProcessesByName("SystemSettings"))
                {
                    try { p.Kill(); } catch { }
                }

                // C. Import preset reg file if exists
                var regFile = Path.Combine(t.DirectoryPath, "windhawk_settings.reg");
                if (File.Exists(regFile))
                {
                    var psi = new ProcessStartInfo("reg.exe", $"import \"{regFile}\"")
                    {
                        CreateNoWindow = true,
                        UseShellExecute = false
                    };
                    Process.Start(psi)?.WaitForExit();
                }

                // D. Reload Windhawk in tray-only mode
                var windhawkExe = Path.Combine(_portableRoot, "windhawk.exe");
                if (!File.Exists(windhawkExe))
                    windhawkExe = @"C:\Program Files\Windhawk\windhawk.exe";

                if (File.Exists(windhawkExe))
                {
                    Process.Start(new ProcessStartInfo(windhawkExe, "-restart -tray-only")
                    {
                        CreateNoWindow = true,
                        UseShellExecute = false
                    });
                }
            }
            catch { }
        }

        private void BtnApply_Click(object sender, RoutedEventArgs e)
        {
            if (_selectedTheme == null) return;

            var sw = Stopwatch.StartNew();
            bool appliedWin = false;
            bool appliedApps = false;

            // 1. If it's a native Windows Theme pack (.theme file):
            if (_selectedTheme.IsNativeWindowsTheme && !string.IsNullOrEmpty(_selectedTheme.NativeThemePath))
            {
                try
                {
                    var psi = new ProcessStartInfo(@"C:\windows\system32\rundll32.exe", $@"C:\windows\system32\themecpl.dll,OpenThemeAction ""{_selectedTheme.NativeThemePath}""")
                    {
                        UseShellExecute = true
                    };
                    Process.Start(psi);
                    appliedWin = true;
                }
                catch
                {
                    Process.Start(new ProcessStartInfo(_selectedTheme.NativeThemePath) { UseShellExecute = true });
                    appliedWin = true;
                }
            }
            else
            {
                // 2. Apply Custom Theme (Mila Universe or LinkVegas) to Windows 11 Shell
                if (ChkApplyWindows.IsChecked == true)
                {
                    ApplyCustomWindowsTheme(_selectedTheme);
                    ApplyWindhawkStyling(_selectedTheme);
                    appliedWin = true;
                }
            }

            // 3. Apply to MilaCore Applications (Registry Synchronization)
            if (ChkApplyApps.IsChecked == true)
            {
                try
                {
                    using var key = Microsoft.Win32.Registry.CurrentUser.CreateSubKey(@"Software\MilaCore");
                    key?.SetValue("ActiveTheme", _selectedTheme.Id);
                    key?.SetValue("ActiveThemeName", _selectedTheme.Name);
                    key?.SetValue("AccentColor", _selectedTheme.Accent);
                    key?.SetValue("BackgroundColor", _selectedTheme.Background);
                    key?.SetValue("BorderColor", _selectedTheme.Border);
                    appliedApps = true;
                }
                catch { }
            }

            sw.Stop();
            var scopeMsg = (appliedWin && appliedApps) ? "Windows 11 System & MilaCore Apps" : (appliedWin ? "Windows 11 System" : "MilaCore Apps");
            TxtStatus.Text = $"✅ Applied '{_selectedTheme.Name}' to {scopeMsg} in {sw.ElapsedMilliseconds}ms! Desktop and apps are live.";
            TxtStatus.Foreground = Brushes.LightGreen;
        }

        private void BtnWinSettings_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                Process.Start(new ProcessStartInfo("ms-settings:themes") { UseShellExecute = true });
                TxtStatus.Text = "🪟 Opened Windows 11 Personalization > Themes Settings.";
                TxtStatus.Foreground = Brushes.LightSkyBlue;
            }
            catch (Exception ex)
            {
                TxtStatus.Text = $"Error opening settings: {ex.Message}";
                TxtStatus.Foreground = Brushes.OrangeRed;
            }
        }

        private void BtnRevert_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                // Restore Windows 11 default aero theme
                var aeroTheme = @"C:\Windows\Resources\Themes\aero.theme";
                if (File.Exists(aeroTheme))
                {
                    Process.Start(new ProcessStartInfo("rundll32.exe", $"themecpl.dll,OpenThemeAction \"{aeroTheme}\"") { UseShellExecute = true });
                }

                // Reset all 5 Windhawk stylers
                string[] modNames = new[] {
                    "windows-11-start-menu-styler",
                    "windows-11-taskbar-styler",
                    "windows-11-notification-center-styler",
                    "windows-11-file-explorer-styler",
                    "windows-11-settings-styler"
                };

                foreach (var mod in modNames)
                {
                    using var key = Microsoft.Win32.Registry.LocalMachine.OpenSubKey($@"SOFTWARE\Windhawk\Engine\Mods\{mod}", true);
                    key?.DeleteSubKeyTree("Settings", false);
                }

                var windhawkExe = Path.Combine(_portableRoot, "windhawk.exe");
                if (!File.Exists(windhawkExe)) windhawkExe = @"C:\Program Files\Windhawk\windhawk.exe";

                if (File.Exists(windhawkExe))
                {
                    Process.Start(new ProcessStartInfo(windhawkExe, "-restart -tray-only") { CreateNoWindow = true, UseShellExecute = false });
                }

                TxtStatus.Text = "🔄 Reverted to stock Windows 11 theme & styling.";
                TxtStatus.Foreground = Brushes.LightSkyBlue;
            }
            catch (Exception ex)
            {
                TxtStatus.Text = $"Error reverting: {ex.Message}";
                TxtStatus.Foreground = Brushes.OrangeRed;
            }
        }
    }
}