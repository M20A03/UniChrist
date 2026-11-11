using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using UniChristBackend.Data;
using UniChristBackend.Models;

namespace UniChristBackend.Controllers.Api
{
    [ApiController]
    [Route("api/[controller]")]
    public class GrievanceApiController : ControllerBase
    {
        private readonly UniChristDbContext _context;

        public GrievanceApiController(UniChristDbContext context)
        {
            _context = context;
        }

        [HttpGet]
        public async Task<IActionResult> GetGrievances([FromQuery] string? status = null, [FromQuery] int? studentId = null)
        {
            var query = _context.Grievances
                .Include(g => g.Student)
                .Include(g => g.Room)
                    .ThenInclude(r => r!.Block)
                .Include(g => g.AssignedStaff)
                .Include(g => g.AuditLogs)
                .AsQueryable();

            if (!string.IsNullOrWhiteSpace(status))
            {
                query = query.Where(g => g.Status == status);
            }

            if (studentId.HasValue && studentId.Value > 0)
            {
                query = query.Where(g => g.StudentId == studentId.Value);
            }

            var list = await query.OrderByDescending(g => g.CreatedAt).ToListAsync();
            return Ok(list);
        }

        [HttpPost]
        public async Task<IActionResult> CreateGrievance([FromBody] CreateGrievanceDto request)
        {
            if (string.IsNullOrWhiteSpace(request.TicketSubject) || string.IsNullOrWhiteSpace(request.Description))
            {
                return BadRequest(new { message = "Subject and description are required." });
            }

            var grievance = new Grievance
            {
                StudentId = request.StudentId > 0 ? request.StudentId : 1, // Default Mayank Raj Gupta
                Category = request.Category,
                RoomId = request.RoomId,
                TicketSubject = request.TicketSubject,
                Description = request.Description,
                Priority = request.Priority,
                Status = "PENDING",
                CreatedAt = DateTime.UtcNow
            };

            _context.Grievances.Add(grievance);
            await _context.SaveChangesAsync();

            // Initial audit log
            var auditLog = new GrievanceAuditLog
            {
                TicketId = grievance.TicketId,
                ChangedByUserId = grievance.StudentId,
                PreviousStatus = null,
                NewStatus = "PENDING",
                ActionTimestamp = DateTime.UtcNow,
                ActionComment = "Ticket submitted by student."
            };
            _context.GrievanceAuditLogs.Add(auditLog);
            await _context.SaveChangesAsync();

            return Ok(new
            {
                success = true,
                ticketId = grievance.TicketId,
                message = "Grievance ticket registered successfully."
            });
        }

        [HttpPost("{ticketId}/update-status")]
        public async Task<IActionResult> UpdateStatus(int ticketId, [FromBody] UpdateGrievanceStatusDto request)
        {
            var grievance = await _context.Grievances.FindAsync(ticketId);
            if (grievance == null)
            {
                return NotFound(new { message = "Grievance ticket not found." });
            }

            var prev = grievance.Status;
            grievance.Status = request.NewStatus;

            if (request.NewStatus == "RESOLVED" || request.NewStatus == "CLOSED")
            {
                grievance.ResolvedAt = DateTime.UtcNow;
                if (!string.IsNullOrWhiteSpace(request.ResolutionNotes))
                {
                    grievance.ResolutionNotes = request.ResolutionNotes;
                }
            }

            var log = new GrievanceAuditLog
            {
                TicketId = grievance.TicketId,
                ChangedByUserId = request.ChangedByUserId > 0 ? request.ChangedByUserId : 3, // Staff/Faculty
                PreviousStatus = prev,
                NewStatus = request.NewStatus,
                ActionTimestamp = DateTime.UtcNow,
                ActionComment = request.ActionComment ?? $"Status updated to {request.NewStatus}"
            };

            _context.GrievanceAuditLogs.Add(log);
            await _context.SaveChangesAsync();

            return Ok(new
            {
                success = true,
                message = $"Ticket #{ticketId} status transitioned from {prev} to {request.NewStatus}"
            });
        }
    }
}

