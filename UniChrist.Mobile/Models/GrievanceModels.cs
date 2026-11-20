namespace UniChrist.Mobile.Models;

public class GrievanceDto
{
    public int TicketId { get; set; }
    public string TicketSubject { get; set; } = string.Empty;
    public string Category { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public string Priority { get; set; } = "MEDIUM";
    public string Status { get; set; } = "SUBMITTED";
    public DateTime CreatedAt { get; set; }
    public string? ResolutionNotes { get; set; }
}

public class CreateGrievanceRequest
{
    public int StudentId { get; set; }
    public string Category { get; set; } = "CAMPUS_WIFI";
    public int? RoomId { get; set; }
    public string TicketSubject { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public string Priority { get; set; } = "MEDIUM";
}
