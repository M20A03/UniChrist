using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Text.Json.Serialization;

namespace UniChristBackend.Models
{
    [Table("roles")]
    public class Role
    {
        [Key]
        [Column("role_id")]
        public int RoleId { get; set; }

        [Required]
        [MaxLength(50)]
        [Column("role_name")]
        public string RoleName { get; set; } = string.Empty;

        [MaxLength(255)]
        [Column("role_description")]
        public string? RoleDescription { get; set; }

        [JsonIgnore]
        public ICollection<User> Users { get; set; } = new List<User>();
    }

    [Table("users")]
    public class User
    {
        [Key]
        [Column("user_id")]
        public int UserId { get; set; }

        [Column("role_id")]
        public int RoleId { get; set; }

        [ForeignKey("RoleId")]
        public Role? Role { get; set; }

        [Required]
        [MaxLength(50)]
        [Column("register_number")]
        public string RegisterNumber { get; set; } = string.Empty;

        [Required]
        [MaxLength(120)]
        [Column("full_name")]
        public string FullName { get; set; } = string.Empty;

        [Required]
        [MaxLength(120)]
        [EmailAddress]
        [Column("email")]
        public string Email { get; set; } = string.Empty;

        [Required]
        [MaxLength(255)]
        [Column("password_hash")]
        [JsonIgnore]
        public string PasswordHash { get; set; } = string.Empty;

        [MaxLength(20)]
        [Column("phone_number")]
        public string? PhoneNumber { get; set; }

        [Column("is_active")]
        public bool IsActive { get; set; } = true;

        [Column("created_at")]
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

        [JsonIgnore]
        public Student? StudentProfile { get; set; }

        [JsonIgnore]
        public Faculty? FacultyProfile { get; set; }
    }

    [Table("schools")]
    public class School
    {
        [Key]
        [Column("school_id")]
        public int SchoolId { get; set; }

        [Required]
        [MaxLength(100)]
        [Column("school_name")]
        public string SchoolName { get; set; } = string.Empty;

        [MaxLength(120)]
        [Column("school_dean")]
        public string? SchoolDean { get; set; }

        [JsonIgnore]
        public ICollection<Department> Departments { get; set; } = new List<Department>();
    }

    [Table("departments")]
    public class Department
    {
        [Key]
        [Column("dept_id")]
        public int DeptId { get; set; }

        [Column("school_id")]
        public int SchoolId { get; set; }

        [ForeignKey("SchoolId")]
        public School? School { get; set; }

        [Required]
        [MaxLength(100)]
        [Column("dept_name")]
        public string DeptName { get; set; } = string.Empty;

        [MaxLength(120)]
        [Column("hod_name")]
        public string? HodName { get; set; }
    }

    [Table("campus_blocks")]
    public class CampusBlock
    {
        [Key]
        [Column("block_id")]
        public int BlockId { get; set; }

        [Required]
        [MaxLength(20)]
        [Column("block_code")]
        public string BlockCode { get; set; } = string.Empty;

        [Required]
        [MaxLength(100)]
        [Column("block_name")]
        public string BlockName { get; set; } = string.Empty;

        [Column("total_floors")]
        public int TotalFloors { get; set; }

        [Column("latitude", TypeName = "decimal(9,6)")]
        public decimal? Latitude { get; set; }

        [Column("longitude", TypeName = "decimal(9,6)")]
        public decimal? Longitude { get; set; }

        [JsonIgnore]
        public ICollection<CampusRoom> Rooms { get; set; } = new List<CampusRoom>();
    }

    [Table("campus_rooms")]
    public class CampusRoom
    {
        [Key]
        [Column("room_id")]
        public int RoomId { get; set; }

        [Column("block_id")]
        public int BlockId { get; set; }

        [ForeignKey("BlockId")]
        public CampusBlock? Block { get; set; }

        [Required]
        [MaxLength(30)]
        [Column("room_number")]
        public string RoomNumber { get; set; } = string.Empty;

        [Column("floor_number")]
        public int FloorNumber { get; set; }

        [Required]
        [MaxLength(50)]
        [Column("room_type")]
        public string RoomType { get; set; } = "CLASSROOM";

        [Column("seating_capacity")]
        public int SeatingCapacity { get; set; } = 60;

        [Column("is_active")]
        public bool IsActive { get; set; } = true;
    }

    [Table("students")]
    public class Student
    {
        [Key]
        [Column("student_id")]
        public int StudentId { get; set; }

        [ForeignKey("StudentId")]
        public User? User { get; set; }

        [Column("dept_id")]
        public int DeptId { get; set; }

        [ForeignKey("DeptId")]
        public Department? Department { get; set; }

        [MaxLength(20)]
        [Column("class_section")]
        public string ClassSection { get; set; } = "4BCA-B";

        [Column("semester")]
        public int Semester { get; set; } = 4;

        [MaxLength(20)]
        [Column("batch_year")]
        public string BatchYear { get; set; } = "2025-2029";
    }

    [Table("faculties")]
    public class Faculty
    {
        [Key]
        [Column("faculty_id")]
        public int FacultyId { get; set; }

        [ForeignKey("FacultyId")]
        public User? User { get; set; }

        [Column("dept_id")]
        public int DeptId { get; set; }

        [ForeignKey("DeptId")]
        public Department? Department { get; set; }

        [Required]
        [MaxLength(80)]
        [Column("designation")]
        public string Designation { get; set; } = "Assistant Professor";

        [Column("cabin_room_id")]
        public int? CabinRoomId { get; set; }

        [ForeignKey("CabinRoomId")]
        public CampusRoom? CabinRoom { get; set; }

        [MaxLength(20)]
        [Column("office_extension")]
        public string? OfficeExtension { get; set; }

        [MaxLength(100)]
        [Column("consultation_hours")]
        public string? ConsultationHours { get; set; }

        [JsonIgnore]
        public ICollection<FacultyTimetable> Timetables { get; set; } = new List<FacultyTimetable>();
    }
}

