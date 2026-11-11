using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace UniChristBackend.Models
{
    [Table("faculty_timetables")]
    public class FacultyTimetable
    {
        [Key]
        [Column("schedule_id")]
        public int ScheduleId { get; set; }

        [Column("faculty_id")]
        public int FacultyId { get; set; }

        [ForeignKey("FacultyId")]
        public Faculty? Faculty { get; set; }

        [Required]
        [MaxLength(15)]
        [Column("day_of_week")]
        public string DayOfWeek { get; set; } = "MONDAY"; // MONDAY, TUESDAY, etc.

        [Column("period_number")]
        public int PeriodNumber { get; set; }

        [Column("start_time")]
        public TimeSpan StartTime { get; set; }

        [Column("end_time")]
        public TimeSpan EndTime { get; set; }

        [Column("room_id")]
        public int RoomId { get; set; }

        [ForeignKey("RoomId")]
        public CampusRoom? Room { get; set; }

        [Required]
        [MaxLength(30)]
        [Column("course_code")]
        public string CourseCode { get; set; } = string.Empty;

        [Required]
        [MaxLength(120)]
        [Column("course_name")]
        public string CourseName { get; set; } = string.Empty;

        [Required]
        [MaxLength(20)]
        [Column("class_section")]
        public string ClassSection { get; set; } = string.Empty;
    }

    [Table("faculty_status_overrides")]
    public class FacultyStatusOverride
    {
        [Key]
        [Column("override_id")]
        public int OverrideId { get; set; }

        [Column("faculty_id")]
        public int FacultyId { get; set; }

        [ForeignKey("FacultyId")]
        public Faculty? Faculty { get; set; }

        [Column("override_date")]
        public DateTime OverrideDate { get; set; } = DateTime.Today;

        [Column("start_time")]
        public TimeSpan StartTime { get; set; }

        [Column("end_time")]
        public TimeSpan EndTime { get; set; }

        [Required]
        [MaxLength(50)]
        [Column("status_type")]
        public string StatusType { get; set; } = "IN_MEETING"; // IN_MEETING, ON_LEAVE, EXAM_DUTY, SPECIAL_DUTY

        [Column("assigned_room_id")]
        public int? AssignedRoomId { get; set; }

        [ForeignKey("AssignedRoomId")]
        public CampusRoom? AssignedRoom { get; set; }

        [MaxLength(255)]
        [Column("notes")]
        public string? Notes { get; set; }
    }
}

