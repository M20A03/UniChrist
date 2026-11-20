namespace UniChrist.Mobile.Models;

public class FacultyLocationDto
{
    public int FacultyId { get; set; }
    public string FacultyName { get; set; } = string.Empty;
    public string Designation { get; set; } = string.Empty;
    public string DepartmentName { get; set; } = string.Empty;
    public string StatusBadge { get; set; } = "AVAILABLE"; // AVAILABLE, IN_CLASS, IN_MEETING, ON_LEAVE
    public string CurrentLocationDescription { get; set; } = string.Empty;
    public string? ActiveCourse { get; set; }
    public string? ActiveClassSection { get; set; }
    public string? CabinRoomNumber { get; set; }
    public string? ConsultationHours { get; set; }
    public string LastUpdatedMessage { get; set; } = "Schedule Live";
}

public class SimulateOverrideRequest
{
    public int FacultyId { get; set; }
    public string StatusType { get; set; } = "IN_MEETING";
    public int? AssignedRoomId { get; set; }
    public string? Notes { get; set; }
    public int DurationMinutes { get; set; } = 60;
}
