using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using UniChristBackend.Data;
using UniChristBackend.Models;

namespace UniChristBackend.Controllers.Api
{
    [ApiController]
    [Route("api/[controller]")]
    public class FacultyApiController : ControllerBase
    {
        private readonly UniChristDbContext _context;

        public FacultyApiController(UniChristDbContext context)
        {
            _context = context;
        }

        /// <summary>
        /// Retrieves the live schedule-based location for all faculty members.
        /// Can accept optional day and time query parameters for testing/simulation.
        /// </summary>
        [HttpGet("live-status")]
        public async Task<ActionResult<IEnumerable<FacultyLiveLocationDto>>> GetLiveFacultyStatus(
            [FromQuery] string? day = null,
            [FromQuery] string? time = null)
        {
            var now = DateTime.Now;
            var currentDay = string.IsNullOrWhiteSpace(day) 
                ? now.DayOfWeek.ToString().ToUpperInvariant() 
                : day.ToUpperInvariant();

            TimeSpan currentTime;
            if (string.IsNullOrWhiteSpace(time) || !TimeSpan.TryParse(time, out currentTime))
            {
                currentTime = now.TimeOfDay;
            }

            var faculties = await _context.Faculties
                .Include(f => f.User)
                .Include(f => f.Department)
                .Include(f => f.CabinRoom)
                    .ThenInclude(r => r!.Block)
                .Include(f => f.Timetables)
                    .ThenInclude(t => t.Room)
                        .ThenInclude(r => r!.Block)
                .ToListAsync();

            var overrides = await _context.FacultyStatusOverrides
                .Include(o => o.AssignedRoom)
                    .ThenInclude(r => r!.Block)
                .Where(o => o.OverrideDate == DateTime.Today && o.StartTime <= currentTime && o.EndTime >= currentTime)
                .ToListAsync();

            var results = new List<FacultyLiveLocationDto>();

            foreach (var faculty in faculties)
            {
                var facultyName = faculty.User?.FullName ?? "Unknown Faculty";
                var deptName = faculty.Department?.DeptName ?? "Computer Science";
                var cabinDesc = faculty.CabinRoom != null
                    ? $"{faculty.CabinRoom.RoomNumber} ({faculty.CabinRoom.Block?.BlockCode ?? "Block A"})"
                    : "Staff Room 304 (Block A)";

                // 1. Check for manual override (Meeting, Leave, Duty)
                var activeOverride = overrides.FirstOrDefault(o => o.FacultyId == faculty.FacultyId);
                if (activeOverride != null)
                {
                    results.Add(new FacultyLiveLocationDto
                    {
                        FacultyId = faculty.FacultyId,
                        FacultyName = facultyName,
                        Designation = faculty.Designation,
                        DepartmentName = deptName,
                        StatusBadge = activeOverride.StatusType,
                        CurrentLocationDescription = activeOverride.AssignedRoom != null 
                            ? $"{activeOverride.AssignedRoom.RoomNumber} ({activeOverride.AssignedRoom.Block?.BlockCode ?? "Campus"})" 
                            : activeOverride.Notes ?? "Active Duty / Conference",
                        CabinRoomNumber = cabinDesc,
                        ConsultationHours = faculty.ConsultationHours,
                        LastUpdatedMessage = $"Special Override: {activeOverride.Notes ?? activeOverride.StatusType}"
                    });
                    continue;
                }

                // 2. Check Timetable for Current Day & Time
                var activeLecture = faculty.Timetables.FirstOrDefault(t =>
                    t.DayOfWeek.Equals(currentDay, StringComparison.OrdinalIgnoreCase) &&
                    t.StartTime <= currentTime &&
                    t.EndTime >= currentTime);

                if (activeLecture != null)
                {
                    var roomDesc = activeLecture.Room != null
                        ? $"{activeLecture.Room.RoomNumber} ({activeLecture.Room.Block?.BlockCode ?? "Academic Block"})"
                        : "Assigned Lecture Room";

                    results.Add(new FacultyLiveLocationDto
                    {
                        FacultyId = faculty.FacultyId,
                        FacultyName = facultyName,
                        Designation = faculty.Designation,
                        DepartmentName = deptName,
                        StatusBadge = "IN_CLASS",
                        CurrentLocationDescription = roomDesc,
                        ActiveCourse = $"{activeLecture.CourseCode} - {activeLecture.CourseName}",
                        ActiveClassSection = activeLecture.ClassSection,
                        CabinRoomNumber = cabinDesc,
                        ConsultationHours = faculty.ConsultationHours,
                        LastUpdatedMessage = $"Conducting Class ({activeLecture.ClassSection}) until {activeLecture.EndTime:hh\\:mm}"
                    });
                }
                else
                {
                    // 3. Teacher is Free / Consultation Hour -> In Cabin
                    results.Add(new FacultyLiveLocationDto
                    {
                        FacultyId = faculty.FacultyId,
                        FacultyName = facultyName,
                        Designation = faculty.Designation,
                        DepartmentName = deptName,
                        StatusBadge = "AVAILABLE",
                        CurrentLocationDescription = cabinDesc,
                        CabinRoomNumber = cabinDesc,
                        ConsultationHours = faculty.ConsultationHours,
                        LastUpdatedMessage = "Available for Student Consultation in Cabin"
                    });
                }
            }

            return Ok(results);
        }

        /// <summary>
        /// Simulates NFC/Biometric checkpoint scan or temporary meeting override.
        /// </summary>
        [HttpPost("simulate-override")]
        public async Task<IActionResult> SimulateStatusOverride([FromBody] SimulateOverrideDto request)
        {
            var faculty = await _context.Faculties.FindAsync(request.FacultyId);
            if (faculty == null)
            {
                return NotFound(new { message = "Faculty record not found" });
            }

            var startTime = DateTime.Now.TimeOfDay;
            var endTime = startTime.Add(TimeSpan.FromMinutes(request.DurationMinutes));

            var overrideEntry = new FacultyStatusOverride
            {
                FacultyId = request.FacultyId,
                OverrideDate = DateTime.Today,
                StartTime = startTime,
                EndTime = endTime,
                StatusType = request.StatusType,
                AssignedRoomId = request.AssignedRoomId,
                Notes = request.Notes ?? $"Simulated Check-in: {request.StatusType}"
            };

            _context.FacultyStatusOverrides.Add(overrideEntry);
            await _context.SaveChangesAsync();

            return Ok(new
            {
                success = true,
                message = $"Status updated to {request.StatusType} until {endTime:hh\\:mm}",
                overrideId = overrideEntry.OverrideId
            });
        }
    }
}

