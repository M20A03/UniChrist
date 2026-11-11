namespace UniChristBackend.Models
{
    // ==========================================
    // AUTHENTICATION DTOs
    // ==========================================
    public class LoginRequestDto
    {
        public string RegisterNumberOrEmail { get; set; } = string.Empty;
        public string Password { get; set; } = string.Empty;
    }

    public class LoginResponseDto
    {
        public int UserId { get; set; }
        public string RegisterNumber { get; set; } = string.Empty;
        public string FullName { get; set; } = string.Empty;
        public string Email { get; set; } = string.Empty;
        public string Role { get; set; } = string.Empty;
        public string? Department { get; set; }
        public string Token { get; set; } = string.Empty;
    }

    // ==========================================
    // FACULTY LOCATION & PRESENCE DTOs
    // ==========================================
    public class FacultyLiveLocationDto
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

    public class SimulateOverrideDto
    {
        public int FacultyId { get; set; }
        public string StatusType { get; set; } = "IN_MEETING"; // IN_MEETING, ON_LEAVE, EXAM_DUTY, SPECIAL_DUTY
        public int? AssignedRoomId { get; set; }
        public string? Notes { get; set; }
        public int DurationMinutes { get; set; } = 60;
    }

    // ==========================================
    // CAFETERIA DTOs
    // ==========================================
    public class CreateOrderItemDto
    {
        public int ItemId { get; set; }
        public int Quantity { get; set; }
    }

    public class CreateOrderRequestDto
    {
        public int UserId { get; set; }
        public int VendorId { get; set; }
        public string PaymentMode { get; set; } = "CAMPUS_DIGITAL_WALLET";
        public List<CreateOrderItemDto> Items { get; set; } = new();
    }

    public class OrderResponseDto
    {
        public int OrderId { get; set; }
        public int TokenNumber { get; set; }
        public decimal TotalAmount { get; set; }
        public string Status { get; set; } = string.Empty;
        public DateTime OrderTime { get; set; }
        public string VendorName { get; set; } = string.Empty;
        public List<string> ItemSummaries { get; set; } = new();
    }

    // ==========================================
    // GRIEVANCE DTOs
    // ==========================================
    public class CreateGrievanceDto
    {
        public int StudentId { get; set; }
        public string Category { get; set; } = "CAMPUS_WIFI";
        public int? RoomId { get; set; }
        public string TicketSubject { get; set; } = string.Empty;
        public string Description { get; set; } = string.Empty;
        public string Priority { get; set; } = "MEDIUM";
    }

    public class UpdateGrievanceStatusDto
    {
        public string NewStatus { get; set; } = "IN_PROGRESS"; // ASSIGNED, IN_PROGRESS, RESOLVED, CLOSED, REJECTED
        public int ChangedByUserId { get; set; }
        public string? ActionComment { get; set; }
        public string? ResolutionNotes { get; set; }
    }

    // ==========================================
    // PARKING DTOs
    // ==========================================
    public class ToggleParkingSlotDto
    {
        public int SlotId { get; set; }
        public bool IsOccupied { get; set; }
        public string? VehicleRegNumber { get; set; }
        public int? UserId { get; set; }
    }
}

