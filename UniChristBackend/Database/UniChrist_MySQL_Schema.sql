-- ============================================================================
-- DATABASE MANAGEMENT SYSTEMS PROJECT (BCA381-4)
-- CHRIST (Deemed to be University) - Bangalore Yeshwanthpur Campus
-- Department of Computer Science | Academic Year: 2025-2026
--
-- PROJECT TITLE: UniChrist - Integrated Smart Campus ERP & Location Services
-- BACKEND DATABASE SCRIPT FOR MYSQL 8.0+ / MARIADB
-- ============================================================================

CREATE DATABASE IF NOT EXISTS unichrist_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE unichrist_db;

-- Disable foreign key checks for clean recreation
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS grievance_audit_logs;
DROP TABLE IF EXISTS grievances;
DROP TABLE IF EXISTS parking_logs;
DROP TABLE IF EXISTS parking_slots;
DROP TABLE IF EXISTS library_books;
DROP TABLE IF EXISTS book_categories;
DROP TABLE IF EXISTS cafeteria_order_items;
DROP TABLE IF EXISTS cafeteria_orders;
DROP TABLE IF EXISTS cafeteria_items;
DROP TABLE IF EXISTS cafeteria_vendors;
DROP TABLE IF EXISTS faculty_status_overrides;
DROP TABLE IF EXISTS faculty_timetables;
DROP TABLE IF EXISTS faculties;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS campus_rooms;
DROP TABLE IF EXISTS campus_blocks;
DROP TABLE IF EXISTS departments;
DROP TABLE IF EXISTS schools;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS roles;

SET FOREIGN_KEY_CHECKS = 1;

