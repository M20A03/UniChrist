using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using UniChristBackend.Data;
using UniChristBackend.Models;

namespace UniChristBackend.Controllers.Api
{
    [ApiController]
    [Route("api/[controller]")]
    public class AuthApiController : ControllerBase
    {
        private readonly UniChristDbContext _context;

        public AuthApiController(UniChristDbContext context)
        {
            _context = context;
        }

        [HttpPost("login")]
        public async Task<IActionResult> Login([FromBody] LoginRequestDto request)
        {
            var user = await _context.Users
                .Include(u => u.Role)
                .Include(u => u.StudentProfile)
                    .ThenInclude(s => s!.Department)
                .Include(u => u.FacultyProfile)
                    .ThenInclude(f => f!.Department)
                .FirstOrDefaultAsync(u =>
                    (u.RegisterNumber == request.RegisterNumberOrEmail || u.Email == request.RegisterNumberOrEmail)
                    && u.IsActive);

            if (user == null || user.PasswordHash != request.Password)
            {
                return Unauthorized(new { message = "Invalid register number/email or password." });
            }

            var department = user.StudentProfile?.Department?.DeptName ?? user.FacultyProfile?.Department?.DeptName;

            return Ok(new LoginResponseDto
            {
                UserId = user.UserId,
                RegisterNumber = user.RegisterNumber,
                FullName = user.FullName,
                Email = user.Email,
                Role = user.Role?.RoleName ?? "STUDENT",
                Department = department,
                Token = $"mock-jwt-token-{user.UserId}-{Guid.NewGuid():N}"
            });
        }

        [HttpGet("demo-users")]
        public async Task<IActionResult> GetDemoUsers()
        {
            var users = await _context.Users
                .Include(u => u.Role)
                .Select(u => new
                {
                    u.UserId,
                    u.FullName,
                    u.RegisterNumber,
                    u.Email,
                    Role = u.Role != null ? u.Role.RoleName : "STUDENT",
                    DemoPassword = "Password@123"
                })
                .ToListAsync();

            return Ok(users);
        }
    }
}

