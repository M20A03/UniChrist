using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using UniChristBackend.Data;
using UniChristBackend.Models;

namespace UniChristBackend.Controllers.Api
{
    [ApiController]
    [Route("api/[controller]")]
    public class CafeteriaApiController : ControllerBase
    {
        private readonly UniChristDbContext _context;

        public CafeteriaApiController(UniChristDbContext context)
        {
            _context = context;
        }

        [HttpGet("menu")]
        public async Task<IActionResult> GetMenu()
        {
            var vendors = await _context.CafeteriaVendors
                .Include(v => v.Block)
                .Include(v => v.Items)
                .Where(v => v.IsOpen)
                .ToListAsync();

            return Ok(vendors);
        }

        [HttpPost("order")]
        public async Task<IActionResult> CreateOrder([FromBody] CreateOrderRequestDto request)
        {
            if (request.Items == null || !request.Items.Any())
            {
                return BadRequest(new { message = "Cart is empty. Please select at least one item." });
            }

            var itemIds = request.Items.Select(i => i.ItemId).ToList();
            var dbItems = await _context.CafeteriaItems
                .Where(i => itemIds.Contains(i.ItemId))
                .ToDictionaryAsync(i => i.ItemId);

            decimal grandTotal = 0;
            var orderItems = new List<CafeteriaOrderItem>();

            foreach (var itemReq in request.Items)
            {
                if (!dbItems.TryGetValue(itemReq.ItemId, out var item))
                {
                    return BadRequest(new { message = $"Item with ID {itemReq.ItemId} does not exist." });
                }

                if (item.CurrentStockQty < itemReq.Quantity)
                {
                    return BadRequest(new { message = $"Insufficient stock for {item.ItemName}. Available: {item.CurrentStockQty}" });
                }

                // Decrement stock
                item.CurrentStockQty -= itemReq.Quantity;

                var subtotal = item.Price * itemReq.Quantity;
                grandTotal += subtotal;

                orderItems.Add(new CafeteriaOrderItem
                {
                    ItemId = item.ItemId,
                    Quantity = itemReq.Quantity,
                    UnitPrice = item.Price,
                    Subtotal = subtotal
                });
            }

            // Generate Token Number (101 - 999 cycling daily)
            var todayOrdersCount = await _context.CafeteriaOrders
                .CountAsync(o => o.OrderTimestamp.Date == DateTime.UtcNow.Date);
            var tokenNumber = 100 + (todayOrdersCount % 900) + 1;

            var newOrder = new CafeteriaOrder
            {
                UserId = request.UserId > 0 ? request.UserId : 1, // default to active student if not specified
                VendorId = request.VendorId,
                OrderTimestamp = DateTime.UtcNow,
                TokenNumber = tokenNumber,
                TotalAmount = grandTotal,
                PaymentMode = request.PaymentMode,
                OrderStatus = "PLACED",
                OrderItems = orderItems
            };

            _context.CafeteriaOrders.Add(newOrder);
            await _context.SaveChangesAsync();

            var vendor = await _context.CafeteriaVendors.FindAsync(request.VendorId);

            return Ok(new OrderResponseDto
            {
                OrderId = newOrder.OrderId,
                TokenNumber = newOrder.TokenNumber,
                TotalAmount = newOrder.TotalAmount,
                Status = newOrder.OrderStatus,
                OrderTime = newOrder.OrderTimestamp,
                VendorName = vendor?.VendorName ?? "Campus Cafeteria",
                ItemSummaries = orderItems.Select(oi => $"{dbItems[oi.ItemId].ItemName} x {oi.Quantity} (₹{oi.Subtotal})").ToList()
            });
        }

        [HttpGet("orders/{userId}")]
        public async Task<IActionResult> GetUserOrders(int userId)
        {
            var orders = await _context.CafeteriaOrders
                .Include(o => o.Vendor)
                .Include(o => o.OrderItems)
                    .ThenInclude(oi => oi.Item)
                .Where(o => o.UserId == userId)
                .OrderByDescending(o => o.OrderTimestamp)
                .Take(10)
                .ToListAsync();

            return Ok(orders);
        }
    }
}

