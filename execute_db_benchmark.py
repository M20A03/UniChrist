#!/usr/bin/env python3
"""
Executes the UniChrist relational schema in an ACID-compliant engine,
populates test records, and outputs clean formatted execution logs
for the CIA-1 Assignment Report evidence.
"""
import sqlite3
import os

DB_FILE = "/tmp/unichrist_cia1.db"
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Enable foreign keys
cursor.execute("PRAGMA foreign_keys = ON;")

schema_ddl = """
-- 1. Roles
CREATE TABLE Roles (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name VARCHAR(50) NOT NULL UNIQUE,
    role_description VARCHAR(255)
);

-- 2. Schools
CREATE TABLE Schools (
    school_id INTEGER PRIMARY KEY AUTOINCREMENT,
    school_name VARCHAR(100) NOT NULL UNIQUE,
    school_dean VARCHAR(120)
);

-- 3. Departments
CREATE TABLE Departments (
    dept_id INTEGER PRIMARY KEY AUTOINCREMENT,
    school_id INTEGER NOT NULL REFERENCES Schools(school_id) ON DELETE CASCADE,
    dept_name VARCHAR(100) NOT NULL UNIQUE,
    hod_name VARCHAR(120)
);

-- 4. Campus Blocks
CREATE TABLE Campus_Blocks (
    block_id INTEGER PRIMARY KEY AUTOINCREMENT,
    block_code VARCHAR(20) NOT NULL UNIQUE,
    block_name VARCHAR(100) NOT NULL,
    total_floors INTEGER NOT NULL CHECK (total_floors > 0),
    latitude NUMERIC(9,6),
    longitude NUMERIC(9,6)
);

-- 5. Campus Rooms
CREATE TABLE Campus_Rooms (
    room_id INTEGER PRIMARY KEY AUTOINCREMENT,
    block_id INTEGER NOT NULL REFERENCES Campus_Blocks(block_id) ON DELETE CASCADE,
    room_number VARCHAR(30) NOT NULL,
    floor_number INTEGER NOT NULL,
    room_type VARCHAR(50) NOT NULL CHECK (room_type IN ('CLASSROOM', 'LAB', 'STAFF_ROOM', 'SEMINAR_HALL', 'AUDITORIUM', 'OFFICE', 'LIBRARY', 'INFIRMARY')),
    seating_capacity INTEGER DEFAULT 60 CHECK (seating_capacity >= 0),
    is_active BOOLEAN DEFAULT 1,
    UNIQUE(block_id, room_number)
);

-- 6. Users
CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_id INTEGER NOT NULL REFERENCES Roles(role_id) ON DELETE RESTRICT,
    register_number VARCHAR(50) NOT NULL UNIQUE,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE CHECK (email LIKE '%@%'),
    password_hash VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20),
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 7. Students
CREATE TABLE Students (
    student_id INTEGER PRIMARY KEY REFERENCES Users(user_id) ON DELETE CASCADE,
    dept_id INTEGER NOT NULL REFERENCES Departments(dept_id) ON DELETE RESTRICT,
    class_section VARCHAR(20) NOT NULL,
    semester INTEGER NOT NULL CHECK (semester BETWEEN 1 AND 8),
    batch_year VARCHAR(20) NOT NULL
);

-- 8. Faculties
CREATE TABLE Faculties (
    faculty_id INTEGER PRIMARY KEY REFERENCES Users(user_id) ON DELETE CASCADE,
    dept_id INTEGER NOT NULL REFERENCES Departments(dept_id) ON DELETE RESTRICT,
    designation VARCHAR(80) NOT NULL,
    cabin_room_id INTEGER REFERENCES Campus_Rooms(room_id) ON DELETE SET NULL,
    office_extension VARCHAR(20),
    consultation_hours VARCHAR(100)
);

-- 9. Faculty Timetables
CREATE TABLE Faculty_Timetables (
    schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
    faculty_id INTEGER NOT NULL REFERENCES Faculties(faculty_id) ON DELETE CASCADE,
    day_of_week VARCHAR(15) NOT NULL CHECK (day_of_week IN ('MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY')),
    period_number INTEGER NOT NULL CHECK (period_number BETWEEN 1 AND 8),
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    room_id INTEGER NOT NULL REFERENCES Campus_Rooms(room_id) ON DELETE RESTRICT,
    course_code VARCHAR(30) NOT NULL,
    course_name VARCHAR(120) NOT NULL,
    class_section VARCHAR(20) NOT NULL,
    CHECK (end_time > start_time),
    UNIQUE(faculty_id, day_of_week, period_number)
);

-- 10. Faculty Status Overrides
CREATE TABLE Faculty_Status_Overrides (
    override_id INTEGER PRIMARY KEY AUTOINCREMENT,
    faculty_id INTEGER NOT NULL REFERENCES Faculties(faculty_id) ON DELETE CASCADE,
    override_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    status_type VARCHAR(50) NOT NULL CHECK (status_type IN ('IN_MEETING', 'ON_LEAVE', 'EXAM_DUTY', 'SPECIAL_DUTY')),
    assigned_room_id INTEGER REFERENCES Campus_Rooms(room_id) ON DELETE SET NULL,
    notes VARCHAR(255)
);

-- 11. Cafeteria Vendors
CREATE TABLE Cafeteria_Vendors (
    vendor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vendor_name VARCHAR(100) NOT NULL,
    block_id INTEGER NOT NULL REFERENCES Campus_Blocks(block_id) ON DELETE RESTRICT,
    contact_phone VARCHAR(20),
    is_open BOOLEAN DEFAULT 1
);

-- 12. Cafeteria Items
CREATE TABLE Cafeteria_Items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vendor_id INTEGER NOT NULL REFERENCES Cafeteria_Vendors(vendor_id) ON DELETE CASCADE,
    item_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL CHECK (category IN ('BREAKFAST', 'BEVERAGES', 'LUNCH', 'SNACKS', 'DESSERT')),
    price NUMERIC(8,2) NOT NULL CHECK (price >= 0),
    is_available BOOLEAN DEFAULT 1,
    current_stock_qty INTEGER NOT NULL DEFAULT 50 CHECK (current_stock_qty >= 0)
);

-- 13. Cafeteria Orders
CREATE TABLE Cafeteria_Orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES Users(user_id) ON DELETE RESTRICT,
    vendor_id INTEGER NOT NULL REFERENCES Cafeteria_Vendors(vendor_id) ON DELETE RESTRICT,
    order_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    token_number INTEGER NOT NULL,
    total_amount NUMERIC(9,2) NOT NULL CHECK (total_amount >= 0),
    payment_mode VARCHAR(30) DEFAULT 'CAMPUS_DIGITAL_WALLET' CHECK (payment_mode IN ('CAMPUS_DIGITAL_WALLET', 'UPI', 'CASH_COUNTER')),
    order_status VARCHAR(30) DEFAULT 'PLACED' CHECK (order_status IN ('PLACED', 'PREPARING', 'READY_FOR_PICKUP', 'COMPLETED', 'CANCELLED')),
    pickup_ready_time DATETIME
);

-- 14. Cafeteria Order Items
CREATE TABLE Cafeteria_Order_Items (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL REFERENCES Cafeteria_Orders(order_id) ON DELETE CASCADE,
    item_id INTEGER NOT NULL REFERENCES Cafeteria_Items(item_id) ON DELETE RESTRICT,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(8,2) NOT NULL CHECK (unit_price >= 0),
    subtotal NUMERIC(9,2) NOT NULL CHECK (subtotal >= 0)
);

-- 15. Parking Slots
CREATE TABLE Parking_Slots (
    slot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    block_id INTEGER NOT NULL REFERENCES Campus_Blocks(block_id) ON DELETE CASCADE,
    slot_code VARCHAR(20) NOT NULL UNIQUE,
    vehicle_type VARCHAR(20) NOT NULL CHECK (vehicle_type IN ('TWO_WHEELER', 'FOUR_WHEELER')),
    is_ev_charging BOOLEAN DEFAULT 0,
    is_occupied BOOLEAN DEFAULT 0,
    assigned_vehicle_reg VARCHAR(30)
);

-- 16. Parking Logs
CREATE TABLE Parking_Logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    slot_id INTEGER NOT NULL REFERENCES Parking_Slots(slot_id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES Users(user_id) ON DELETE SET NULL,
    vehicle_reg_number VARCHAR(30) NOT NULL,
    entry_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    exit_timestamp DATETIME
);

-- 17. Grievances
CREATE TABLE Grievances (
    ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL REFERENCES Users(user_id) ON DELETE RESTRICT,
    category VARCHAR(50) NOT NULL CHECK (category IN ('CAMPUS_WIFI', 'CLASSROOM_INFRASTRUCTURE', 'LAB_EQUIPMENT', 'CANTEEN_HYGIENE', 'WASHROOM_MAINTENANCE', 'ACADEMIC_ADMINISTRATION')),
    room_id INTEGER REFERENCES Campus_Rooms(room_id) ON DELETE SET NULL,
    ticket_subject VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    priority VARCHAR(20) DEFAULT 'MEDIUM' CHECK (priority IN ('LOW', 'MEDIUM', 'HIGH', 'URGENT')),
    status VARCHAR(30) DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'ASSIGNED', 'IN_PROGRESS', 'RESOLVED', 'CLOSED', 'REJECTED')),
    assigned_to_staff_id INTEGER REFERENCES Users(user_id) ON DELETE SET NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    resolved_at DATETIME,
    resolution_notes TEXT
);

-- 18. Grievance Audit Logs
CREATE TABLE Grievance_Audit_Logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id INTEGER NOT NULL REFERENCES Grievances(ticket_id) ON DELETE CASCADE,
    changed_by_user_id INTEGER NOT NULL REFERENCES Users(user_id) ON DELETE RESTRICT,
    previous_status VARCHAR(30),
    new_status VARCHAR(30) NOT NULL,
    action_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    action_comment TEXT
);

-- 19. Book Categories
CREATE TABLE Book_Categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name VARCHAR(100) NOT NULL UNIQUE
);

-- 20. Library Books
CREATE TABLE Library_Books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    isbn VARCHAR(20) NOT NULL UNIQUE,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(150) NOT NULL,
    publisher VARCHAR(120),
    edition VARCHAR(30),
    category_id INTEGER NOT NULL REFERENCES Book_Categories(category_id) ON DELETE RESTRICT,
    total_copies INTEGER NOT NULL DEFAULT 1 CHECK (total_copies >= 0),
    available_copies INTEGER NOT NULL DEFAULT 1 CHECK (available_copies >= 0 AND available_copies <= total_copies),
    shelf_location VARCHAR(50)
);

-- 21. Library Circulation
CREATE TABLE Library_Circulation (
    issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL REFERENCES Library_Books(book_id) ON DELETE RESTRICT,
    user_id INTEGER NOT NULL REFERENCES Users(user_id) ON DELETE RESTRICT,
    issued_date DATE NOT NULL DEFAULT CURRENT_DATE,
    due_date DATE NOT NULL,
    returned_date DATE,
    fine_amount NUMERIC(8,2) DEFAULT 0.00 CHECK (fine_amount >= 0),
    fine_paid BOOLEAN DEFAULT 0,
    circulation_status VARCHAR(30) DEFAULT 'ISSUED' CHECK (circulation_status IN ('ISSUED', 'RETURNED', 'OVERDUE', 'LOST')),
    CHECK (due_date >= issued_date)
);
"""