-- 1. CORE AUTHENTICATION & CAMPUS ENTITIES
CREATE TABLE roles (
    role_id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL UNIQUE,
    role_description VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    role_id INT NOT NULL,
    register_number VARCHAR(50) NOT NULL UNIQUE,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE schools (
    school_id INT AUTO_INCREMENT PRIMARY KEY,
    school_name VARCHAR(100) NOT NULL UNIQUE,
    school_dean VARCHAR(120)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE departments (
    dept_id INT AUTO_INCREMENT PRIMARY KEY,
    school_id INT NOT NULL,
    dept_name VARCHAR(100) NOT NULL UNIQUE,
    hod_name VARCHAR(120),
    FOREIGN KEY (school_id) REFERENCES schools(school_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE campus_blocks (
    block_id INT AUTO_INCREMENT PRIMARY KEY,
    block_code VARCHAR(20) NOT NULL UNIQUE,
    block_name VARCHAR(100) NOT NULL,
    total_floors INT NOT NULL,
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE campus_rooms (
    room_id INT AUTO_INCREMENT PRIMARY KEY,
    block_id INT NOT NULL,
    room_number VARCHAR(30) NOT NULL,
    floor_number INT NOT NULL,
    room_type VARCHAR(50) NOT NULL,
    seating_capacity INT DEFAULT 60,
    is_active BOOLEAN DEFAULT TRUE,
    UNIQUE KEY uq_block_room (block_id, room_number),
    FOREIGN KEY (block_id) REFERENCES campus_blocks(block_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE students (
    student_id INT PRIMARY KEY,
    dept_id INT NOT NULL,
    class_section VARCHAR(20) NOT NULL,
    semester INT NOT NULL,
    batch_year VARCHAR(20) NOT NULL,
    FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE faculties (
    faculty_id INT PRIMARY KEY,
    dept_id INT NOT NULL,
    designation VARCHAR(80) NOT NULL,
    cabin_room_id INT,
    office_extension VARCHAR(20),
    consultation_hours VARCHAR(100),
    FOREIGN KEY (faculty_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id) ON DELETE RESTRICT,
    FOREIGN KEY (cabin_room_id) REFERENCES campus_rooms(room_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. TIMETABLE & LOCATION ENGINE
CREATE TABLE faculty_timetables (
    schedule_id INT AUTO_INCREMENT PRIMARY KEY,
    faculty_id INT NOT NULL,
    day_of_week VARCHAR(15) NOT NULL,
    period_number INT NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    room_id INT NOT NULL,
    course_code VARCHAR(30) NOT NULL,
    course_name VARCHAR(120) NOT NULL,
    class_section VARCHAR(20) NOT NULL,
    FOREIGN KEY (faculty_id) REFERENCES faculties(faculty_id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES campus_rooms(room_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE faculty_status_overrides (
    override_id INT AUTO_INCREMENT PRIMARY KEY,
    faculty_id INT NOT NULL,
    override_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    status_type VARCHAR(50) NOT NULL,
    assigned_room_id INT,
    notes VARCHAR(255),
    FOREIGN KEY (faculty_id) REFERENCES faculties(faculty_id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_room_id) REFERENCES campus_rooms(room_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. CAFETERIA MODULE
CREATE TABLE cafeteria_vendors (
    vendor_id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_name VARCHAR(100) NOT NULL,
    block_id INT NOT NULL,
    contact_phone VARCHAR(20),
    is_open BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (block_id) REFERENCES campus_blocks(block_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE cafeteria_items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id INT NOT NULL,
    item_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price DECIMAL(8,2) NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,
    current_stock_qty INT NOT NULL DEFAULT 50,
    FOREIGN KEY (vendor_id) REFERENCES cafeteria_vendors(vendor_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE cafeteria_orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    vendor_id INT NOT NULL,
    order_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    token_number INT NOT NULL,
    total_amount DECIMAL(9,2) NOT NULL,
    payment_mode VARCHAR(30) DEFAULT 'CAMPUS_DIGITAL_WALLET',
    order_status VARCHAR(30) DEFAULT 'PLACED',
    pickup_ready_time DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT,
    FOREIGN KEY (vendor_id) REFERENCES cafeteria_vendors(vendor_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE cafeteria_order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(8,2) NOT NULL,
    subtotal DECIMAL(9,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES cafeteria_orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES cafeteria_items(item_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. SMART PARKING
CREATE TABLE parking_slots (
    slot_id INT AUTO_INCREMENT PRIMARY KEY,
    block_id INT NOT NULL,
    slot_code VARCHAR(20) NOT NULL UNIQUE,
    vehicle_type VARCHAR(20) NOT NULL,
    is_ev_charging BOOLEAN DEFAULT FALSE,
    is_occupied BOOLEAN DEFAULT FALSE,
    assigned_vehicle_reg VARCHAR(30),
    FOREIGN KEY (block_id) REFERENCES campus_blocks(block_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE parking_logs (
    log_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    slot_id INT NOT NULL,
    user_id INT,
    vehicle_reg_number VARCHAR(30) NOT NULL,
    entry_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    exit_timestamp DATETIME,
    FOREIGN KEY (slot_id) REFERENCES parking_slots(slot_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. GRIEVANCE REDRESSAL
CREATE TABLE grievances (
    ticket_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    category VARCHAR(50) NOT NULL,
    room_id INT,
    ticket_subject VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    priority VARCHAR(20) DEFAULT 'MEDIUM',
    status VARCHAR(30) DEFAULT 'PENDING',
    assigned_to_staff_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    resolved_at DATETIME,
    resolution_notes TEXT,
    FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE RESTRICT,
    FOREIGN KEY (room_id) REFERENCES campus_rooms(room_id) ON DELETE SET NULL,
    FOREIGN KEY (assigned_to_staff_id) REFERENCES users(user_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE grievance_audit_logs (
    log_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    ticket_id INT NOT NULL,
    changed_by_user_id INT NOT NULL,
    previous_status VARCHAR(30),
    new_status VARCHAR(30) NOT NULL,
    action_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    action_comment TEXT,
    FOREIGN KEY (ticket_id) REFERENCES grievances(ticket_id) ON DELETE CASCADE,
    FOREIGN KEY (changed_by_user_id) REFERENCES users(user_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6. LIBRARY MODULE
CREATE TABLE book_categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE library_books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    isbn VARCHAR(20) NOT NULL UNIQUE,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(150) NOT NULL,
    publisher VARCHAR(120),
    edition VARCHAR(30),
    category_id INT NOT NULL,
    total_copies INT NOT NULL DEFAULT 1,
    available_copies INT NOT NULL DEFAULT 1,
    shelf_location VARCHAR(50),
    FOREIGN KEY (category_id) REFERENCES book_categories(category_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================================
-- INITIAL DATA SEEDING (CORRESPONDING TO SRS & GUIDE RECOMMENDATIONS)
-- ============================================================================

INSERT INTO roles (role_id, role_name, role_description) VALUES
(1, 'ADMIN', 'System Administrator'),
(2, 'FACULTY', 'Academic Teaching Faculty'),
(3, 'STUDENT', 'Enrolled Student'),
(4, 'STAFF', 'Campus Facility Staff');

INSERT INTO schools (school_id, school_name, school_dean) VALUES
(1, 'School of Sciences', 'Dr George Thomas');

INSERT INTO departments (dept_id, school_id, dept_name, hod_name) VALUES
(1, 1, 'Department of Computer Science', 'Dr Vinay M');

INSERT INTO campus_blocks (block_id, block_code, block_name, total_floors, latitude, longitude) VALUES
(1, 'BLK-A', 'Block A (Main Academic & Administrative Block)', 5, 13.031200, 77.545100),
(2, 'BLK-B', 'Block B (Computing Labs & Research Center)', 4, 13.031800, 77.545600);

INSERT INTO campus_rooms (room_id, block_id, room_number, floor_number, room_type, seating_capacity) VALUES
(1, 1, 'Staff Room 304', 3, 'STAFF_ROOM', 15),
(2, 2, 'Lab 201 (DBMS Lab)', 2, 'LAB', 60),
(3, 1, 'Conference Room 102', 1, 'SEMINAR_HALL', 40),
(4, 1, 'Room 405 (Classroom)', 4, 'CLASSROOM', 75);

INSERT INTO users (user_id, role_id, register_number, full_name, email, password_hash, phone_number) VALUES
(1, 3, '2543115', 'Mayank Raj Gupta', 'mayank.raj@christuniversity.in', 'Password@123', '+91 9876543210'),
(2, 3, '2543140', 'Sonti Sri Lakshmi Aslesha', 'aslesha.sonti@christuniversity.in', 'Password@123', '+91 9876543211'),
(3, 2, 'EMP-CS-101', 'Dr Hemanth K S', 'hemanth.ks@christuniversity.in', 'Password@123', '+91 9123456780'),
(4, 2, 'EMP-CS-102', 'Dr Deepa B G', 'deepa.bg@christuniversity.in', 'Password@123', '+91 9123456781'),
(5, 2, 'EMP-CS-100', 'Dr Vinay M', 'vinay.m@christuniversity.in', 'Password@123', '+91 9123456782');

INSERT INTO students (student_id, dept_id, class_section, semester, batch_year) VALUES
(1, 1, '4BCA-B', 4, '2025-2029'),
(2, 1, '4BCA-B', 4, '2025-2029');

INSERT INTO faculties (faculty_id, dept_id, designation, cabin_room_id, office_extension, consultation_hours) VALUES
(3, 1, 'Associate Professor & DBMS Project Guide', 1, '4102', 'Mon-Thu 03:00 PM - 04:30 PM'),
(4, 1, 'Associate Professor', 1, '4105', 'Wed-Fri 02:00 PM - 03:30 PM'),
(5, 1, 'Head of Department (HOD)', 3, '4100', 'Mon-Fri 11:00 AM - 01:00 PM');

INSERT INTO faculty_timetables (faculty_id, day_of_week, period_number, start_time, end_time, room_id, course_code, course_name, class_section) VALUES
(3, 'MONDAY', 2, '09:45:00', '10:45:00', 4, 'BCA302', 'Relational Database Management Systems', '4BCA-B'),
(3, 'MONDAY', 4, '11:45:00', '13:15:00', 2, 'BCA381', 'DBMS Project Lab', '4BCA-B'),
(4, 'MONDAY', 3, '10:45:00', '11:45:00', 2, 'BCA382', 'Advanced Data Structures Lab', '4BCA-A');

INSERT INTO cafeteria_vendors (vendor_id, vendor_name, block_id, contact_phone, is_open) VALUES
(1, 'Christ Central Cafeteria (South & North Kitchen)', 1, '+91 80 4012 9000', 1),
(2, 'Campus Brew & Bakery Desk', 2, '+91 80 4012 9005', 1);

INSERT INTO cafeteria_items (item_id, vendor_id, item_name, category, price, is_available, current_stock_qty) VALUES
(1, 1, 'Masala Dosa with Sambar & Chutney', 'BREAKFAST', 45.00, 1, 60),
(2, 1, 'South Indian Thali Meal', 'LUNCH', 70.00, 1, 120),
(3, 1, 'Paneer Butter Masala Combo', 'LUNCH', 90.00, 1, 40),
(4, 2, 'Cappuccino (Filter Blend)', 'BEVERAGES', 25.00, 1, 200),
(5, 2, 'Grilled Veggie & Cheese Sandwich', 'SNACKS', 50.00, 1, 35);

INSERT INTO parking_slots (slot_id, block_id, slot_code, vehicle_type, is_ev_charging, is_occupied, assigned_vehicle_reg) VALUES
(1, 1, 'A-TW-01', 'TWO_WHEELER', 0, 0, NULL),
(2, 1, 'A-EV-02', 'TWO_WHEELER', 1, 1, 'KA-04-MB-4512'),
(3, 2, 'B-FW-10', 'FOUR_WHEELER', 0, 0, NULL),
(4, 2, 'B-EV-11', 'FOUR_WHEELER', 1, 0, NULL);

INSERT INTO book_categories (category_id, category_name) VALUES
(1, 'Computer Science & Database Engineering');

INSERT INTO library_books (book_id, isbn, title, author, publisher, edition, category_id, total_copies, available_copies, shelf_location) VALUES
(1, '978-0133970777', 'Fundamentals of Database Systems (7th Edition)', 'Ramez Elmasri, Shamkant B. Navathe', 'Pearson', '7th', 1, 10, 7, 'Stack 3, Shelf B2'),
(2, '978-0078022159', 'Database System Concepts', 'Abraham Silberschatz, Henry F. Korth, S. Sudarshan', 'McGraw-Hill', '6th', 1, 12, 9, 'Stack 3, Shelf B3');

