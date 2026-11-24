using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using UniChrist.Mobile.Services;

#if ANDROID
using Microsoft.AspNetCore.Components.WebView.Maui;
#endif

namespace UniChrist.Mobile;

public static class MauiProgram
{
    public static MauiApp CreateMauiApp()
    {
        var builder = MauiApp.CreateBuilder();
        builder.UseMauiApp<App>();

        // Register MAUI Blazor WebView
        builder.Services.AddMauiBlazorWebView();

        // Enable developer tools unconditionally for diagnostic inspection via chrome://inspect
        builder.Services.AddBlazorWebViewDeveloperTools();

        // =========================================================================
        // DOMAIN D: NATIVE PLATFORM HANDLER & ANDROID WEBVIEW BACKGROUND OVERRIDE
        // Forces native android.webkit.WebView to deep dark #080C14 at OS level
        // =========================================================================
        builder.ConfigureMauiHandlers(handlers =>
        {
#if ANDROID
            BlazorWebViewHandler.BlazorWebViewMapper.AppendToMapping("UniChristDarkBackground", (handler, view) =>
            {
                if (handler.PlatformView != null)
                {
                    handler.PlatformView.SetBackgroundColor(Android.Graphics.Color.ParseColor("#080C14"));
                    
                    // Enable remote webview debugging unconditionally for chrome://inspect
                    Android.Webkit.WebView.SetWebContentsDebuggingEnabled(true);
                    
                    // Configure WebSettings for maximum compatibility
                    handler.PlatformView.Settings.JavaScriptEnabled = true;
                    handler.PlatformView.Settings.DomStorageEnabled = true;
                    handler.PlatformView.Settings.DatabaseEnabled = true;
                    handler.PlatformView.Settings.AllowFileAccess = true;
                    handler.PlatformView.Settings.AllowContentAccess = true;
                    handler.PlatformView.Settings.MixedContentMode = Android.Webkit.MixedContentHandling.AlwaysAllow;
                }
            });
#endif
        });

#if DEBUG
        builder.Logging.AddDebug();
#endif

        // Configure Production Deployed API Address
        var apiBaseUrl = "https://unichrist-production.up.railway.app"; 

        builder.Services.AddHttpClient<IAPIService, APIService>(client =>
        {
            client.BaseAddress = new Uri(apiBaseUrl);
            client.DefaultRequestHeaders.Add("Accept", "application/json");
            client.DefaultRequestHeaders.Add("User-Agent", "UniChrist-Mobile-App/1.0");
            client.Timeout = TimeSpan.FromSeconds(30);
        });

        return builder.Build();
    }
}