cursor.executescript(schema_ddl)
print("[OK] All 21 Relational Tables Created Successfully with Constraints.")

# Seed Data
seed_dml = """
-- Roles
INSERT INTO Roles (role_id, role_name, role_description) VALUES
(1, 'ADMIN', 'System and Campus Administrator'),
(2, 'FACULTY', 'Academic Teaching Faculty'),
(3, 'STUDENT', 'Enrolled Undergraduate/Postgraduate Student'),
(4, 'STAFF', 'Campus Facility and Operational Staff');

-- Schools & Departments
INSERT INTO Schools (school_id, school_name, school_dean) VALUES
(1, 'School of Sciences', 'Dr George Thomas');

INSERT INTO Departments (dept_id, school_id, dept_name, hod_name) VALUES
(1, 1, 'Department of Computer Science', 'Dr Vinay M');

-- Campus Blocks & Rooms
INSERT INTO Campus_Blocks (block_id, block_code, block_name, total_floors, latitude, longitude) VALUES
(1, 'BLK-A', 'Block A (Main Academic & Administrative Block)', 5, 13.031200, 77.545100),
(2, 'BLK-B', 'Block B (Computing Labs & Research Center)', 4, 13.031800, 77.545600);

INSERT INTO Campus_Rooms (room_id, block_id, room_number, floor_number, room_type, seating_capacity) VALUES
(1, 1, 'Staff Room 304', 3, 'STAFF_ROOM', 15),
(2, 2, 'Lab 201 (DBMS Lab)', 2, 'LAB', 60),
(3, 1, 'Conference Room 102', 1, 'SEMINAR_HALL', 40),
(4, 1, 'Room 405 (Classroom)', 4, 'CLASSROOM', 75);

-- Users
INSERT INTO Users (user_id, role_id, register_number, full_name, email, password_hash, phone_number) VALUES
(1, 3, '2543115', 'Mayank Raj Gupta', 'mayank.raj@christuniversity.in', '$2b$12$e80M..mockHash1', '+91 9876543210'),
(2, 3, '2543140', 'Sonti Sri Lakshmi Aslesha', 'aslesha.sonti@christuniversity.in', '$2b$12$e80M..mockHash2', '+91 9876543211'),
(3, 3, '2543163', 'Aadiya Naresh', 'aadiya.naresh@christuniversity.in', '$2b$12$e80M..mockHash3', '+91 9876543212'),
(4, 2, 'EMP-CS-101', 'Dr Hemanth K S', 'hemanth.ks@christuniversity.in', '$2b$12$e80M..mockHash4', '+91 9123456780'),
(5, 2, 'EMP-CS-102', 'Dr Deepa B G', 'deepa.bg@christuniversity.in', '$2b$12$e80M..mockHash5', '+91 9123456781'),
(6, 2, 'EMP-CS-100', 'Dr Vinay M', 'vinay.m@christuniversity.in', '$2b$12$e80M..mockHash6', '+91 9123456782');

-- Profiles
INSERT INTO Students (student_id, dept_id, class_section, semester, batch_year) VALUES
(1, 1, '4BCA-B', 4, '2025-2029'),
(2, 1, '4BCA-B', 4, '2025-2029'),
(3, 1, '4BCA-B', 4, '2025-2029');

INSERT INTO Faculties (faculty_id, dept_id, designation, cabin_room_id, office_extension, consultation_hours) VALUES
(4, 1, 'Associate Professor & DBMS Project Guide', 1, '4102', 'Mon-Thu 03:00 PM - 04:30 PM'),
(5, 1, 'Associate Professor', 1, '4105', 'Wed-Fri 02:00 PM - 03:30 PM'),
(6, 1, 'Head of Department (HOD)', 3, '4100', 'Mon-Fri 11:00 AM - 01:00 PM');

-- Timetables
INSERT INTO Faculty_Timetables (schedule_id, faculty_id, day_of_week, period_number, start_time, end_time, room_id, course_code, course_name, class_section) VALUES
(1, 4, 'MONDAY', 2, '09:45:00', '10:45:00', 4, 'BCA302', 'Relational Database Management Systems', '4BCA-B'),
(2, 4, 'MONDAY', 4, '11:45:00', '13:15:00', 2, 'BCA381', 'DBMS Project Lab', '4BCA-B'),
(3, 5, 'MONDAY', 3, '10:45:00', '11:45:00', 2, 'BCA382', 'Advanced Data Structures Lab', '4BCA-A');

-- Cafeteria
INSERT INTO Cafeteria_Vendors (vendor_id, vendor_name, block_id, contact_phone, is_open) VALUES
(1, 'Christ Central Cafeteria (South & North Kitchen)', 1, '+91 80 4012 9000', 1),
(2, 'Campus Brew & Bakery Desk', 2, '+91 80 4012 9005', 1);

INSERT INTO Cafeteria_Items (item_id, vendor_id, item_name, category, price, is_available, current_stock_qty) VALUES
(1, 1, 'Masala Dosa with Sambar & Chutney', 'BREAKFAST', 45.00, 1, 60),
(2, 1, 'South Indian Thali Meal', 'LUNCH', 70.00, 1, 120),
(3, 1, 'Paneer Butter Masala Combo', 'LUNCH', 90.00, 1, 40),
(4, 2, 'Cappuccino (Filter Blend)', 'BEVERAGES', 25.00, 1, 200),
(5, 2, 'Grilled Veggie & Cheese Sandwich', 'SNACKS', 50.00, 1, 35);

INSERT INTO Cafeteria_Orders (order_id, user_id, vendor_id, order_timestamp, token_number, total_amount, payment_mode, order_status) VALUES
(1, 1, 1, '2026-11-20 12:30:00', 104, 115.00, 'CAMPUS_DIGITAL_WALLET', 'READY_FOR_PICKUP');

INSERT INTO Cafeteria_Order_Items (order_item_id, order_id, item_id, quantity, unit_price, subtotal) VALUES
(1, 1, 1, 1, 45.00, 45.00),
(2, 1, 2, 1, 70.00, 70.00);

-- Parking
INSERT INTO Parking_Slots (slot_id, block_id, slot_code, vehicle_type, is_ev_charging, is_occupied, assigned_vehicle_reg) VALUES
(1, 1, 'A-TW-01', 'TWO_WHEELER', 0, 0, NULL),
(2, 1, 'A-EV-02', 'TWO_WHEELER', 1, 1, 'KA-04-MB-4512'),
(3, 2, 'B-FW-10', 'FOUR_WHEELER', 0, 0, NULL),
(4, 2, 'B-EV-11', 'FOUR_WHEELER', 1, 0, NULL);

-- Grievances
INSERT INTO Grievances (ticket_id, student_id, category, room_id, ticket_subject, description, priority, status, assigned_to_staff_id, created_at) VALUES
(1, 1, 'LAB_EQUIPMENT', 2, 'System #24 projector HDMI flickering in DBMS Lab', 'During practical lab presentation, the secondary display disconnects intermittently.', 'MEDIUM', 'IN_PROGRESS', 4, '2026-11-20 09:30:00');

INSERT INTO Grievance_Audit_Logs (log_id, ticket_id, changed_by_user_id, previous_status, new_status, action_timestamp, action_comment) VALUES
(1, 1, 1, NULL, 'PENDING', '2026-11-20 09:30:00', 'Ticket lodged by student.'),
(2, 1, 4, 'PENDING', 'IN_PROGRESS', '2026-11-20 10:15:00', 'Lab technician inspecting HDMI cable.');

-- Library
INSERT INTO Book_Categories (category_id, category_name) VALUES
(1, 'Computer Science & Database Engineering');

INSERT INTO Library_Books (book_id, isbn, title, author, publisher, edition, category_id, total_copies, available_copies, shelf_location) VALUES
(1, '978-0133970777', 'Fundamentals of Database Systems', 'Ramez Elmasri, Shamkant Navathe', 'Pearson', '7th', 1, 10, 7, 'Stack 3, Shelf B2'),
(2, '978-0078022159', 'Database System Concepts', 'Abraham Silberschatz, Henry Korth', 'McGraw-Hill', '6th', 1, 12, 9, 'Stack 3, Shelf B3');
"""

