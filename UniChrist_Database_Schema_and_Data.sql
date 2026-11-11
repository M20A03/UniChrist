-- ============================================================================
-- DATABASE MANAGEMENT SYSTEMS PROJECT (BCA381-4)
-- CHRIST (Deemed to be University) - Bangalore Yeshwanthpur Campus
-- Department of Computer Science | Class: 4BCA-B | Academic Year: 2025-2026
--
-- PROJECT TITLE: UniChrist - Integrated Smart Campus ERP & Location-Aware Services Management System
--
-- TEAM MEMBERS:
--   1. Mayank Raj Gupta (2543115) - Team Lead / Backend & Database Architect
--   2. Sonti Sri Lakshmi Aslesha (2543140) - Core Developer & Schema Analyst
--   3. Aadiya Naresh (2543163) - System Analyst, UI/UX & Integration Specialist
--
-- PROJECT GUIDE: Dr Hemanth K S
-- ============================================================================

-- Drop existing tables with CASCADE to ensure clean recreation
DROP TABLE IF EXISTS Academic_Resources CASCADE;
DROP TABLE IF EXISTS Grievance_Audit_Logs CASCADE;
DROP TABLE IF EXISTS Grievances CASCADE;
DROP TABLE IF EXISTS Club_Memberships CASCADE;
DROP TABLE IF EXISTS Student_Clubs CASCADE;
DROP TABLE IF EXISTS Event_Registrations CASCADE;
DROP TABLE IF EXISTS Campus_Events CASCADE;
DROP TABLE IF EXISTS Parking_Logs CASCADE;
DROP TABLE IF EXISTS Parking_Slots CASCADE;
DROP TABLE IF EXISTS Library_Circulation CASCADE;
DROP TABLE IF EXISTS Library_Books CASCADE;
DROP TABLE IF EXISTS Book_Categories CASCADE;
DROP TABLE IF EXISTS Lost_Found_Claims CASCADE;
DROP TABLE IF EXISTS Lost_Found_Items CASCADE;
DROP TABLE IF EXISTS Medical_Prescriptions CASCADE;
DROP TABLE IF EXISTS Medical_Visits CASCADE;
DROP TABLE IF EXISTS Store_Order_Items CASCADE;
DROP TABLE IF EXISTS Store_Orders CASCADE;
DROP TABLE IF EXISTS Store_Inventory CASCADE;
DROP TABLE IF EXISTS Store_Categories CASCADE;
DROP TABLE IF EXISTS Cafeteria_Order_Items CASCADE;
DROP TABLE IF EXISTS Cafeteria_Orders CASCADE;
DROP TABLE IF EXISTS Cafeteria_Items CASCADE;
DROP TABLE IF EXISTS Cafeteria_Vendors CASCADE;
DROP TABLE IF EXISTS Teacher_Presence_Logs CASCADE;
DROP TABLE IF EXISTS Teacher_Current_Status CASCADE;
DROP TABLE IF EXISTS Biometric_Checkpoints CASCADE;
DROP TABLE IF EXISTS Campus_Rooms CASCADE;
DROP TABLE IF EXISTS Campus_Blocks CASCADE;
DROP TABLE IF EXISTS Faculties CASCADE;
DROP TABLE IF EXISTS Students CASCADE;
DROP TABLE IF EXISTS Departments CASCADE;
DROP TABLE IF EXISTS Schools CASCADE;
DROP TABLE IF EXISTS User_Sessions CASCADE;
DROP TABLE IF EXISTS Users CASCADE;
DROP TABLE IF EXISTS Roles CASCADE;

-- ============================================================================
-- 1. CORE AUTHENTICATION, ROLES & CAMPUS INFRASTRUCTURE
-- ============================================================================

CREATE TABLE Roles (
    role_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL UNIQUE,
    role_description VARCHAR(255)
);

CREATE TABLE Users (
    user_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    role_id INT NOT NULL REFERENCES Roles(role_id) ON DELETE RESTRICT,
    register_number VARCHAR(50) NOT NULL UNIQUE,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_email_format CHECK (email LIKE '%@%christuniversity.in' OR email LIKE '%@%')
);

CREATE TABLE Schools (
    school_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    school_name VARCHAR(100) NOT NULL UNIQUE,
    school_dean VARCHAR(120)
);

CREATE TABLE Departments (
    dept_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    school_id INT NOT NULL REFERENCES Schools(school_id) ON DELETE CASCADE,
    dept_name VARCHAR(100) NOT NULL UNIQUE,
    hod_name VARCHAR(120)
);

CREATE TABLE Campus_Blocks (
    block_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    block_code VARCHAR(20) NOT NULL UNIQUE,
    block_name VARCHAR(100) NOT NULL,
    total_floors INT NOT NULL CHECK (total_floors > 0),
    latitude NUMERIC(9,6),
    longitude NUMERIC(9,6)
);

CREATE TABLE Campus_Rooms (
    room_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    block_id INT NOT NULL REFERENCES Campus_Blocks(block_id) ON DELETE CASCADE,
    room_number VARCHAR(30) NOT NULL,
    floor_number INT NOT NULL,
    room_type VARCHAR(50) NOT NULL CHECK (room_type IN ('CLASSROOM', 'LAB', 'STAFF_ROOM', 'SEMINAR_HALL', 'AUDITORIUM', 'OFFICE', 'LIBRARY', 'INFIRMARY')),
    seating_capacity INT DEFAULT 60 CHECK (seating_capacity >= 0),
    is_active BOOLEAN DEFAULT TRUE,
    CONSTRAINT uq_block_room UNIQUE (block_id, room_number)
);

