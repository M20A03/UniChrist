-- ============================================================================
-- DATABASE MANAGEMENT SYSTEMS PROJECT (BCA381-4)
-- CHRIST (Deemed to be University) - Bangalore Yeshwanthpur Campus
-- Department of Computer Science | Academic Year: 2025-2026
--
-- PROJECT TITLE: UniChrist - Integrated Smart Campus ERP & Location Services
-- ADVANCED DATABASE OBJECTS: STORED PROCEDURES, TRIGGERS & ANALYTICAL VIEWS
-- For Evaluation: Dr Hemanth K S (Guide)
-- Team: Mayank Raj Gupta (2543115), Sonti Sri Lakshmi Aslesha (2543140), Aadiya Naresh (2543163)
-- ============================================================================

USE unichrist_db;

-- ============================================================================
-- 1. ANALYTICAL & REPORTING VIEWS
-- ============================================================================

-- View 1: Live Faculty Location & Consultation Status View
CREATE OR REPLACE VIEW vw_LiveFacultyLocations AS
SELECT 
    f.faculty_id,
    u.full_name AS faculty_name,
    u.email AS faculty_email,
    f.designation,
    d.dept_name,
    cb.block_name AS cabin_block,
    cr.room_number AS cabin_room,
    f.consultation_hours,
    COALESCE(ov.status_type, 
             CASE 
                WHEN tt.schedule_id IS NOT NULL THEN 'IN_CLASS'
                ELSE 'AVAILABLE'
             END) AS current_status,
    COALESCE(ov.notes,
             CASE 
                WHEN tt.schedule_id IS NOT NULL THEN CONCAT('In Lecture: ', tt.course_code, ' (', tt_room.room_number, ')')
                ELSE CONCAT('Available in Cabin: ', cr.room_number)
             END) AS location_details
FROM faculties f
JOIN users u ON f.faculty_id = u.user_id
JOIN departments d ON f.dept_id = d.dept_id
LEFT JOIN campus_rooms cr ON f.cabin_room_id = cr.room_id
LEFT JOIN campus_blocks cb ON cr.block_id = cb.block_id
LEFT JOIN faculty_status_overrides ov ON f.faculty_id = ov.faculty_id 
    AND ov.override_date = CURRENT_DATE 
    AND CURRENT_TIME BETWEEN ov.start_time AND ov.end_time
LEFT JOIN faculty_timetables tt ON f.faculty_id = tt.faculty_id
    AND tt.day_of_week = UPPER(DAYNAME(CURRENT_DATE))
    AND CURRENT_TIME BETWEEN tt.start_time AND tt.end_time
LEFT JOIN campus_rooms tt_room ON tt.room_id = tt_room.room_id;

-- View 2: Cafeteria Daily Revenue and Vendor Sales Summary
CREATE OR REPLACE VIEW vw_CafeteriaDailySalesReport AS
SELECT 
    v.vendor_id,
    v.vendor_name,
    b.block_name,
    DATE(o.order_timestamp) AS sales_date,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(o.total_amount) AS gross_revenue_inr,
    AVG(o.total_amount) AS average_order_value_inr
FROM cafeteria_vendors v
JOIN campus_blocks b ON v.block_id = b.block_id
LEFT JOIN cafeteria_orders o ON v.vendor_id = o.vendor_id AND o.order_status != 'CANCELLED'
GROUP BY v.vendor_id, v.vendor_name, b.block_name, DATE(o.order_timestamp);

-- View 3: Grievance Resolution SLA and Category Performance
CREATE OR REPLACE VIEW vw_GrievanceSLAReport AS
SELECT 
    g.category,
    COUNT(g.ticket_id) AS total_tickets,
    SUM(CASE WHEN g.status = 'PENDING' THEN 1 ELSE 0 END) AS pending_tickets,
    SUM(CASE WHEN g.status = 'IN_PROGRESS' THEN 1 ELSE 0 END) AS in_progress_tickets,
    SUM(CASE WHEN g.status = 'RESOLVED' THEN 1 ELSE 0 END) AS resolved_tickets,
    ROUND(SUM(CASE WHEN g.status = 'RESOLVED' THEN 1 ELSE 0 END) * 100.0 / COUNT(g.ticket_id), 2) AS resolution_rate_percentage
FROM grievances g
GROUP BY g.category;

-- View 4: Real-time Parking Block Occupancy Overview
CREATE OR REPLACE VIEW vw_ParkingOccupancySummary AS
SELECT 
    b.block_code,
    b.block_name,
    COUNT(p.slot_id) AS total_slots,
    SUM(CASE WHEN p.is_occupied = 1 THEN 1 ELSE 0 END) AS occupied_slots,
    SUM(CASE WHEN p.is_occupied = 0 THEN 1 ELSE 0 END) AS vacant_slots,
    SUM(CASE WHEN p.is_ev_charging = 1 THEN 1 ELSE 0 END) AS ev_charging_slots,
    ROUND((SUM(CASE WHEN p.is_occupied = 1 THEN 1 ELSE 0 END) * 100.0) / COUNT(p.slot_id), 1) AS occupancy_percentage
FROM campus_blocks b
JOIN parking_slots p ON b.block_id = p.block_id
GROUP BY b.block_code, b.block_name;

-- ============================================================================
-- 2. DATABASE TRIGGERS
-- ============================================================================

DELIMITER $$