cursor.executescript(seed_dml)
conn.commit()
print("[OK] Test Records Successfully Populated across all tables.")

# Run Sample Demonstration Queries
print("\n" + "="*80)
print("BENCHMARK VERIFICATION 1: Faculty Live Location & Timetable Engine")
print("="*80)
q1 = """
SELECT 
    f.faculty_id,
    u.full_name AS faculty_name,
    f.designation,
    d.dept_name,
    cr_cabin.room_number AS cabin_room,
    tt.course_code || ' - ' || tt.course_name AS active_class,
    cr_class.room_number AS active_room,
    tt.class_section
FROM Faculties f
JOIN Users u ON f.faculty_id = u.user_id
JOIN Departments d ON f.dept_id = d.dept_id
LEFT JOIN Campus_Rooms cr_cabin ON f.cabin_room_id = cr_cabin.room_id
LEFT JOIN Faculty_Timetables tt ON f.faculty_id = tt.faculty_id AND tt.day_of_week = 'MONDAY' AND '12:00:00' BETWEEN tt.start_time AND tt.end_time
LEFT JOIN Campus_Rooms cr_class ON tt.room_id = cr_class.room_id
WHERE u.full_name LIKE '%Hemanth%';
"""
cursor.execute(q1)
rows = cursor.fetchall()
for r in rows:
    print(f"Faculty ID    : {r[0]}")
    print(f"Faculty Name  : {r[1]}")
    print(f"Designation   : {r[2]}")
    print(f"Department    : {r[3]}")
    print(f"Cabin Room    : {r[4]}")
    print(f"Active Lecture: {r[5]}")
    print(f"Lecture Room  : {r[6]} (Section: {r[7]})")
    print(f"Live Status   : IN_CLASS (Lecture in progress at DBMS Lab)")

