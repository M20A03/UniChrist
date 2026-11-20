namespace UniChrist.Mobile.Models;

public class CafeteriaVendorDto
{
    public int VendorId { get; set; }
    public string VendorName { get; set; } = string.Empty;
    public string CuisineType { get; set; } = string.Empty;
    public string ContactPhone { get; set; } = string.Empty;
    public bool IsOpen { get; set; }
    public List<CafeteriaItemDto> Items { get; set; } = new();
}

public class CafeteriaItemDto
{
    public int ItemId { get; set; }
    public int VendorId { get; set; }
    public string ItemName { get; set; } = string.Empty;
    public string Category { get; set; } = string.Empty;
    public decimal Price { get; set; }
    public bool IsAvailable { get; set; }
    public int StockQuantity { get; set; }
    public int PreparationTimeMinutes { get; set; }
}

public class CreateOrderItemDto
{
    public int ItemId { get; set; }
    public int Quantity { get; set; }
}

public class OrderRequest
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
