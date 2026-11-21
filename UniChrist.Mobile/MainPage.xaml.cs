using Microsoft.AspNetCore.Components.WebView.Maui;
using UniChrist.Mobile.Components;

namespace UniChrist.Mobile;

public partial class MainPage : ContentPage
{
    public MainPage()
    {
        InitializeComponent();

        // Programmatic initialization guarantees compile-time resolution of Routes component and bypasses XAML type resolution issues
        var blazorWebView = new BlazorWebView
        {
            HostPage = "wwwroot/index.html",
            BackgroundColor = Color.FromArgb("#080C14")
        };

        blazorWebView.RootComponents.Add(new RootComponent
        {
            Selector = "#app",
            ComponentType = typeof(Routes)
        });

        Content = blazorWebView;
    }
}
