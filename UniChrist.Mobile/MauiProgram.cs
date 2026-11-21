using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using UniChrist.Mobile.Services;

namespace UniChrist.Mobile;

public static class MauiProgram
{
    public static MauiApp CreateMauiApp()
    {
        var builder = MauiApp.CreateBuilder();
        builder.UseMauiApp<App>();

        // Register MAUI Blazor WebView
        builder.Services.AddMauiBlazorWebView();
        builder.Services.AddBlazorWebViewDeveloperTools();

        builder.ConfigureMauiHandlers(handlers =>
        {
#if ANDROID
            Microsoft.Maui.Handlers.WebViewHandler.Mapper.AppendToMapping("CustomWebViewBackground", (handler, view) =>
            {
                handler.PlatformView.SetBackgroundColor(Android.Graphics.Color.ParseColor("#080C14"));
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
