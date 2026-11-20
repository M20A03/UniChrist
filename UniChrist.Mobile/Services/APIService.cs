using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Text.Json;
using UniChrist.Mobile.Models;

namespace UniChrist.Mobile.Services;

public class APIService : IAPIService
{
    private readonly HttpClient _http;
    private readonly JsonSerializerOptions _jsonOptions = new()
    {
        PropertyNameCaseInsensitive = true
    };

    private LoginResponse? _currentUser;
    public LoginResponse? CurrentUser => _currentUser;

    public APIService(HttpClient http)
    {
        _http = http;
    }

    public async Task<LoginResponse?> LoginAsync(LoginRequest request)
    {
        try
        {
            var response = await _http.PostAsJsonAsync("/api/AuthApi/login", request);
            if (response.IsSuccessStatusCode)
            {
                var loginRes = await response.Content.ReadFromJsonAsync<LoginResponse>(_jsonOptions);
                if (loginRes != null && !string.IsNullOrEmpty(loginRes.Token))
                {
                    _currentUser = loginRes;
                    _http.DefaultRequestHeaders.Authorization =
                        new AuthenticationHeaderValue("Bearer", loginRes.Token);
                    return loginRes;
                }
            }
        }
        catch (Exception ex)
        {
            System.Diagnostics.Debug.WriteLine($"[APIService.LoginAsync] Error: {ex.Message}");
        }
        return null;
    }

    public void Logout()
    {
        _currentUser = null;
        _http.DefaultRequestHeaders.Authorization = null;
    }

    public async Task<List<FacultyLocationDto>> GetLiveFacultyStatusAsync(string? day = null, string? time = null)
    {
        try
        {
            var url = "/api/FacultyApi/live-status";
            var queryParams = new List<string>();
            if (!string.IsNullOrWhiteSpace(day)) queryParams.Add($"day={Uri.EscapeDataString(day)}");
            if (!string.IsNullOrWhiteSpace(time)) queryParams.Add($"time={Uri.EscapeDataString(time)}");
            if (queryParams.Any()) url += "?" + string.Join("&", queryParams);

            var res = await _http.GetAsync(url);
            if (res.IsSuccessStatusCode)
            {
                return await res.Content.ReadFromJsonAsync<List<FacultyLocationDto>>(_jsonOptions) ?? new();
            }
        }
        catch (Exception ex)
        {
            System.Diagnostics.Debug.WriteLine($"[APIService.GetLiveFacultyStatus] Error: {ex.Message}");
        }
        return new();
    }

    public async Task<FacultyLocationDto?> GetFacultyLocationByIdAsync(int facultyId)
    {
        var all = await GetLiveFacultyStatusAsync();
        return all.FirstOrDefault(f => f.FacultyId == facultyId);
    }

    public async Task<List<CafeteriaVendorDto>> GetCafeteriaMenuAsync()
    {
        try
        {
            var res = await _http.GetAsync("/api/CafeteriaApi/menu");
            if (res.IsSuccessStatusCode)
            {
                return await res.Content.ReadFromJsonAsync<List<CafeteriaVendorDto>>(_jsonOptions) ?? new();
            }
        }
        catch (Exception ex)
        {
            System.Diagnostics.Debug.WriteLine($"[APIService.GetCafeteriaMenu] Error: {ex.Message}");
        }
        return new();
    }

    public async Task<OrderResponseDto?> PlaceCafeteriaOrderAsync(OrderRequest req)
    {
        try
        {
            var res = await _http.PostAsJsonAsync("/api/CafeteriaApi/order", req);
            if (res.IsSuccessStatusCode)
            {
                return await res.Content.ReadFromJsonAsync<OrderResponseDto>(_jsonOptions);
            }
        }
        catch (Exception ex)
        {
            System.Diagnostics.Debug.WriteLine($"[APIService.PlaceCafeteriaOrder] Error: {ex.Message}");
        }
        return null;
    }

    public async Task<List<GrievanceDto>> GetGrievancesAsync(int studentId)
    {
        try
        {
            var res = await _http.GetAsync($"/api/GrievanceApi/student/{studentId}");
            if (res.IsSuccessStatusCode)
            {
                return await res.Content.ReadFromJsonAsync<List<GrievanceDto>>(_jsonOptions) ?? new();
            }
        }
        catch (Exception ex)
        {
            System.Diagnostics.Debug.WriteLine($"[APIService.GetGrievances] Error: {ex.Message}");
        }
        return new();
    }

    public async Task<bool> SubmitGrievanceAsync(CreateGrievanceRequest req)
    {
        try
        {
            var res = await _http.PostAsJsonAsync("/api/GrievanceApi", req);
            return res.IsSuccessStatusCode;
        }
        catch (Exception ex)
        {
            System.Diagnostics.Debug.WriteLine($"[APIService.SubmitGrievance] Error: {ex.Message}");
            return false;
        }
    }

    public async Task<List<BookDto>> SearchBooksAsync(string? query = null)
    {
        try
        {
            var url = "/api/LibraryApi/books";
            if (!string.IsNullOrWhiteSpace(query))
            {
                url += $"?query={Uri.EscapeDataString(query)}";
            }
            var res = await _http.GetAsync(url);
            if (res.IsSuccessStatusCode)
            {
                return await res.Content.ReadFromJsonAsync<List<BookDto>>(_jsonOptions) ?? new();
            }
        }
        catch (Exception ex)
        {
            System.Diagnostics.Debug.WriteLine($"[APIService.SearchBooks] Error: {ex.Message}");
        }
        return new();
    }
}