-- Trigger 1: Auto-generate Audit Trail on Grievance Status Change
DROP TRIGGER IF EXISTS trg_GrievanceAudit_AfterUpdate$$
CREATE TRIGGER trg_GrievanceAudit_AfterUpdate
AFTER UPDATE ON grievances
FOR EACH ROW
BEGIN
    IF OLD.status != NEW.status THEN
        INSERT INTO grievance_audit_logs (
            ticket_id, 
            changed_by_user_id, 
            previous_status, 
            new_status, 
            action_timestamp, 
            action_comment
        ) VALUES (
            NEW.ticket_id,
            COALESCE(NEW.assigned_to_staff_id, NEW.student_id),
            OLD.status,
            NEW.status,
            NOW(),
            CONCAT('Status updated automatically from ', OLD.status, ' to ', NEW.status)
        );
    END IF;
END$$

-- Trigger 2: Prevent placing orders with quantity greater than available stock
DROP TRIGGER IF EXISTS trg_ValidateOrderItemStock_BeforeInsert$$
CREATE TRIGGER trg_ValidateOrderItemStock_BeforeInsert
BEFORE INSERT ON cafeteria_order_items
FOR EACH ROW
BEGIN
    DECLARE v_available_stock INT;
    DECLARE v_item_name VARCHAR(100);

    SELECT current_stock_qty, item_name 
    INTO v_available_stock, v_item_name
    FROM cafeteria_items 
    WHERE item_id = NEW.item_id;

    IF v_available_stock < NEW.quantity THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Requested quantity exceeds available cafeteria stock.';
    END IF;
END$$

-- ============================================================================
-- 3. TRANSACTION-SAFE STORED PROCEDURES (ACID COMPLIANCE)
-- ============================================================================

-- Stored Procedure 1: Atomic Cafeteria Pre-Order Creation with Token Generation
DROP PROCEDURE IF EXISTS sp_PlaceCafeteriaOrder$$
CREATE PROCEDURE sp_PlaceCafeteriaOrder (
    IN p_user_id INT,
    IN p_vendor_id INT,
    IN p_item_id INT,
    IN p_quantity INT,
    IN p_payment_mode VARCHAR(30),
    OUT p_order_id INT,
    OUT p_token_number INT,
    OUT p_total_amount DECIMAL(9,2)
)
proc_label: BEGIN
    DECLARE v_item_price DECIMAL(8,2);
    DECLARE v_stock INT;
    DECLARE v_subtotal DECIMAL(9,2);
    DECLARE v_today_orders INT;

    -- Error handler to rollback transaction on any SQL error
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    -- 1. Check stock and price
    SELECT price, current_stock_qty INTO v_item_price, v_stock
    FROM cafeteria_items
    WHERE item_id = p_item_id AND is_available = 1
    FOR UPDATE;

    IF v_stock IS NULL OR v_stock < p_quantity THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Selected item is out of stock or unavailable.';
    END IF;

    -- 2. Calculate subtotal & generate daily cycling token (101 - 999)
    SET v_subtotal = v_item_price * p_quantity;
    SET p_total_amount = v_subtotal;

    SELECT COUNT(*) INTO v_today_orders
    FROM cafeteria_orders
    WHERE DATE(order_timestamp) = CURRENT_DATE;

    SET p_token_number = 100 + (v_today_orders % 900) + 1;

    -- 3. Insert Cafeteria Order Header
    INSERT INTO cafeteria_orders (
        user_id, vendor_id, order_timestamp, token_number, total_amount, payment_mode, order_status
    ) VALUES (
        p_user_id, p_vendor_id, NOW(), p_token_number, v_subtotal, p_payment_mode, 'PLACED'
    );

    SET p_order_id = LAST_INSERT_ID();

    -- 4. Insert Order Item Detail
    INSERT INTO cafeteria_order_items (
        order_id, item_id, quantity, unit_price, subtotal
    ) VALUES (
        p_order_id, p_item_id, p_quantity, v_item_price, v_subtotal
    );

    -- 5. Decrement Item Stock Inventory
    UPDATE cafeteria_items
    SET current_stock_qty = current_stock_qty - p_quantity
    WHERE item_id = p_item_id;

    COMMIT;
END$$

-- Stored Procedure 2: Atomic Parking Slot Occupancy Sensor Toggle
DROP PROCEDURE IF EXISTS sp_ToggleParkingSlot$$
CREATE PROCEDURE sp_ToggleParkingSlot (
    IN p_slot_id INT,
    IN p_is_occupied BOOLEAN,
    IN p_vehicle_reg VARCHAR(30),
    IN p_user_id INT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    IF p_is_occupied = 1 THEN
        -- Slot marked occupied: update slot and insert parking entry log
        UPDATE parking_slots
        SET is_occupied = 1,
            assigned_vehicle_reg = p_vehicle_reg
        WHERE slot_id = p_slot_id;

        INSERT INTO parking_logs (slot_id, user_id, vehicle_reg_number, entry_timestamp)
        VALUES (p_slot_id, p_user_id, p_vehicle_reg, NOW());
    ELSE
        -- Slot released: update slot and close active parking log
        UPDATE parking_slots
        SET is_occupied = 0,
            assigned_vehicle_reg = NULL
        WHERE slot_id = p_slot_id;

        UPDATE parking_logs
        SET exit_timestamp = NOW()
        WHERE slot_id = p_slot_id AND exit_timestamp IS NULL
        ORDER BY entry_timestamp DESC
        LIMIT 1;
    END IF;

    COMMIT;
END$$

DELIMITER ;

