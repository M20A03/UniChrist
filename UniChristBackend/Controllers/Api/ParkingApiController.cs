using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using UniChristBackend.Data;
using UniChristBackend.Models;

namespace UniChristBackend.Controllers.Api
{
    [ApiController]
    [Route("api/[controller]")]
    public class ParkingApiController : ControllerBase
    {
        private readonly UniChristDbContext _context;

        public ParkingApiController(UniChristDbContext context)
        {
            _context = context;
        }

        [HttpGet("slots")]
        public async Task<IActionResult> GetSlots()
        {
            var slots = await _context.ParkingSlots
                .Include(s => s.Block)
                .OrderBy(s => s.SlotCode)
                .ToListAsync();

            var total = slots.Count;
            var occupied = slots.Count(s => s.IsOccupied);
            var available = total - occupied;

            return Ok(new
            {
                totalSlots = total,
                occupiedSlots = occupied,
                availableSlots = available,
                slots
            });
        }

        [HttpPost("toggle")]
        public async Task<IActionResult> ToggleSlot([FromBody] ToggleParkingSlotDto request)
        {
            var slot = await _context.ParkingSlots.FindAsync(request.SlotId);
            if (slot == null)
            {
                return NotFound(new { message = "Parking slot not found." });
            }

            slot.IsOccupied = request.IsOccupied;
            slot.AssignedVehicleReg = request.IsOccupied ? request.VehicleRegNumber ?? "KA-04-XX-0000" : null;

            // Add parking log
            if (request.IsOccupied)
            {
                var log = new ParkingLog
                {
                    SlotId = slot.SlotId,
                    UserId = request.UserId,
                    VehicleRegNumber = slot.AssignedVehicleReg ?? "KA-04-XX-0000",
                    EntryTimestamp = DateTime.UtcNow
                };
                _context.ParkingLogs.Add(log);
            }
            else
            {
                var activeLog = await _context.ParkingLogs
                    .Where(l => l.SlotId == slot.SlotId && l.ExitTimestamp == null)
                    .OrderByDescending(l => l.EntryTimestamp)
                    .FirstOrDefaultAsync();

                if (activeLog != null)
                {
                    activeLog.ExitTimestamp = DateTime.UtcNow;
                }
            }

            await _context.SaveChangesAsync();

            return Ok(new
            {
                success = true,
                slotId = slot.SlotId,
                slotCode = slot.SlotCode,
                isOccupied = slot.IsOccupied,
                message = slot.IsOccupied ? $"Slot {slot.SlotCode} marked OCCUPIED" : $"Slot {slot.SlotCode} released to AVAILABLE"
            });
        }
    }
}

