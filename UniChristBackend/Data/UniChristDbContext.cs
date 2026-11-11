using Microsoft.EntityFrameworkCore;
using UniChristBackend.Models;

namespace UniChristBackend.Data
{
    public class UniChristDbContext : DbContext
    {
        public UniChristDbContext(DbContextOptions<UniChristDbContext> options) : base(options)
        {
        }

        public DbSet<Role> Roles => Set<Role>();
        public DbSet<User> Users => Set<User>();
        public DbSet<School> Schools => Set<School>();
        public DbSet<Department> Departments => Set<Department>();
        public DbSet<CampusBlock> CampusBlocks => Set<CampusBlock>();
        public DbSet<CampusRoom> CampusRooms => Set<CampusRoom>();
        public DbSet<Student> Students => Set<Student>();
        public DbSet<Faculty> Faculties => Set<Faculty>();
        public DbSet<FacultyTimetable> FacultyTimetables => Set<FacultyTimetable>();
        public DbSet<FacultyStatusOverride> FacultyStatusOverrides => Set<FacultyStatusOverride>();
        public DbSet<CafeteriaVendor> CafeteriaVendors => Set<CafeteriaVendor>();
        public DbSet<CafeteriaItem> CafeteriaItems => Set<CafeteriaItem>();
        public DbSet<CafeteriaOrder> CafeteriaOrders => Set<CafeteriaOrder>();
        public DbSet<CafeteriaOrderItem> CafeteriaOrderItems => Set<CafeteriaOrderItem>();
        public DbSet<ParkingSlot> ParkingSlots => Set<ParkingSlot>();
        public DbSet<ParkingLog> ParkingLogs => Set<ParkingLog>();
        public DbSet<Grievance> Grievances => Set<Grievance>();
        public DbSet<GrievanceAuditLog> GrievanceAuditLogs => Set<GrievanceAuditLog>();
        public DbSet<BookCategory> BookCategories => Set<BookCategory>();
        public DbSet<LibraryBook> LibraryBooks => Set<LibraryBook>();

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // Users & Roles
            modelBuilder.Entity<Role>(entity =>
            {
                entity.HasIndex(e => e.RoleName).IsUnique();
            });

            modelBuilder.Entity<User>(entity =>
            {
                entity.HasIndex(e => e.RegisterNumber).IsUnique();
                entity.HasIndex(e => e.Email).IsUnique();
            });

            // Student 1-to-1 User
            modelBuilder.Entity<Student>()
                .HasOne(s => s.User)
                .WithOne(u => u.StudentProfile)
                .HasForeignKey<Student>(s => s.StudentId)
                .OnDelete(DeleteBehavior.Cascade);

            // Faculty 1-to-1 User
            modelBuilder.Entity<Faculty>()
                .HasOne(f => f.User)
                .WithOne(u => u.FacultyProfile)
                .HasForeignKey<Faculty>(f => f.FacultyId)
                .OnDelete(DeleteBehavior.Cascade);

            // Room Unique constraint block + room_number
            modelBuilder.Entity<CampusRoom>()
                .HasIndex(r => new { r.BlockId, r.RoomNumber })
                .IsUnique();

            // ParkingSlot slot_code unique
            modelBuilder.Entity<ParkingSlot>()
                .HasIndex(p => p.SlotCode)
                .IsUnique();
        }
    }
}

