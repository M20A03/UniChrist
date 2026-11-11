using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Text.Json.Serialization;

namespace UniChristBackend.Models
{
    // ==========================================
    // PARKING
    // ==========================================
    [Table("parking_slots")]
    public class ParkingSlot
    {
        [Key]
        [Column("slot_id")]
        public int SlotId { get; set; }

        [Column("block_id")]
        public int BlockId { get; set; }

        [ForeignKey("BlockId")]
        public CampusBlock? Block { get; set; }

        [Required]
        [MaxLength(20)]
        [Column("slot_code")]
        public string SlotCode { get; set; } = string.Empty;

        [Required]
        [MaxLength(20)]
        [Column("vehicle_type")]
        public string VehicleType { get; set; } = "FOUR_WHEELER"; // TWO_WHEELER, FOUR_WHEELER

        [Column("is_ev_charging")]
        public bool IsEvCharging { get; set; } = false;

        [Column("is_occupied")]
        public bool IsOccupied { get; set; } = false;

        [MaxLength(30)]
        [Column("assigned_vehicle_reg")]
        public string? AssignedVehicleReg { get; set; }
    }

    [Table("parking_logs")]
    public class ParkingLog
    {
        [Key]
        [Column("log_id")]
        public long LogId { get; set; }

        [Column("slot_id")]
        public int SlotId { get; set; }

        [ForeignKey("SlotId")]
        public ParkingSlot? Slot { get; set; }

        [Column("user_id")]
        public int? UserId { get; set; }

        [ForeignKey("UserId")]
        public User? User { get; set; }

        [Required]
        [MaxLength(30)]
        [Column("vehicle_reg_number")]
        public string VehicleRegNumber { get; set; } = string.Empty;

        [Column("entry_timestamp")]
        public DateTime EntryTimestamp { get; set; } = DateTime.UtcNow;

        [Column("exit_timestamp")]
        public DateTime? ExitTimestamp { get; set; }
    }

    // ==========================================
    // GRIEVANCE
    // ==========================================
    [Table("grievances")]
    public class Grievance
    {
        [Key]
        [Column("ticket_id")]
        public int TicketId { get; set; }

        [Column("student_id")]
        public int StudentId { get; set; }

        [ForeignKey("StudentId")]
        public User? Student { get; set; }

        [Required]
        [MaxLength(50)]
        [Column("category")]
        public string Category { get; set; } = "CAMPUS_WIFI"; // CAMPUS_WIFI, CLASSROOM_INFRASTRUCTURE, LAB_EQUIPMENT, CANTEEN_HYGIENE, WASHROOM_MAINTENANCE, ACADEMIC_ADMINISTRATION

        [Column("room_id")]
        public int? RoomId { get; set; }

        [ForeignKey("RoomId")]
        public CampusRoom? Room { get; set; }

        [Required]
        [MaxLength(150)]
        [Column("ticket_subject")]
        public string TicketSubject { get; set; } = string.Empty;

        [Required]
        [Column("description")]
        public string Description { get; set; } = string.Empty;

        [MaxLength(20)]
        [Column("priority")]
        public string Priority { get; set; } = "MEDIUM"; // LOW, MEDIUM, HIGH, URGENT

        [MaxLength(30)]
        [Column("status")]
        public string Status { get; set; } = "PENDING"; // PENDING, ASSIGNED, IN_PROGRESS, RESOLVED, CLOSED, REJECTED

        [Column("assigned_to_staff_id")]
        public int? AssignedToStaffId { get; set; }

        [ForeignKey("AssignedToStaffId")]
        public User? AssignedStaff { get; set; }

        [Column("created_at")]
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

        [Column("resolved_at")]
        public DateTime? ResolvedAt { get; set; }

        [Column("resolution_notes")]
        public string? ResolutionNotes { get; set; }

        public ICollection<GrievanceAuditLog> AuditLogs { get; set; } = new List<GrievanceAuditLog>();
    }

    [Table("grievance_audit_logs")]
    public class GrievanceAuditLog
    {
        [Key]
        [Column("log_id")]
        public long LogId { get; set; }

        [Column("ticket_id")]
        public int TicketId { get; set; }

        [JsonIgnore]
        [ForeignKey("TicketId")]
        public Grievance? Grievance { get; set; }

        [Column("changed_by_user_id")]
        public int ChangedByUserId { get; set; }

        [ForeignKey("ChangedByUserId")]
        public User? ChangedByUser { get; set; }

        [MaxLength(30)]
        [Column("previous_status")]
        public string? PreviousStatus { get; set; }

        [Required]
        [MaxLength(30)]
        [Column("new_status")]
        public string NewStatus { get; set; } = string.Empty;

        [Column("action_timestamp")]
        public DateTime ActionTimestamp { get; set; } = DateTime.UtcNow;

        [Column("action_comment")]
        public string? ActionComment { get; set; }
    }

    // ==========================================
    // LIBRARY
    // ==========================================
    [Table("book_categories")]
    public class BookCategory
    {
        [Key]
        [Column("category_id")]
        public int CategoryId { get; set; }

        [Required]
        [MaxLength(100)]
        [Column("category_name")]
        public string CategoryName { get; set; } = string.Empty;
    }

    [Table("library_books")]
    public class LibraryBook
    {
        [Key]
        [Column("book_id")]
        public int BookId { get; set; }

        [Required]
        [MaxLength(20)]
        [Column("isbn")]
        public string Isbn { get; set; } = string.Empty;

        [Required]
        [MaxLength(200)]
        [Column("title")]
        public string Title { get; set; } = string.Empty;

        [Required]
        [MaxLength(150)]
        [Column("author")]
        public string Author { get; set; } = string.Empty;

        [MaxLength(120)]
        [Column("publisher")]
        public string? Publisher { get; set; }

        [MaxLength(30)]
        [Column("edition")]
        public string? Edition { get; set; }

        [Column("category_id")]
        public int CategoryId { get; set; }

        [ForeignKey("CategoryId")]
        public BookCategory? Category { get; set; }

        [Column("total_copies")]
        public int TotalCopies { get; set; } = 1;

        [Column("available_copies")]
        public int AvailableCopies { get; set; } = 1;

        [MaxLength(50)]
        [Column("shelf_location")]
        public string? ShelfLocation { get; set; }
    }
}

