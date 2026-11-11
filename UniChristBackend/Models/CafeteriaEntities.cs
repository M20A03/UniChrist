using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Text.Json.Serialization;

namespace UniChristBackend.Models
{
    [Table("cafeteria_vendors")]
    public class CafeteriaVendor
    {
        [Key]
        [Column("vendor_id")]
        public int VendorId { get; set; }

        [Required]
        [MaxLength(100)]
        [Column("vendor_name")]
        public string VendorName { get; set; } = string.Empty;

        [Column("block_id")]
        public int BlockId { get; set; }

        [ForeignKey("BlockId")]
        public CampusBlock? Block { get; set; }

        [MaxLength(20)]
        [Column("contact_phone")]
        public string? ContactPhone { get; set; }

        [Column("is_open")]
        public bool IsOpen { get; set; } = true;

        [JsonIgnore]
        public ICollection<CafeteriaItem> Items { get; set; } = new List<CafeteriaItem>();
    }

    [Table("cafeteria_items")]
    public class CafeteriaItem
    {
        [Key]
        [Column("item_id")]
        public int ItemId { get; set; }

        [Column("vendor_id")]
        public int VendorId { get; set; }

        [ForeignKey("VendorId")]
        public CafeteriaVendor? Vendor { get; set; }

        [Required]
        [MaxLength(100)]
        [Column("item_name")]
        public string ItemName { get; set; } = string.Empty;

        [Required]
        [MaxLength(50)]
        [Column("category")]
        public string Category { get; set; } = "SNACKS"; // BREAKFAST, BEVERAGES, LUNCH, SNACKS, DESSERT

        [Column("price", TypeName = "decimal(8,2)")]
        public decimal Price { get; set; }

        [Column("is_available")]
        public bool IsAvailable { get; set; } = true;

        [Column("current_stock_qty")]
        public int CurrentStockQty { get; set; } = 50;
    }

    [Table("cafeteria_orders")]
    public class CafeteriaOrder
    {
        [Key]
        [Column("order_id")]
        public int OrderId { get; set; }

        [Column("user_id")]
        public int UserId { get; set; }

        [ForeignKey("UserId")]
        public User? User { get; set; }

        [Column("vendor_id")]
        public int VendorId { get; set; }

        [ForeignKey("VendorId")]
        public CafeteriaVendor? Vendor { get; set; }

        [Column("order_timestamp")]
        public DateTime OrderTimestamp { get; set; } = DateTime.UtcNow;

        [Column("token_number")]
        public int TokenNumber { get; set; }

        [Column("total_amount", TypeName = "decimal(9,2)")]
        public decimal TotalAmount { get; set; }

        [MaxLength(30)]
        [Column("payment_mode")]
        public string PaymentMode { get; set; } = "CAMPUS_DIGITAL_WALLET";

        [MaxLength(30)]
        [Column("order_status")]
        public string OrderStatus { get; set; } = "PLACED"; // PLACED, PREPARING, READY_FOR_PICKUP, COMPLETED, CANCELLED

        [Column("pickup_ready_time")]
        public DateTime? PickupReadyTime { get; set; }

        public ICollection<CafeteriaOrderItem> OrderItems { get; set; } = new List<CafeteriaOrderItem>();
    }

    [Table("cafeteria_order_items")]
    public class CafeteriaOrderItem
    {
        [Key]
        [Column("order_item_id")]
        public int OrderItemId { get; set; }

        [Column("order_id")]
        public int OrderId { get; set; }

        [JsonIgnore]
        [ForeignKey("OrderId")]
        public CafeteriaOrder? Order { get; set; }

        [Column("item_id")]
        public int ItemId { get; set; }

        [ForeignKey("ItemId")]
        public CafeteriaItem? Item { get; set; }

        [Column("quantity")]
        public int Quantity { get; set; }

        [Column("unit_price", TypeName = "decimal(8,2)")]
        public decimal UnitPrice { get; set; }

        [Column("subtotal", TypeName = "decimal(9,2)")]
        public decimal Subtotal { get; set; }
    }
}