CREATE TABLE Students (
    student_id INT PRIMARY KEY REFERENCES Users(user_id) ON DELETE CASCADE,
    dept_id INT NOT NULL REFERENCES Departments(dept_id) ON DELETE RESTRICT,
    class_section VARCHAR(20) NOT NULL,
    semester INT NOT NULL CHECK (semester BETWEEN 1 AND 8),
    batch_year VARCHAR(20) NOT NULL
);

CREATE TABLE Faculties (
    faculty_id INT PRIMARY KEY REFERENCES Users(user_id) ON DELETE CASCADE,
    dept_id INT NOT NULL REFERENCES Departments(dept_id) ON DELETE RESTRICT,
    designation VARCHAR(80) NOT NULL,
    cabin_room_id INT REFERENCES Campus_Rooms(room_id) ON DELETE SET NULL,
    office_extension VARCHAR(20),
    consultation_hours VARCHAR(100)
);

-- ============================================================================
-- 2. TEACHER BIOMETRIC CHECKPOINT & REAL-TIME PRESENCE TRACKING
-- ============================================================================

-- ============================================================================
-- 2. FACULTY TIMETABLE & AUTOMATED LOCATION ENGINE (GUIDE RECOMMENDATION)
-- ============================================================================

CREATE TABLE Faculty_Timetables (
    schedule_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    faculty_id INT NOT NULL REFERENCES Faculties(faculty_id) ON DELETE CASCADE,
    day_of_week VARCHAR(15) NOT NULL CHECK (day_of_week IN ('MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY')),
    period_number INT NOT NULL CHECK (period_number BETWEEN 1 AND 8),
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    room_id INT NOT NULL REFERENCES Campus_Rooms(room_id) ON DELETE RESTRICT,
    course_code VARCHAR(30) NOT NULL,
    course_name VARCHAR(120) NOT NULL,
    class_section VARCHAR(20) NOT NULL,
    CONSTRAINT chk_period_time CHECK (end_time > start_time),
    CONSTRAINT uq_faculty_period UNIQUE (faculty_id, day_of_week, period_number)
);

CREATE INDEX idx_timetable_lookup ON Faculty_Timetables(faculty_id, day_of_week, start_time, end_time);

CREATE TABLE Faculty_Status_Overrides (
    override_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    faculty_id INT NOT NULL REFERENCES Faculties(faculty_id) ON DELETE CASCADE,
    override_date DATE NOT NULL DEFAULT CURRENT_DATE,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    status_type VARCHAR(50) NOT NULL CHECK (status_type IN ('IN_MEETING', 'ON_LEAVE', 'EXAM_DUTY', 'SPECIAL_DUTY')),
    assigned_room_id INT REFERENCES Campus_Rooms(room_id) ON DELETE SET NULL,
    notes VARCHAR(255)
);

-- ============================================================================
-- 3. SMART CAFETERIA & DIGITAL PRE-ORDERING MODULE
-- ============================================================================

CREATE TABLE Cafeteria_Vendors (
    vendor_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    vendor_name VARCHAR(100) NOT NULL,
    block_id INT NOT NULL REFERENCES Campus_Blocks(block_id) ON DELETE RESTRICT,
    contact_phone VARCHAR(20),
    is_open BOOLEAN DEFAULT TRUE
);

CREATE TABLE Cafeteria_Items (
    item_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    vendor_id INT NOT NULL REFERENCES Cafeteria_Vendors(vendor_id) ON DELETE CASCADE,
    item_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL CHECK (category IN ('BREAKFAST', 'BEVERAGES', 'LUNCH', 'SNACKS', 'DESSERT')),
    price NUMERIC(8,2) NOT NULL CHECK (price >= 0),
    is_available BOOLEAN DEFAULT TRUE,
    current_stock_qty INT NOT NULL DEFAULT 50 CHECK (current_stock_qty >= 0)
);

CREATE TABLE Cafeteria_Orders (
    order_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INT NOT NULL REFERENCES Users(user_id) ON DELETE RESTRICT,
    vendor_id INT NOT NULL REFERENCES Cafeteria_Vendors(vendor_id) ON DELETE RESTRICT,
    order_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    token_number INT NOT NULL,
    total_amount NUMERIC(9,2) NOT NULL CHECK (total_amount >= 0),
    payment_mode VARCHAR(30) DEFAULT 'CAMPUS_DIGITAL_WALLET' CHECK (payment_mode IN ('CAMPUS_DIGITAL_WALLET', 'UPI', 'CASH_COUNTER')),
    order_status VARCHAR(30) DEFAULT 'PLACED' CHECK (order_status IN ('PLACED', 'PREPARING', 'READY_FOR_PICKUP', 'COMPLETED', 'CANCELLED')),
    pickup_ready_time TIMESTAMP WITH TIME ZONE
);

CREATE TABLE Cafeteria_Order_Items (
    order_item_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id INT NOT NULL REFERENCES Cafeteria_Orders(order_id) ON DELETE CASCADE,
    item_id INT NOT NULL REFERENCES Cafeteria_Items(item_id) ON DELETE RESTRICT,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(8,2) NOT NULL CHECK (unit_price >= 0),
    subtotal NUMERIC(9,2) NOT NULL CHECK (subtotal >= 0)
);

-- ============================================================================
-- 4. UNIVERSITY BOOKSTORE & CHRIST MERCHANDISE STORE
-- ============================================================================

CREATE TABLE Store_Categories (
    category_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    category_name VARCHAR(80) NOT NULL UNIQUE
);