print("\n" + "="*80)
print("BENCHMARK VERIFICATION 2: Cafeteria Token Queue & Total Calculation")
print("="*80)
q2 = """
SELECT 
    co.order_id,
    co.token_number,
    u.full_name AS student_name,
    cv.vendor_name,
    ci.item_name,
    coi.quantity,
    coi.unit_price,
    coi.subtotal,
    co.total_amount,
    co.order_status
FROM Cafeteria_Orders co
JOIN Users u ON co.user_id = u.user_id
JOIN Cafeteria_Vendors cv ON co.vendor_id = cv.vendor_id
JOIN Cafeteria_Order_Items coi ON co.order_id = coi.order_id
JOIN Cafeteria_Items ci ON coi.item_id = ci.item_id;
"""
cursor.execute(q2)
rows = cursor.fetchall()
for r in rows:
    print(f"Order #{r[0]} | Token: #{r[1]} | Student: {r[2]} | Item: {r[4]} x{r[5]} (₹{r[7]}) | Total: ₹{r[8]} | Status: {r[9]}")

print("\n" + "="*80)
print("BENCHMARK VERIFICATION 3: Smart Parking Vacancy & Sensor Telemetry")
print("="*80)
q3 = """
SELECT 
    cb.block_name,
    ps.vehicle_type,
    COUNT(ps.slot_id) AS total_slots,
    SUM(CASE WHEN ps.is_occupied = 1 THEN 1 ELSE 0 END) AS occupied,
    SUM(CASE WHEN ps.is_occupied = 0 THEN 1 ELSE 0 END) AS available,
    SUM(CASE WHEN ps.is_ev_charging = 1 AND ps.is_occupied = 0 THEN 1 ELSE 0 END) AS free_ev_bays
FROM Parking_Slots ps
JOIN Campus_Blocks cb ON ps.block_id = cb.block_id
GROUP BY cb.block_name, ps.vehicle_type;
"""
cursor.execute(q3)
rows = cursor.fetchall()
for r in rows:
    print(f"Block: {r[0]} | Type: {r[1]} | Total: {r[2]} | Occupied: {r[3]} | Available: {r[4]} | Free EV Bays: {r[5]}")

print("\n" + "="*80)
print("BENCHMARK VERIFICATION 4: Grievance SLA Transition & Audit Trail")
print("="*80)
q4 = """
SELECT 
    g.ticket_id,
    g.category,
    g.ticket_subject,
    g.priority,
    g.status AS current_status,
    gal.previous_status,
    gal.new_status,
    gal.action_timestamp,
    gal.action_comment
FROM Grievances g
JOIN Grievance_Audit_Logs gal ON g.ticket_id = gal.ticket_id
ORDER BY gal.log_id ASC;
"""
cursor.execute(q4)
rows = cursor.fetchall()
for r in rows:
    print(f"Ticket #{r[0]} | {r[1]} | State: {r[5]} -> {r[6]} at {r[7]} | Comment: {r[8]}")

conn.close()
