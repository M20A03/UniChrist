using Microsoft.EntityFrameworkCore;
using Microsoft.OpenApi.Models;
using UniChristBackend.Data;

var builder = WebApplication.CreateBuilder(args);

// Configure Port for Railway / Cloud Deployment
var port = Environment.GetEnvironmentVariable("PORT");
if (!string.IsNullOrEmpty(port))
{
    builder.WebHost.UseUrls($"http://0.0.0.0:{port}");
}

// Add services to the container.
builder.Services.AddControllersWithViews()
    .AddJsonOptions(options =>
    {
        options.JsonSerializerOptions.ReferenceHandler = System.Text.Json.Serialization.ReferenceHandler.IgnoreCycles;
        options.JsonSerializerOptions.DefaultIgnoreCondition = System.Text.Json.Serialization.JsonIgnoreCondition.WhenWritingNull;
    });

// Configure Database Connection (Supports Localhost & Railway MySQL Service)
var connectionString = BuildConnectionString(builder.Configuration);

builder.Services.AddDbContext<UniChristDbContext>(options =>
{
    try
    {
        var serverVersion = ServerVersion.AutoDetect(connectionString);
        options.UseMySql(connectionString, serverVersion, mySqlOptions =>
        {
            mySqlOptions.EnableRetryOnFailure(
                maxRetryCount: 3,
                maxRetryDelay: TimeSpan.FromSeconds(5),
                errorNumbersToAdd: null);
        });
    }
    catch (Exception)
    {
        // Fallback to MySQL standard version specification if AutoDetect fails before DB is running
        options.UseMySql(connectionString, new MySqlServerVersion(new Version(8, 0, 36)));
    }
});

// Configure CORS
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAll", policy =>
    {
        policy.AllowAnyOrigin()
              .AllowAnyMethod()
              .AllowAnyHeader();
    });
});

// Configure Swagger / OpenAPI
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new OpenApiInfo
    {
        Title = "UniChrist Smart Campus ERP API",
        Version = "v1",
        Description = "ASP.NET Core REST API & MySQL Backend for CHRIST (Deemed to be University) - DBMS Project (BCA381-4)",
        Contact = new OpenApiContact
        {
            Name = "Mayank Raj Gupta (Lead) & Team UniChrist",
            Email = "mayank.raj@christuniversity.in"
        }
    });
});

var app = builder.Build();

// Seed Database automatically on startup
using (var scope = app.Services.CreateScope())
{
    var services = scope.ServiceProvider;
    try
    {
        var context = services.GetRequiredService<UniChristDbContext>();
        DbInitializer.Initialize(context);
    }
    catch (Exception ex)
    {
        var logger = services.GetRequiredService<ILogger<Program>>();
        logger.LogWarning(ex, "Could not seed MySQL database on startup. Ensure MySQL server is running on localhost:3306.");
    }
}

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment() || true)
{
    app.UseDeveloperExceptionPage();
    app.UseSwagger();
    app.UseSwaggerUI(c =>
    {
        c.SwaggerEndpoint("/swagger/v1/swagger.json", "UniChrist ERP API v1");
        c.RoutePrefix = "swagger";
    });
}

app.UseHttpsRedirection();
app.UseStaticFiles();

app.UseRouting();
app.UseCors("AllowAll");

app.UseAuthorization();

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");

app.MapControllers();

Console.WriteLine("=================================================================");
Console.WriteLine("  UniChrist Campus ERP Backend Server (ASP.NET Core + C# + MySQL)");
Console.WriteLine("  API Documentation (Swagger UI): http://localhost:5000/swagger");
Console.WriteLine("  Web Portal Application:         http://localhost:5000");
Console.WriteLine("=================================================================");

app.Run();

// Helper method to automatically construct MySQL connection string from Railway environment variables or local appsettings
static string BuildConnectionString(IConfiguration config)
{
    // 1. Check for Railway MySQL discrete variables
    var mysqlHost = Environment.GetEnvironmentVariable("MYSQLHOST");
    var mysqlPort = Environment.GetEnvironmentVariable("MYSQLPORT") ?? "3306";
    var mysqlUser = Environment.GetEnvironmentVariable("MYSQLUSER");
    var mysqlPass = Environment.GetEnvironmentVariable("MYSQLPASSWORD");
    var mysqlDb   = Environment.GetEnvironmentVariable("MYSQLDATABASE") ?? "railway";

    if (!string.IsNullOrEmpty(mysqlHost) && !string.IsNullOrEmpty(mysqlUser))
    {
        Console.WriteLine($"[Config] Detected Railway MySQL Service: {mysqlHost}:{mysqlPort} (DB: {mysqlDb})");
        return $"Server={mysqlHost};Port={mysqlPort};Database={mysqlDb};User={mysqlUser};Password={mysqlPass};CharSet=utf8mb4;";
    }

    // 2. Check for MYSQL_URL or DATABASE_URL (URI format: mysql://user:pass@host:port/db)
    var mysqlUrl = Environment.GetEnvironmentVariable("MYSQL_URL") ?? Environment.GetEnvironmentVariable("DATABASE_URL");
    if (!string.IsNullOrEmpty(mysqlUrl) && mysqlUrl.StartsWith("mysql://", StringComparison.OrdinalIgnoreCase))
    {
        try
        {
            var uri = new Uri(mysqlUrl);
            var userInfo = uri.UserInfo.Split(':');
            var user = userInfo[0];
            var pass = userInfo.Length > 1 ? userInfo[1] : "";
            var db = uri.AbsolutePath.TrimStart('/');
            var p = uri.Port > 0 ? uri.Port : 3306;
            Console.WriteLine($"[Config] Detected Railway MYSQL_URL: {uri.Host}:{p}");
            return $"Server={uri.Host};Port={p};Database={db};User={user};Password={pass};CharSet=utf8mb4;";
        }
        catch (Exception ex)
        {
            Console.WriteLine($"[Config] Notice: Error parsing MYSQL_URL ({ex.Message}). Falling back to DefaultConnection.");
        }
    }

    // 3. Fallback to appsettings.json
    return config.GetConnectionString("DefaultConnection") 
        ?? "Server=localhost;Port=3306;Database=unichrist_db;User=root;Password=root;CharSet=utf8mb4;";
}


