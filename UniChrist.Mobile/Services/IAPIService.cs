using UniChrist.Mobile.Models;

namespace UniChrist.Mobile.Services;

public interface IAPIService
{
    // Authentication
    Task<LoginResponse?> LoginAsync(LoginRequest request);
    void Logout();
    LoginResponse? CurrentUser { get; }

    // Faculty Navigation
    Task<List<FacultyLocationDto>> GetLiveFacultyStatusAsync(string? day = null, string? time = null);
    Task<FacultyLocationDto?> GetFacultyLocationByIdAsync(int facultyId);

    // Cafeteria
    Task<List<CafeteriaVendorDto>> GetCafeteriaMenuAsync();
    Task<OrderResponseDto?> PlaceCafeteriaOrderAsync(OrderRequest req);

    // Grievances
    Task<List<GrievanceDto>> GetGrievancesAsync(int studentId);
    Task<bool> SubmitGrievanceAsync(CreateGrievanceRequest req);

    // Library OPAC
    Task<List<BookDto>> SearchBooksAsync(string? query = null);
}
