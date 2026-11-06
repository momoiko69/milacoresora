using System;
using System.IO;
using System.Windows;

namespace MilaThemeSelector;

public partial class App : Application
{
    private static readonly string CrashLog = @"C:\Users\k69-admin\.gemini\MilaCore_ThemeEngine_Portable\crash.log";

    protected override void OnStartup(StartupEventArgs e)
    {
        AppDomain.CurrentDomain.UnhandledException += (s, args) =>
        {
            try { File.WriteAllText(CrashLog, "AppDomain Unhandled: " + args.ExceptionObject.ToString()); } catch { }
        };
        DispatcherUnhandledException += (s, args) =>
        {
            try { File.WriteAllText(CrashLog, "Dispatcher Unhandled: " + args.Exception.ToString()); } catch { }
            // Do not suppress if fatal
        };
        base.OnStartup(e);
    }
}
