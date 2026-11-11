using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using UniChristBackend.Data;
using UniChristBackend.Models;

namespace UniChristBackend.Controllers.Api
{
    [ApiController]
    [Route("api/[controller]")]
    public class LibraryApiController : ControllerBase
    {
        private readonly UniChristDbContext _context;

        public LibraryApiController(UniChristDbContext context)
        {
            _context = context;
        }

        [HttpGet("books")]
        public async Task<IActionResult> GetBooks([FromQuery] string? query = null)
        {
            var booksQuery = _context.LibraryBooks
                .Include(b => b.Category)
                .AsQueryable();

            if (!string.IsNullOrWhiteSpace(query))
            {
                var q = query.ToLower();
                booksQuery = booksQuery.Where(b =>
                    b.Title.ToLower().Contains(q) ||
                    b.Author.ToLower().Contains(q) ||
                    b.Isbn.Contains(q));
            }

            var books = await booksQuery.ToListAsync();
            return Ok(books);
        }
    }
}