CREATE TABLE Store_Inventory (
    product_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    category_id INT NOT NULL REFERENCES Store_Categories(category_id) ON DELETE RESTRICT,
    product_code VARCHAR(50) NOT NULL UNIQUE,
    product_name VARCHAR(120) NOT NULL,
    unit_price NUMERIC(8,2) NOT NULL CHECK (unit_price >= 0),
    stock_quantity INT NOT NULL DEFAULT 0 CHECK (stock_quantity >= 0),
    reorder_level INT NOT NULL DEFAULT 10,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE Store_Orders (
    store_order_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INT NOT NULL REFERENCES Users(user_id) ON DELETE RESTRICT,
    order_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    total_amount NUMERIC(9,2) NOT NULL CHECK (total_amount >= 0),
    order_status VARCHAR(30) DEFAULT 'CONFIRMED' CHECK (order_status IN ('CONFIRMED', 'COLLECTED', 'CANCELLED'))
);

CREATE TABLE Store_Order_Items (
    store_order_item_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    store_order_id INT NOT NULL REFERENCES Store_Orders(store_order_id) ON DELETE CASCADE,
    product_id INT NOT NULL REFERENCES Store_Inventory(product_id) ON DELETE RESTRICT,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(8,2) NOT NULL CHECK (unit_price >= 0),
    subtotal NUMERIC(9,2) NOT NULL CHECK (subtotal >= 0)
);

-- ============================================================================
-- 5. CAMPUS MEDICAL & INFIRMARY HEALTHCARE SERVICE
-- ============================================================================

CREATE TABLE Medical_Visits (
    visit_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    student_id INT NOT NULL REFERENCES Users(user_id) ON DELETE RESTRICT,
    attending_staff_id INT NOT NULL REFERENCES Users(user_id) ON DELETE RESTRICT,
    checkin_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    symptoms_observed TEXT NOT NULL,
    diagnosis_notes TEXT,
    temperature_celsius NUMERIC(4,1),
    blood_pressure VARCHAR(20),
    is_emergency_flag BOOLEAN DEFAULT FALSE,
    disposition VARCHAR(50) DEFAULT 'REST_IN_INFIRMARY' CHECK (disposition IN ('SENT_TO_CLASS', 'REST_IN_INFIRMARY', 'REFERRED_TO_HOSPITAL', 'PARENTS_INFORMED'))
);

CREATE TABLE Medical_Prescriptions (
    prescription_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    visit_id INT NOT NULL REFERENCES Medical_Visits(visit_id) ON DELETE CASCADE,
    medicine_name VARCHAR(100) NOT NULL,
    dosage VARCHAR(50) NOT NULL,
    quantity_dispensed INT NOT NULL DEFAULT 1 CHECK (quantity_dispensed > 0),
    instructions VARCHAR(150)
);

-- ============================================================================
-- 6. CAMPUS LOST & FOUND REPOSITORY
-- ============================================================================

CREATE TABLE Lost_Found_Items (
    item_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    reported_by_user_id INT NOT NULL REFERENCES Users(user_id) ON DELETE RESTRICT,
    item_title VARCHAR(120) NOT NULL,
    category VARCHAR(50) NOT NULL CHECK (category IN ('ELECTRONICS', 'ID_CARDS_WALLETS', 'BOOKS_NOTES', 'CLOTHING', 'KEYS', 'OTHERS')),
    description TEXT,
    photo_url VARCHAR(255),
    found_at_room_id INT REFERENCES Campus_Rooms(room_id) ON DELETE SET NULL,
    found_location_details VARCHAR(150),
    date_found TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    status VARCHAR(30) DEFAULT 'UNCLAIMED' CHECK (status IN ('UNCLAIMED', 'CLAIM_PENDING', 'VERIFIED_CLAIMED', 'ARCHIVED'))
);

CREATE TABLE Lost_Found_Claims (
    claim_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    item_id INT NOT NULL REFERENCES Lost_Found_Items(item_id) ON DELETE CASCADE,
    claimed_by_user_id INT NOT NULL REFERENCES Users(user_id) ON DELETE RESTRICT,
    claim_description TEXT NOT NULL,
    claim_submitted_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    verification_status VARCHAR(30) DEFAULT 'PENDING' CHECK (verification_status IN ('PENDING', 'APPROVED', 'REJECTED')),
    handed_over_by_security_id INT REFERENCES Users(user_id) ON DELETE SET NULL,
    handover_timestamp TIMESTAMP WITH TIME ZONE
);

-- ============================================================================
-- 7. CENTRALIZED LIBRARY OPAC & READING ROOM MANAGEMENT
-- ============================================================================

CREATE TABLE Book_Categories (
    category_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE Library_Books (
    book_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    isbn VARCHAR(20) NOT NULL UNIQUE,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(150) NOT NULL,
    publisher VARCHAR(120),
    edition VARCHAR(30),
    category_id INT NOT NULL REFERENCES Book_Categories(category_id) ON DELETE RESTRICT,
    total_copies INT NOT NULL DEFAULT 1 CHECK (total_copies >= 0),
    available_copies INT NOT NULL DEFAULT 1 CHECK (available_copies >= 0 AND available_copies <= total_copies),
    shelf_location VARCHAR(50)
);

CREATE TABLE Library_Circulation (
    issue_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    book_id INT NOT NULL REFERENCES Library_Books(book_id) ON DELETE RESTRICT,
    user_id INT NOT NULL REFERENCES Users(user_id) ON DELETE RESTRICT,
    issued_date DATE NOT NULL DEFAULT CURRENT_DATE,
    due_date DATE NOT NULL,
    returned_date DATE,
    fine_amount NUMERIC(8,2) DEFAULT 0.00 CHECK (fine_amount >= 0),
    fine_paid BOOLEAN DEFAULT FALSE,
    circulation_status VARCHAR(30) DEFAULT 'ISSUED' CHECK (circulation_status IN ('ISSUED', 'RETURNED', 'OVERDUE', 'LOST')),
    CONSTRAINT chk_due_date CHECK (due_date >= issued_date)
);

-- ============================================================================
-- 8. SMART PARKING & EV ALLOCATION MANAGEMENT
-- ============================================================================

CREATE TABLE Parking_Slots (
    slot_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    block_id INT NOT NULL REFERENCES Campus_Blocks(block_id) ON DELETE CASCADE,
    slot_code VARCHAR(20) NOT NULL UNIQUE,
    vehicle_type VARCHAR(20) NOT NULL CHECK (vehicle_type IN ('TWO_WHEELER', 'FOUR_WHEELER')),
    is_ev_charging BOOLEAN DEFAULT FALSE,
    is_occupied BOOLEAN DEFAULT FALSE,
    assigned_vehicle_reg VARCHAR(30)
);

CREATE TABLE Parking_Logs (
    log_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    slot_id INT NOT NULL REFERENCES Parking_Slots(slot_id) ON DELETE CASCADE,
    user_id INT REFERENCES Users(user_id) ON DELETE SET NULL,
    vehicle_reg_number VARCHAR(30) NOT NULL,
    entry_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    exit_timestamp TIMESTAMP WITH TIME ZONE,
    security_guard_user_id INT REFERENCES Users(user_id) ON DELETE SET NULL
);

-- ============================================================================
-- 9. CAMPUS EVENTS, FESTS & MULTI-SCHOOL CLUBS
-- ============================================================================

CREATE TABLE Student_Clubs (
    club_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    school_id INT NOT NULL REFERENCES Schools(school_id) ON DELETE CASCADE,
    club_name VARCHAR(120) NOT NULL UNIQUE,
    club_tagline VARCHAR(200),
    faculty_coordinator_id INT NOT NULL REFERENCES Faculties(faculty_id) ON DELETE RESTRICT,
    president_student_id INT REFERENCES Students(student_id) ON DELETE SET NULL,
    founded_year INT DEFAULT 2024
);

CREATE TABLE Club_Memberships (
    membership_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    club_id INT NOT NULL REFERENCES Student_Clubs(club_id) ON DELETE CASCADE,
    student_id INT NOT NULL REFERENCES Students(student_id) ON DELETE CASCADE,
    joined_date DATE DEFAULT CURRENT_DATE NOT NULL,
    member_role VARCHAR(40) DEFAULT 'MEMBER' CHECK (member_role IN ('MEMBER', 'CORE_COMMITTEE', 'TREASURER', 'SECRETARY', 'VICE_PRESIDENT')),
    CONSTRAINT uq_club_student UNIQUE (club_id, student_id)
);

CREATE TABLE Campus_Events (
    event_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    club_id INT REFERENCES Student_Clubs(club_id) ON DELETE SET NULL,
    event_title VARCHAR(150) NOT NULL,
    event_type VARCHAR(50) NOT NULL CHECK (event_type IN ('INTER_COLLEGE_FEST', 'HACKATHON', 'WORKSHOP', 'GUEST_LECTURE', 'CULTURAL_MEET')),
    venue_room_id INT NOT NULL REFERENCES Campus_Rooms(room_id) ON DELETE RESTRICT,
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE NOT NULL,
    max_registrations INT DEFAULT 100 CHECK (max_registrations > 0),
    current_registrations INT DEFAULT 0 CHECK (current_registrations <= max_registrations),
    is_open_for_registration BOOLEAN DEFAULT TRUE,
    CONSTRAINT chk_event_times CHECK (end_time > start_time)
);

CREATE TABLE Event_Registrations (
    registration_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    event_id INT NOT NULL REFERENCES Campus_Events(event_id) ON DELETE CASCADE,
    user_id INT NOT NULL REFERENCES Users(user_id) ON DELETE CASCADE,
    registration_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    qr_ticket_hash VARCHAR(100) NOT NULL UNIQUE,
    has_attended BOOLEAN DEFAULT FALSE,
    CONSTRAINT uq_event_user UNIQUE (event_id, user_id)
);

-- ============================================================================
-- 10. GRIEVANCE REDRESSAL & SLA TICKETING MODULE
-- ============================================================================

CREATE TABLE Grievances (
    ticket_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    student_id INT NOT NULL REFERENCES Users(user_id) ON DELETE RESTRICT,
    category VARCHAR(50) NOT NULL CHECK (category IN ('CAMPUS_WIFI', 'CLASSROOM_INFRASTRUCTURE', 'LAB_EQUIPMENT', 'CANTEEN_HYGIENE', 'WASHROOM_MAINTENANCE', 'ACADEMIC_ADMINISTRATION')),
    room_id INT REFERENCES Campus_Rooms(room_id) ON DELETE SET NULL,
    ticket_subject VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    priority VARCHAR(20) DEFAULT 'MEDIUM' CHECK (priority IN ('LOW', 'MEDIUM', 'HIGH', 'URGENT')),
    status VARCHAR(30) DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'ASSIGNED', 'IN_PROGRESS', 'RESOLVED', 'CLOSED', 'REJECTED')),
    assigned_to_staff_id INT REFERENCES Users(user_id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    resolved_at TIMESTAMP WITH TIME ZONE,
    resolution_notes TEXT
);

CREATE TABLE Grievance_Audit_Logs (
    log_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    ticket_id INT NOT NULL REFERENCES Grievances(ticket_id) ON DELETE CASCADE,
    changed_by_user_id INT NOT NULL REFERENCES Users(user_id) ON DELETE RESTRICT,
    previous_status VARCHAR(30),
    new_status VARCHAR(30) NOT NULL,
    action_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    action_comment TEXT
);

-- ============================================================================
-- 11. ACADEMIC & STUDENT RESOURCES REPOSITORY
-- ============================================================================

CREATE TABLE Academic_Resources (
    resource_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    dept_id INT NOT NULL REFERENCES Departments(dept_id) ON DELETE RESTRICT,
    uploaded_by_faculty_id INT NOT NULL REFERENCES Faculties(faculty_id) ON DELETE RESTRICT,
    resource_type VARCHAR(50) NOT NULL CHECK (resource_type IN ('SYLLABUS_COPY', 'PREVIOUS_YEAR_QP', 'LAB_MANUAL', 'LECTURE_NOTES', 'SOFTWARE_TOOL')),
    course_code VARCHAR(30) NOT NULL,
    course_title VARCHAR(120) NOT NULL,
    document_title VARCHAR(150) NOT NULL,
    file_storage_url VARCHAR(255) NOT NULL,
    upload_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    download_count INT DEFAULT 0
);

-- ============================================================================
-- 12. ADVANCED VIEWS FOR INSTANT QUERYING & REPORTING
-- ============================================================================

-- 1. Live Faculty Presence & Location View
CREATE OR REPLACE VIEW vw_LiveFacultyLocations AS
SELECT 
    f.faculty_id,
    u.full_name AS faculty_name,
    d.dept_name,
    f.designation,
    s.current_status,
    cb.block_name AS current_block,
    cr.room_number AS current_room,
    cr.room_type,
    bc.checkpoint_name AS last_scanned_checkpoint,
    s.last_updated_at,
    f.consultation_hours
FROM Teacher_Current_Status s
JOIN Faculties f ON s.faculty_id = f.faculty_id
JOIN Users u ON f.faculty_id = u.user_id
JOIN Departments d ON f.dept_id = d.dept_id
LEFT JOIN Campus_Rooms cr ON s.current_room_id = cr.room_id
LEFT JOIN Campus_Blocks cb ON cr.block_id = cb.block_id
LEFT JOIN Biometric_Checkpoints bc ON s.current_checkpoint_id = bc.checkpoint_id;

-- 2. Cafeteria Live Queue & Token Tracker View
CREATE OR REPLACE VIEW vw_CafeteriaLiveQueue AS
SELECT 
    co.order_id,
    co.token_number,
    cv.vendor_name,
    u.full_name AS student_name,
    co.total_amount,
    co.order_status,
    co.order_timestamp,
    co.pickup_ready_time
FROM Cafeteria_Orders co
JOIN Cafeteria_Vendors cv ON co.vendor_id = cv.vendor_id
JOIN Users u ON co.user_id = u.user_id
WHERE co.order_status IN ('PLACED', 'PREPARING', 'READY_FOR_PICKUP')
ORDER BY co.order_timestamp ASC;

-- 3. Smart Parking Live Occupancy by Block
CREATE OR REPLACE VIEW vw_ParkingOccupancySummary AS
SELECT 
    cb.block_name,
    ps.vehicle_type,
    COUNT(ps.slot_id) AS total_slots,
    SUM(CASE WHEN ps.is_occupied THEN 1 ELSE 0 END) AS occupied_slots,
    SUM(CASE WHEN NOT ps.is_occupied THEN 1 ELSE 0 END) AS available_slots,
    SUM(CASE WHEN ps.is_ev_charging AND NOT ps.is_occupied THEN 1 ELSE 0 END) AS available_ev_bays
FROM Parking_Slots ps
JOIN Campus_Blocks cb ON ps.block_id = cb.block_id
GROUP BY cb.block_name, ps.vehicle_type;

-- 4. Active Grievances SLA Monitor View
CREATE OR REPLACE VIEW vw_ActiveGrievancesSLA AS
SELECT 
    g.ticket_id,
    g.category,
    g.ticket_subject,
    g.priority,
    g.status,
    u_stu.full_name AS reported_by,
    u_staff.full_name AS assigned_to,
    cr.room_number AS location_room,
    g.created_at,
    ROUND(EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - g.created_at)) / 3600, 1) AS hours_open
