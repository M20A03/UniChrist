using Microsoft.EntityFrameworkCore;
using UniChristBackend.Models;

namespace UniChristBackend.Data
{
    public static class DbInitializer
    {
        public static void Initialize(UniChristDbContext context)
        {
            // Ensure created or migrated
            try
            {
                context.Database.EnsureCreated();
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[DbInitializer] Note: EnsureCreated check completed with notice: {ex.Message}");
            }

            // Check if already seeded
            if (context.Roles.Any())
            {
                return; // DB already has data
            }

            Console.WriteLine("[DbInitializer] Seeding Initial UniChrist Campus Data...");

            // 1. Roles
            var roleAdmin = new Role { RoleName = "ADMIN", RoleDescription = "System & Campus Administrator" };
            var roleFaculty = new Role { RoleName = "FACULTY", RoleDescription = "Academic Teaching Faculty" };
            var roleStudent = new Role { RoleName = "STUDENT", RoleDescription = "Enrolled Undergraduate / Postgraduate Student" };
            var roleStaff = new Role { RoleName = "STAFF", RoleDescription = "Cafeteria, Security and Maintenance Staff" };

            context.Roles.AddRange(roleAdmin, roleFaculty, roleStudent, roleStaff);
            context.SaveChanges();

            // 2. Schools & Departments
            var schoolScience = new School
            {
                SchoolName = "School of Sciences",
                SchoolDean = "Dr George Thomas"
            };
            context.Schools.Add(schoolScience);
            context.SaveChanges();

            var deptCs = new Department
            {
                SchoolId = schoolScience.SchoolId,
                DeptName = "Department of Computer Science",
                HodName = "Dr Vinay M"
            };
            context.Departments.Add(deptCs);
            context.SaveChanges();

            // 3. Blocks & Rooms
            var blockA = new CampusBlock
            {
                BlockCode = "BLK-A",
                BlockName = "Block A (Main Academic & Administrative Block)",
                TotalFloors = 5,
                Latitude = 13.031200m,
                Longitude = 77.545100m
            };
            var blockB = new CampusBlock
            {
                BlockCode = "BLK-B",
                BlockName = "Block B (Computing Labs & Research Center)",
                TotalFloors = 4,
                Latitude = 13.031800m,
                Longitude = 77.545600m
            };
            context.CampusBlocks.AddRange(blockA, blockB);
            context.SaveChanges();

            var roomStaff304 = new CampusRoom
            {
                BlockId = blockA.BlockId,
                RoomNumber = "Staff Room 304",
                FloorNumber = 3,
                RoomType = "STAFF_ROOM",
                SeatingCapacity = 15
            };
            var roomLab201 = new CampusRoom
            {
                BlockId = blockB.BlockId,
                RoomNumber = "Lab 201 (DBMS Lab)",
                FloorNumber = 2,
                RoomType = "LAB",
                SeatingCapacity = 60
            };
            var roomConf102 = new CampusRoom
            {
                BlockId = blockA.BlockId,
                RoomNumber = "Conference Room 102",
                FloorNumber = 1,
                RoomType = "SEMINAR_HALL",
                SeatingCapacity = 40
            };
            var roomClass405 = new CampusRoom
            {
                BlockId = blockA.BlockId,
                RoomNumber = "Room 405 (Classroom)",
                FloorNumber = 4,
                RoomType = "CLASSROOM",
                SeatingCapacity = 75
            };

            context.CampusRooms.AddRange(roomStaff304, roomLab201, roomConf102, roomClass405);
            context.SaveChanges();

            // 4. Users (Students, Faculty, Staff)
            // Team Lead Student: Mayank Raj Gupta
            var userStudent1 = new User
            {
                RoleId = roleStudent.RoleId,
                RegisterNumber = "2543115",
                FullName = "Mayank Raj Gupta",
                Email = "mayank.raj@christuniversity.in",
                PasswordHash = "Password@123",
                PhoneNumber = "+91 9876543210"
            };
            // Team Member: Sonti Sri Lakshmi Aslesha
            var userStudent2 = new User
            {
                RoleId = roleStudent.RoleId,
                RegisterNumber = "2543140",
                FullName = "Sonti Sri Lakshmi Aslesha",
                Email = "aslesha.sonti@christuniversity.in",
                PasswordHash = "Password@123",
                PhoneNumber = "+91 9876543211"
            };
            // Guide / Faculty: Dr Hemanth K S
            var userFaculty1 = new User
            {
                RoleId = roleFaculty.RoleId,
                RegisterNumber = "EMP-CS-101",
                FullName = "Dr Hemanth K S",
                Email = "hemanth.ks@christuniversity.in",
                PasswordHash = "Password@123",
                PhoneNumber = "+91 9123456780"
            };
            // Faculty: Dr Deepa B G
            var userFaculty2 = new User
            {
                RoleId = roleFaculty.RoleId,
                RegisterNumber = "EMP-CS-102",
                FullName = "Dr Deepa B G",
                Email = "deepa.bg@christuniversity.in",
                PasswordHash = "Password@123",
                PhoneNumber = "+91 9123456781"
            };
            // HOD: Dr Vinay M
            var userFaculty3 = new User
            {
                RoleId = roleFaculty.RoleId,
                RegisterNumber = "EMP-CS-100",
                FullName = "Dr Vinay M",
                Email = "vinay.m@christuniversity.in",
                PasswordHash = "Password@123",
                PhoneNumber = "+91 9123456782"
            };

            context.Users.AddRange(userStudent1, userStudent2, userFaculty1, userFaculty2, userFaculty3);
            context.SaveChanges();

            // 5. Profiles
            var studentMayank = new Student
            {
                StudentId = userStudent1.UserId,
                DeptId = deptCs.DeptId,
                ClassSection = "4BCA-B",
                Semester = 4,
                BatchYear = "2025-2029"
            };
            var studentAslesha = new Student
            {
                StudentId = userStudent2.UserId,
                DeptId = deptCs.DeptId,
                ClassSection = "4BCA-B",
                Semester = 4,
                BatchYear = "2025-2029"
            };
            context.Students.AddRange(studentMayank, studentAslesha);

            var facultyHemanth = new Faculty
            {
                FacultyId = userFaculty1.UserId,
                DeptId = deptCs.DeptId,
                Designation = "Associate Professor & DBMS Project Guide",
                CabinRoomId = roomStaff304.RoomId,
                OfficeExtension = "4102",
                ConsultationHours = "Mon-Thu 03:00 PM - 04:30 PM"
            };
            var facultyDeepa = new Faculty
            {
                FacultyId = userFaculty2.UserId,
                DeptId = deptCs.DeptId,
                Designation = "Associate Professor",
                CabinRoomId = roomStaff304.RoomId,
                OfficeExtension = "4105",
                ConsultationHours = "Wed-Fri 02:00 PM - 03:30 PM"
            };
            var facultyVinay = new Faculty
            {
                FacultyId = userFaculty3.UserId,
                DeptId = deptCs.DeptId,
                Designation = "Head of Department (HOD)",
                CabinRoomId = roomConf102.RoomId,
                OfficeExtension = "4100",
                ConsultationHours = "Mon-Fri 11:00 AM - 01:00 PM"
            };
            context.Faculties.AddRange(facultyHemanth, facultyDeepa, facultyVinay);
            context.SaveChanges();

            // 6. Faculty Timetable
            // Dr Hemanth K S timetable
            var tt1 = new FacultyTimetable
            {
                FacultyId = facultyHemanth.FacultyId,
                DayOfWeek = "MONDAY",
                PeriodNumber = 2,
                StartTime = new TimeSpan(9, 45, 0),
                EndTime = new TimeSpan(10, 45, 0),
                RoomId = roomClass405.RoomId,
                CourseCode = "BCA302",
                CourseName = "Relational Database Management Systems",
                ClassSection = "4BCA-B"
            };
            var tt2 = new FacultyTimetable
            {
                FacultyId = facultyHemanth.FacultyId,
                DayOfWeek = "MONDAY",
                PeriodNumber = 4,
                StartTime = new TimeSpan(11, 45, 0),
                EndTime = new TimeSpan(13, 15, 0),
                RoomId = roomLab201.RoomId,
                CourseCode = "BCA381",
                CourseName = "DBMS Project Lab",
                ClassSection = "4BCA-B"
            };
            var tt3 = new FacultyTimetable
            {
                FacultyId = facultyDeepa.FacultyId,
                DayOfWeek = "MONDAY",
                PeriodNumber = 3,
                StartTime = new TimeSpan(10, 45, 0),
                EndTime = new TimeSpan(11, 45, 0),
                RoomId = roomLab201.RoomId,
                CourseCode = "BCA382",
                CourseName = "Advanced Data Structures Lab",
                ClassSection = "4BCA-A"
            };

            context.FacultyTimetables.AddRange(tt1, tt2, tt3);
            context.SaveChanges();

            // 7. Cafeteria Vendors & Items
            var vendorMain = new CafeteriaVendor
            {
                VendorName = "Christ Central Cafeteria (South & North Kitchen)",
                BlockId = blockA.BlockId,
                ContactPhone = "+91 80 4012 9000",
                IsOpen = true
            };
            var vendorCafe = new CafeteriaVendor
            {
                VendorName = "Campus Brew & Bakery Desk",
                BlockId = blockB.BlockId,
                ContactPhone = "+91 80 4012 9005",
                IsOpen = true
            };
            context.CafeteriaVendors.AddRange(vendorMain, vendorCafe);
            context.SaveChanges();

            var item1 = new CafeteriaItem { VendorId = vendorMain.VendorId, ItemName = "Masala Dosa with Sambar & Chutney", Category = "BREAKFAST", Price = 45.00m, CurrentStockQty = 60 };
            var item2 = new CafeteriaItem { VendorId = vendorMain.VendorId, ItemName = "South Indian Thali Meal", Category = "LUNCH", Price = 70.00m, CurrentStockQty = 120 };
            var item3 = new CafeteriaItem { VendorId = vendorMain.VendorId, ItemName = "Paneer Butter Masala Combo", Category = "LUNCH", Price = 90.00m, CurrentStockQty = 40 };
            var item4 = new CafeteriaItem { VendorId = vendorCafe.VendorId, ItemName = "Cappuccino (Filter Blend)", Category = "BEVERAGES", Price = 25.00m, CurrentStockQty = 200 };
            var item5 = new CafeteriaItem { VendorId = vendorCafe.VendorId, ItemName = "Grilled Veggie & Cheese Sandwich", Category = "SNACKS", Price = 50.00m, CurrentStockQty = 35 };

            context.CafeteriaItems.AddRange(item1, item2, item3, item4, item5);
            context.SaveChanges();

            // 8. Parking Slots
            var slot1 = new ParkingSlot { BlockId = blockA.BlockId, SlotCode = "A-TW-01", VehicleType = "TWO_WHEELER", IsEvCharging = false, IsOccupied = false };
            var slot2 = new ParkingSlot { BlockId = blockA.BlockId, SlotCode = "A-EV-02", VehicleType = "TWO_WHEELER", IsEvCharging = true, IsOccupied = true, AssignedVehicleReg = "KA-04-MB-4512" };
            var slot3 = new ParkingSlot { BlockId = blockB.BlockId, SlotCode = "B-FW-10", VehicleType = "FOUR_WHEELER", IsEvCharging = false, IsOccupied = false };
            var slot4 = new ParkingSlot { BlockId = blockB.BlockId, SlotCode = "B-EV-11", VehicleType = "FOUR_WHEELER", IsEvCharging = true, IsOccupied = false };

            context.ParkingSlots.AddRange(slot1, slot2, slot3, slot4);
            context.SaveChanges();

            // 9. Grievance Categories & Initial Ticket
            var g1 = new Grievance
            {
                StudentId = userStudent1.UserId,
                Category = "LAB_EQUIPMENT",
                RoomId = roomLab201.RoomId,
                TicketSubject = "System #24 projector HDMI flickering in DBMS Lab",
                Description = "During practical lab presentation, the secondary display keeps disconnecting every 5 minutes.",
                Priority = "MEDIUM",
                Status = "IN_PROGRESS",
                AssignedToStaffId = userFaculty1.UserId,
                CreatedAt = DateTime.UtcNow.AddHours(-4)
            };
            context.Grievances.Add(g1);
            context.SaveChanges();

            // 10. Library Book Sample
            var catCs = new BookCategory { CategoryName = "Computer Science & Database Engineering" };
            context.BookCategories.Add(catCs);
            context.SaveChanges();

            var book1 = new LibraryBook
            {
                Isbn = "978-0133970777",
                Title = "Fundamentals of Database Systems (7th Edition)",
                Author = "Ramez Elmasri, Shamkant B. Navathe",
                Publisher = "Pearson",
                Edition = "7th",
                CategoryId = catCs.CategoryId,
                TotalCopies = 10,
                AvailableCopies = 7,
                ShelfLocation = "Stack 3, Shelf B2"
            };
            var book2 = new LibraryBook
            {
                Isbn = "978-0078022159",
                Title = "Database System Concepts",
                Author = "Abraham Silberschatz, Henry F. Korth, S. Sudarshan",
                Publisher = "McGraw-Hill",
                Edition = "6th",
                CategoryId = catCs.CategoryId,
                TotalCopies = 12,
                AvailableCopies = 9,
                ShelfLocation = "Stack 3, Shelf B3"
            };
            context.LibraryBooks.AddRange(book1, book2);
            context.SaveChanges();

            Console.WriteLine("[DbInitializer] Seeding Completed Successfully.");
        }
    }
}