FROM Grievances g
JOIN Users u_stu ON g.student_id = u_stu.user_id
LEFT JOIN Users u_staff ON g.assigned_to_staff_id = u_staff.user_id
LEFT JOIN Campus_Rooms cr ON g.room_id = cr.room_id
WHERE g.status NOT IN ('RESOLVED', 'CLOSED', 'REJECTED')
ORDER BY 
    CASE g.priority
        WHEN 'URGENT' THEN 1
        WHEN 'HIGH' THEN 2
        WHEN 'MEDIUM' THEN 3
        ELSE 4
    END,
    g.created_at ASC;

-- ============================================================================
-- 13. STORED PROCEDURES (BUSINESS LOGIC WITH ACID TRANSACTIONS)
-- ============================================================================

-- Procedure 1: Record Faculty Biometric / NFC Checkpoint Scan
CREATE OR REPLACE PROCEDURE sp_RecordTeacherBiometricScan(
    p_faculty_id INT,
    p_checkpoint_id INT,
    p_auth_method VARCHAR(30)
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_room_id INT;
    v_checkpoint_type VARCHAR(50);
    v_computed_status VARCHAR(50);
BEGIN
    -- 1. Validate checkpoint and get room details
    SELECT room_id, checkpoint_type 
    INTO v_room_id, v_checkpoint_type 
    FROM Biometric_Checkpoints 
    WHERE checkpoint_id = p_checkpoint_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Checkpoint ID % does not exist.', p_checkpoint_id;
    END IF;

    -- 2. Determine presence status based on scanned checkpoint
    IF v_checkpoint_type = 'STAFF_ROOM_DOOR' THEN
        v_computed_status := 'IN_STAFF_ROOM';
    ELSIF v_checkpoint_type = 'CLASSROOM_PODIUM' THEN
        v_computed_status := 'IN_CLASSROOM';
    ELSIF v_checkpoint_type = 'LAB_ENTRANCE' THEN
        v_computed_status := 'IN_LAB';
    ELSE
        v_computed_status := 'IN_MEETING';
    END IF;

    -- 3. Insert audit log record
    INSERT INTO Teacher_Presence_Logs (faculty_id, checkpoint_id, auth_method, logged_status)
    VALUES (p_faculty_id, p_checkpoint_id, p_auth_method, v_computed_status);

    -- 4. Upsert real-time current status
    INSERT INTO Teacher_Current_Status (faculty_id, current_checkpoint_id, current_room_id, current_status, last_updated_at)
    VALUES (p_faculty_id, p_checkpoint_id, v_room_id, v_computed_status, CURRENT_TIMESTAMP)
    ON CONFLICT (faculty_id) 
    DO UPDATE SET 
        current_checkpoint_id = EXCLUDED.current_checkpoint_id,
        current_room_id = EXCLUDED.current_room_id,
        current_status = EXCLUDED.current_status,
        last_updated_at = CURRENT_TIMESTAMP;

    RAISE NOTICE 'Faculty presence successfully logged as % in Room %', v_computed_status, v_room_id;
END;
$$;

-- Procedure 2: Place Cafeteria Order with Atomic Stock Verification
CREATE OR REPLACE PROCEDURE sp_PlaceCafeteriaOrder(
    p_user_id INT,
    p_vendor_id INT,
    p_item_id INT,
    p_quantity INT,
    INOUT p_order_id INT DEFAULT NULL,
    INOUT p_token_number INT DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_current_stock INT;
    v_item_price NUMERIC(8,2);
    v_total_amt NUMERIC(9,2);
    v_next_token INT;
BEGIN
    -- 1. Lock and verify item inventory to prevent race conditions
    SELECT current_stock_qty, price 
    INTO v_current_stock, v_item_price
    FROM Cafeteria_Items 
    WHERE item_id = p_item_id AND vendor_id = p_vendor_id
    FOR UPDATE;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Item ID % not found for Vendor ID %', p_item_id, p_vendor_id;
    END IF;

    IF v_current_stock < p_quantity THEN
        RAISE EXCEPTION 'Insufficient stock. Available: %, Requested: %', v_current_stock, p_quantity;
    END IF;

    -- 2. Compute total amount & generate token number for today
    v_total_amt := v_item_price * p_quantity;
    
    SELECT COALESCE(MAX(token_number), 100) + 1 
    INTO v_next_token
    FROM Cafeteria_Orders 
    WHERE vendor_id = p_vendor_id 
      AND CAST(order_timestamp AS DATE) = CURRENT_DATE;

    -- 3. Create Order
    INSERT INTO Cafeteria_Orders (user_id, vendor_id, token_number, total_amount, order_status)
    VALUES (p_user_id, p_vendor_id, v_next_token, v_total_amt, 'PLACED')
    RETURNING order_id, token_number INTO p_order_id, p_token_number;

    -- 4. Create Order Item details
    INSERT INTO Cafeteria_Order_Items (order_id, item_id, quantity, unit_price, subtotal)
    VALUES (p_order_id, p_item_id, p_quantity, v_item_price, v_total_amt);

    -- 5. Atomically decrement stock
    UPDATE Cafeteria_Items
    SET current_stock_qty = current_stock_qty - p_quantity
    WHERE item_id = p_item_id;

    RAISE NOTICE 'Order % successfully created. Token: %', p_order_id, p_token_number;
END;
$$;

-- Procedure 3: Lodge and Assign Student Grievance Ticket
CREATE OR REPLACE PROCEDURE sp_LodgeGrievanceTicket(
    p_student_id INT,
    p_category VARCHAR(50),
    p_room_id INT,
    p_subject VARCHAR(150),
    p_description TEXT,
    p_priority VARCHAR(20),
    INOUT p_ticket_id INT DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO Grievances (student_id, category, room_id, ticket_subject, description, priority, status)
    VALUES (p_student_id, p_category, p_room_id, p_subject, p_description, p_priority, 'PENDING')
    RETURNING ticket_id INTO p_ticket_id;

    -- Insert initial audit entry
    INSERT INTO Grievance_Audit_Logs (ticket_id, changed_by_user_id, previous_status, new_status, action_comment)
    VALUES (p_ticket_id, p_student_id, NULL, 'PENDING', 'Grievance ticket lodged by student.');

    RAISE NOTICE 'Grievance ticket #% successfully registered.', p_ticket_id;
END;
$$;

-- ============================================================================
-- 14. TRIGGERS & BUSINESS INTEGRITY RULES
-- ============================================================================

-- Trigger 1: Auto-decrement library available copies upon new circulation issue
CREATE OR REPLACE FUNCTION fn_AfterLibraryBookIssue()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE Library_Books 
        SET available_copies = available_copies - 1
        WHERE book_id = NEW.book_id AND available_copies > 0;
    ELSIF TG_OP = 'UPDATE' AND NEW.circulation_status = 'RETURNED' AND OLD.circulation_status != 'RETURNED' THEN
        UPDATE Library_Books 
        SET available_copies = available_copies + 1
        WHERE book_id = NEW.book_id;
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_ManageLibraryInventory
AFTER INSERT OR UPDATE ON Library_Circulation
FOR EACH ROW
EXECUTE FUNCTION fn_AfterLibraryBookIssue();

-- Trigger 2: Prevent grievance ticket state transition violation (State Machine Rule)
CREATE OR REPLACE FUNCTION fn_EnforceGrievanceWorkflow()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    -- Enforce transition: PENDING -> ASSIGNED -> IN_PROGRESS -> RESOLVED -> CLOSED
    IF OLD.status = 'CLOSED' AND NEW.status != 'CLOSED' THEN
        RAISE EXCEPTION 'A closed ticket cannot be reopened without administrative override.';
    END IF;

    IF NEW.status = 'RESOLVED' AND NEW.resolved_at IS NULL THEN
        NEW.resolved_at := CURRENT_TIMESTAMP;
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_EnforceGrievanceLifecycle
BEFORE UPDATE ON Grievances
FOR EACH ROW
EXECUTE FUNCTION fn_EnforceGrievanceWorkflow();

-- ============================================================================
-- 15. SEED DATA POPULATION (REALISTIC CHRIST BANGALORE DATA)
-- ============================================================================

-- Roles
INSERT INTO Roles (role_name, role_description) VALUES
('ADMIN', 'Super administrator with full ERP database access'),
('FACULTY', 'Teaching faculty member'),
('STUDENT', 'Enrolled university student'),
('VENDOR', 'Cafeteria or store concessionaire staff'),
('MEDIC', 'Campus infirmary nurse/doctor'),
('SECURITY', 'Campus security personnel');

-- Schools & Departments
INSERT INTO Schools (school_name, school_dean) VALUES
('School of Sciences', 'Dr. George Thomas'),
('School of Commerce, Finance and Accountancy', 'Dr. Kavitha R'),
('School of Arts and Humanities', 'Dr. John Joseph'),
('School of Business and Management', 'Dr. Suniti Phadke');

INSERT INTO Departments (school_id, dept_name, hod_name) VALUES
(1, 'Department of Computer Science', 'Dr. Vinay M'),
(1, 'Department of Mathematics & Statistics', 'Dr. Hariharan N'),
(2, 'Department of Professional Studies', 'Dr. Biju Toms'),
(4, 'Department of Management Studies', 'Dr. Georgy P Kurien');

-- Campus Blocks (Bangalore Yeshwanthpur Campus)
INSERT INTO Campus_Blocks (block_code, block_name, total_floors, latitude, longitude) VALUES
('BLK_A', 'Academic Block A', 6, 13.029841, 77.540112),
('BLK_B', 'Academic Block B (Computing Labs)', 7, 13.030115, 77.540455),
('BLK_CENTRAL', 'Central Block (Auditorium & Library)', 8, 13.030520, 77.540780),
('BLK_AMENITY', 'Student Amenities & Food Court', 3, 13.029310, 77.539890);

-- Rooms
INSERT INTO Campus_Rooms (block_id, room_number, floor_number, room_type, seating_capacity) VALUES
(1, 'Room 101', 1, 'CLASSROOM', 60),
(1, 'Room 304', 3, 'STAFF_ROOM', 25),
(2, 'Lab 201 (DBMS Lab)', 2, 'LAB', 65),
(2, 'Lab 305 (AI/ML Lab)', 3, 'LAB', 65),
(3, 'Central Seminar Hall A', 2, 'SEMINAR_HALL', 250),
(3, 'Main University Library', 1, 'LIBRARY', 400),
(4, 'Campus Infirmary (Health Centre)', 1, 'INFIRMARY', 10),
(4, 'Main Cafeteria Food Court', 1, 'CLASSROOM', 300);

-- Users (Admin, Guide Dr Hemanth K S, and Teammates)
INSERT INTO Users (role_id, register_number, full_name, email, password_hash, phone_number) VALUES
(1, 'ADMIN001', 'System Administrator', 'admin@christuniversity.in', '$2b$12$e8Fj1O/75J7kZ8A9G1BqE.7T3fT8U7G9D2H3J4K5L6M7N8O9P0Q1', '9880011223'),
(2, 'FAC1042', 'Dr Hemanth K S', 'hemanth.ks@christuniversity.in', '$2b$12$w0Yq8P/44J9kZ8A9G1BqE.8U4gU9V8H0E3I4K5L6M7N8O9P0Q2', '9845112233'),
(3, '2543115', 'Mayank Raj Gupta', 'mayank.rajgupta@bca.christuniversity.in', '$2b$12$k2Lp9Q/55K0lZ9B0H2CrF.9V5hV0W9I1F4J5L6M7N8O9P0Q3', '9711223344'),
(3, '2543140', 'Sonti Sri Lakshmi Aslesha', 'sonti.aslesha@bca.christuniversity.in', '$2b$12$m3Mq0R/66L1ma0C1I3DsG.0W6iW1X0J2G5K6L7M8N9O0P1Q4', '9722334455'),
(3, '2543163', 'Aadiya Naresh', 'aadiya.naresh@bca.christuniversity.in', '$2b$12$n4Nr1S/77M2nb1D2J4EtH.1X7jX2Y1K3H6L7M8N9O0P1Q5', '9733445566'),
(4, 'VEND101', 'Gourmet Campus Kitchens', 'cafeteria.yeshwanthpur@christuniversity.in', '$2b$12$o5Os2T/88N3oc2E3K5FuI.2Y8kY3Z2L4I7M8N9O0P1Q6', '9900112244'),
(5, 'MEDIC01', 'Sr. Nurse Grace Mathew', 'infirmary@christuniversity.in', '$2b$12$p6Pt3U/99O4pd3F4L6GvJ.3Z9lZ4A3M5J8N9O0P1Q7', '9911223355'),
(6, 'SEC001', 'Chief Officer Ram Singh', 'security.yp@christuniversity.in', '$2b$12$q7Qu4V/00P5qe4G5M7HwK.4A0ma5B4N6K9O0P1Q8', '9922334466');

-- Faculty & Student Details
INSERT INTO Faculties (faculty_id, dept_id, designation, cabin_room_id, office_extension, consultation_hours) VALUES
(2, 1, 'Associate Professor', 2, 'EXT-3042', 'Mon-Thu 03:00 PM - 04:30 PM');

INSERT INTO Students (student_id, dept_id, class_section, semester, batch_year) VALUES
(3, 1, '4BCA-B', 4, '2025-2029'),
(4, 1, '4BCA-B', 4, '2025-2029'),
(5, 1, '4BCA-B', 4, '2025-2029');

-- Biometric Checkpoints
INSERT INTO Biometric_Checkpoints (room_id, checkpoint_name, checkpoint_type, device_hardware_uid, ip_address) VALUES
(2, 'Staff Room 304 Door Scanner', 'STAFF_ROOM_DOOR', 'NFC-HW-304-01', '10.12.34.101'),
(3, 'Lab 201 DBMS Podium Scanner', 'CLASSROOM_PODIUM', 'NFC-HW-201-02', '10.12.34.102'),
(5, 'Central Seminar Hall A Scanner', 'SEMINAR_HALL_DOOR', 'NFC-HW-501-03', '10.12.34.103');

-- Initial Faculty Status
INSERT INTO Teacher_Current_Status (faculty_id, current_checkpoint_id, current_room_id, current_status, custom_status_note) VALUES
(2, 1, 2, 'IN_STAFF_ROOM', 'Available for project consultations');

-- Cafeteria Vendor & Items
INSERT INTO Cafeteria_Vendors (vendor_name, block_id, contact_phone, is_open) VALUES
('Christ Fresh Foods & Bakery', 4, '080-22119900', TRUE);

INSERT INTO Cafeteria_Items (vendor_id, item_name, category, price, is_available, current_stock_qty) VALUES
(1, 'Masala Dosa', 'BREAKFAST', 45.00, TRUE, 80),
(1, 'Cold Coffee', 'BEVERAGES', 35.00, TRUE, 120),
(1, 'Veg Thali Special', 'LUNCH', 80.00, TRUE, 100),
(1, 'Veg Puff', 'SNACKS', 20.00, TRUE, 90);

-- Student Clubs
INSERT INTO Student_Clubs (school_id, club_name, club_tagline, faculty_coordinator_id, president_student_id, founded_year) VALUES
(1, 'HexaGrid Computing Club', 'Innovating Computer Applications', 2, 3, 2024),
(2, 'FinTrade Society', 'Empowering Financial Leadership', 2, 4, 2024);

-- Parking Slots
INSERT INTO Parking_Slots (block_id, slot_code, vehicle_type, is_ev_charging, is_occupied) VALUES
(1, 'P-A-01', 'FOUR_WHEELER', TRUE, FALSE),
(1, 'P-A-02', 'FOUR_WHEELER', FALSE, TRUE),
(2, 'P-B-101', 'TWO_WHEELER', FALSE, FALSE),
(2, 'P-B-102', 'TWO_WHEELER', TRUE, FALSE);

-- Library Categories & Books
INSERT INTO Book_Categories (category_name) VALUES
('Database Systems & SQL'),
('Software Engineering'),
('Artificial Intelligence');

INSERT INTO Library_Books (isbn, title, author, publisher, edition, category_id, total_copies, available_copies, shelf_location) VALUES
('978-0133970777', 'Fundamentals of Database Systems', 'Ramez Elmasri, Shamkant Navathe', 'Pearson', '7th Edition', 1, 10, 8, 'Shelf CS-04-A'),
('978-0078022159', 'Database System Concepts', 'Abraham Silberschatz, Henry F. Korth', 'McGraw-Hill', '7th Edition', 1, 12, 11, 'Shelf CS-04-B');

-- Store Categories & Products
INSERT INTO Store_Categories (category_name) VALUES
('Textbooks & Lab Records'),
('University Stationery'),
('CHRIST Branded Merchandise');

INSERT INTO Store_Inventory (category_id, product_code, product_name, unit_price, stock_quantity) VALUES
(1, 'BCA-REC-4', '4BCA Practical Lab Observation Record Book', 75.00, 250),
(3, 'CH-HOODIE-M', 'Official CHRIST University Hoodie (Medium)', 850.00, 45);

-- Sample Grievance
INSERT INTO Grievances (student_id, category, room_id, ticket_subject, description, priority, status) VALUES
(3, 'CAMPUS_WIFI', 3, 'Weak Wi-Fi signal at Lab 201 DBMS workstations', 'Signal fluctuates during practical lab exercises.', 'HIGH', 'IN_PROGRESS');

-- Verification commit message
-- ============================================================================
-- END OF UNICHRIST DBMS DDL & POPULATION SCRIPT
-- ============================================================================
