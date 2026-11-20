#!/usr/bin/env python3
"""
Generate 3 separate high-resolution, full-page ER Diagram images designed specifically
for high-clarity physical hardcopy printing (A4 / Letter paper).

Part 1: Core Academic & Spatial Hierarchy (Modules 0, 9, 12, 10, 11 — 13 Entities)
Part 2: Campus Commercial & Welfare Services (Modules 1, 2, 3, 4 — 12 Entities)
Part 3: Campus Logistics, Library & Student Life (Modules 5, 6, 7, 8 + Legend — 9 Entities)

All cards have large, bold, crystal-clear typography, pill badges, and distinct relationship connectors.
"""

import os
from PIL import Image, ImageDraw, ImageFont

def get_fonts():
    font_bold = '/usr/share/fonts/google-carlito-fonts/Carlito-Bold.ttf'
    font_reg = '/usr/share/fonts/google-carlito-fonts/Carlito-Regular.ttf'
    font_mono = '/usr/share/fonts/adwaita-mono-fonts/AdwaitaMono-Regular.ttf'
    
    return {
        'title': ImageFont.truetype(font_bold, 36),
        'sub': ImageFont.truetype(font_reg, 20),
        'meta': ImageFont.truetype(font_bold, 17),
        'frame_title': ImageFont.truetype(font_bold, 20),
        'frame_sub': ImageFont.truetype(font_reg, 16),
        'card_hdr': ImageFont.truetype(font_bold, 20),
        'pill': ImageFont.truetype(font_bold, 14),
        'attr': ImageFont.truetype(font_mono, 17),
        'rel': ImageFont.truetype(font_bold, 15),
        'legend_hdr': ImageFont.truetype(font_bold, 18),
        'legend_txt': ImageFont.truetype(font_reg, 16)
    }

def draw_module_frame(draw, fonts, x, y, w, h, title, sub, pill_color):
    draw.rounded_rectangle([x, y, x+w, y+h], radius=12, fill='#FFFFFF', outline='#94A3B8', width=3)
    tw = len(title) * 12 + 30
    draw.rounded_rectangle([x+20, y+14, x+20+tw, y+46], radius=6, fill=pill_color)
    draw.text((x+32, y+30), title, font=fonts['frame_title'], fill='#FFFFFF', anchor='lm')
    draw.text((x+32+tw+16, y+30), sub, font=fonts['frame_sub'], fill='#475569', anchor='lm')

def draw_card(draw, fonts, x, y, w, title, attrs, hdr_color):
    hh = 42
    rh = 30
    bh = len(attrs) * rh + 16
    th = hh + bh
    
    # Drop shadow effect
    draw.rounded_rectangle([x+3, y+3, x+w+3, y+th+3], radius=8, fill='#E2E8F0')
    # Card Body
    draw.rounded_rectangle([x, y, x+w, y+th], radius=8, fill='#FFFFFF', outline='#94A3B8', width=2)
    # Header
    draw.rounded_rectangle([x, y, x+w, y+hh], radius=8, fill=hdr_color)
    draw.text((x + w/2, y + 21), title, font=fonts['card_hdr'], fill='#FFFFFF', anchor='mm')
    
    # Attributes
    cy = y + hh + 20
    for atype, aname in attrs:
        if 'PK,FK' in atype or 'PK/FK' in atype:
            draw.rounded_rectangle([x+10, cy-13, x+65, cy+11], radius=4, fill='#F3E8FF', outline='#A855F7', width=2)
            draw.text((x+37, cy-1), 'PK,FK', font=fonts['pill'], fill='#7E22CE', anchor='mm')
            draw.text((x+75, cy-1), aname, font=fonts['attr'], fill='#7E22CE', anchor='lm')
        elif 'PK' in atype:
            draw.rounded_rectangle([x+10, cy-13, x+48, cy+11], radius=4, fill='#FEF3C7', outline='#F59E0B', width=2)
            draw.text((x+29, cy-1), 'PK', font=fonts['pill'], fill='#B45309', anchor='mm')
            draw.text((x+58, cy-1), aname, font=fonts['attr'], fill='#B45309', anchor='lm')
        elif 'FK' in atype:
            draw.rounded_rectangle([x+10, cy-13, x+48, cy+11], radius=4, fill='#DBEAFE', outline='#3B82F6', width=2)
            draw.text((x+29, cy-1), 'FK', font=fonts['pill'], fill='#1D4ED8', anchor='mm')
            draw.text((x+58, cy-1), aname, font=fonts['attr'], fill='#1D4ED8', anchor='lm')
        else:
            draw.text((x+25, cy-1), aname, font=fonts['attr'], fill='#1E293B', anchor='lm')
        cy += rh
    return th

def draw_rel(draw, fonts, x1, y1, x2, y2, card, mx, my):
    draw.line([x1, y1, x2, y2], fill='#475569', width=3)
    points = [(mx, my-14), (mx+18, my), (mx, my+14), (mx-18, my)]
    draw.polygon(points, fill='#FFFFFF', outline='#1D4ED8', width=2)
    draw.text((mx, my), card, font=fonts['rel'], fill='#0F172A', anchor='mm')

# =============================================================================
# PART 1: CORE ACADEMIC & SPATIAL ENGINE
# =============================================================================
def generate_erd_part1():
    W, H = 2400, 3000
    im = Image.new('RGB', (W, H), color='#F8FAFC')
    draw = ImageDraw.Draw(im)
    f = get_fonts()

    # Top Banner
    draw.rounded_rectangle([30, 20, 2370, 135], radius=12, fill='#FFFFFF', outline='#CBD5E1', width=3)
    draw.text((1200, 48), 'UniChrist : Relational ER Diagram — Part 1 of 3', font=f['title'], fill='#0F172A', anchor='mm')
    draw.text((1200, 84), 'Core Academic Hierarchy, Spatial Directory, Faculty Timetables & Grievance Vault', font=f['sub'], fill='#475569', anchor='mm')
    draw.text((1200, 112), 'Modules 0, 9, 12, 10 & 11 • Fully Normalized to BCNF • Hardcopy Print Quality Edition', font=f['meta'], fill='#2563EB', anchor='mm')

    # Frame 1: Module 0 (Core Demographics & RBAC)
    draw_module_frame(draw, f, 30, 155, 2340, 1120, "MODULE 0: CORE DEMOGRAPHICS, AUTHENTICATION & ACADEMIC HIERARCHY", "RBAC roles, master user accounts, schools, departments, student and faculty subtypes", "#1D4ED8")
    draw_card(draw, f, 60, 225, 340, "Roles", [("PK", "role_id (INT)"), ("REG", "role_name (VARCHAR) UQ"), ("REG", "role_desc (VARCHAR)")], "#1E40AF")
    draw_card(draw, f, 440, 225, 420, "Users", [("PK", "user_id (INT)"), ("FK", "role_id (INT)"), ("REG", "register_number (UQ)"), ("REG", "full_name (VARCHAR)"), ("REG", "email (VARCHAR) UQ"), ("REG", "password_hash (VARCHAR)"), ("REG", "is_active (BOOLEAN)")], "#1E40AF")
    draw_card(draw, f, 900, 225, 400, "Schools", [("PK", "school_id (INT)"), ("REG", "school_name (VARCHAR) UQ"), ("REG", "school_dean (VARCHAR)")], "#1E40AF")
    draw_card(draw, f, 1340, 225, 440, "Departments", [("PK", "dept_id (INT)"), ("FK", "school_id (INT)"), ("REG", "dept_name (VARCHAR) UQ"), ("REG", "hod_name (VARCHAR)")], "#1E40AF")
    draw_card(draw, f, 1820, 225, 520, "Academic_Resources", [("PK", "resource_id (INT)"), ("FK", "dept_id (INT)"), ("FK", "uploaded_by_faculty_id (INT)"), ("REG", "resource_type (CHECK)"), ("REG", "course_code (VARCHAR)"), ("REG", "document_title (VARCHAR)"), ("REG", "download_count (INT)")], "#334155")

    # Subtypes
    draw_card(draw, f, 240, 640, 520, "Students", [("PK,FK", "student_id (INT -> Users)"), ("FK", "dept_id (INT -> Depts)"), ("REG", "class_section (VARCHAR)"), ("REG", "semester (INT 1-8)"), ("REG", "batch_year (INT >= 2020)")], "#2563EB")
    draw_card(draw, f, 840, 640, 540, "Faculties", [("PK,FK", "faculty_id (INT -> Users)"), ("FK", "dept_id (INT -> Depts)"), ("REG", "designation (VARCHAR)"), ("FK", "cabin_room_id (INT -> Rooms)"), ("REG", "office_extension (VARCHAR)")], "#2563EB")
    draw_card(draw, f, 1460, 640, 480, "Grievances", [("PK", "ticket_id (INT)"), ("FK", "student_id (INT -> Users)"), ("REG", "category (CHECK)"), ("FK", "room_id (INT -> Rooms)"), ("REG", "ticket_subject (VARCHAR)"), ("REG", "priority (CHECK)"), ("REG", "status (CHECK)")], "#B91C1C")
    draw_card(draw, f, 1460, 960, 480, "Grievance_Audit_Logs", [("PK", "log_id (INT)"), ("FK", "ticket_id (INT -> Grievances)"), ("FK", "changed_by_user_id (INT -> Users)"), ("REG", "previous_status (CHECK)"), ("REG", "new_status (CHECK)"), ("REG", "action_timestamp (TIMESTAMP)")], "#B91C1C")

    # Connectors Frame 1
    draw_rel(draw, f, 400, 280, 440, 280, "1:N", 420, 280)
    draw_rel(draw, f, 1300, 280, 1340, 280, "1:N", 1320, 280)
    draw_rel(draw, f, 560, 500, 420, 640, "1:1", 490, 570)
    draw_rel(draw, f, 720, 500, 980, 640, "1:1", 850, 570)
    draw_rel(draw, f, 1700, 860, 1700, 960, "1:N", 1700, 910)

    # Frame 2: Modules 9 & 12 (Spatial Directory & Automated Timetable Engine)
    draw_module_frame(draw, f, 30, 1310, 2340, 1550, "MODULES 9 & 12: SPATIAL DIRECTORY & AUTOMATED FACULTY SCHEDULE ENGINE", "Multi-floor campus blocks, room geometry, timetable period lookups, and dynamic cabin resolution", "#6D28D9")
    draw_card(draw, f, 60, 1390, 480, "Campus_Blocks", [("PK", "block_id (INT)"), ("REG", "block_code (VARCHAR) UQ"), ("REG", "block_name (VARCHAR)"), ("REG", "total_floors (INT > 0)"), ("REG", "latitude (NUMERIC)"), ("REG", "longitude (NUMERIC)")], "#059669")
    draw_card(draw, f, 620, 1390, 540, "Campus_Rooms", [("PK", "room_id (INT)"), ("FK", "block_id (INT -> Blocks)"), ("REG", "room_number (VARCHAR)"), ("REG", "floor_number (INT >= 0)"), ("REG", "room_type (CHECK)"), ("REG", "seating_capacity (INT >= 0)")], "#059669")
    draw_card(draw, f, 1260, 1390, 600, "Faculty_Timetables", [("PK", "schedule_id (INT)"), ("FK", "faculty_id (INT -> Faculties)"), ("REG", "day_of_week (CHECK MONDAY-SAT)"), ("REG", "period_number (INT 1-8)"), ("REG", "start_time (TIME) / end_time (TIME)"), ("FK", "room_id (INT -> Rooms)"), ("REG", "course_code (VARCHAR)"), ("REG", "class_section (VARCHAR)")], "#6D28D9")
    draw_card(draw, f, 1260, 1850, 600, "Faculty_Status_Overrides", [("PK", "override_id (INT)"), ("FK", "faculty_id (INT -> Faculties)"), ("REG", "override_date (DATE)"), ("REG", "start_time (TIME) / end_time (TIME)"), ("REG", "status_type (CHECK: ON_LEAVE, MEETING)"), ("FK", "assigned_room_id (INT -> Rooms)"), ("REG", "notes (VARCHAR)")], "#6D28D9")

    # Connectors Frame 2
    draw_rel(draw, f, 540, 1490, 620, 1490, "1:N", 580, 1490)
    draw_rel(draw, f, 1160, 1490, 1260, 1490, "1:N", 1210, 1490)
    draw_rel(draw, f, 1560, 1750, 1560, 1850, "1:N", 1560, 1800)

    # Bottom Footer
    draw.rounded_rectangle([30, 2890, 2370, 2975], radius=8, fill='#FFFFFF', outline='#CBD5E1', width=2)
    draw.text((60, 2932), 'CHRIST (Deemed to be University) • Department of Computer Science • Course: BCA381-4 (DBMS Project) • Team 12', font=f['meta'], fill='#1E3A8A', anchor='lm')
    draw.text((2340, 2932), 'Sheet 1 of 3 (Core & Spatial Models)', font=f['frame_title'], fill='#059669', anchor='rm')

    out_path = 'images/erd_part1.png'
    im.save(out_path, format='PNG', optimize=True)
    print(f"[OK] Generated {out_path} ({os.path.getsize(out_path)} bytes)")

# =============================================================================
# PART 2: COMMERCIAL SERVICES & WELFARE
# =============================================================================
def generate_erd_part2():
    W, H = 2400, 3000
    im = Image.new('RGB', (W, H), color='#F8FAFC')
    draw = ImageDraw.Draw(im)
    f = get_fonts()

    # Top Banner
    draw.rounded_rectangle([30, 20, 2370, 135], radius=12, fill='#FFFFFF', outline='#CBD5E1', width=3)
    draw.text((1200, 48), 'UniChrist : Relational ER Diagram — Part 2 of 3', font=f['title'], fill='#0F172A', anchor='mm')
    draw.text((1200, 84), 'Smart Cafeteria Pre-Ordering, Bookstore & Uniforms, Health Clinic & Lost Vault', font=f['sub'], fill='#475569', anchor='mm')
    draw.text((1200, 112), 'Modules 1, 2, 3 & 4 • Fully Normalized to BCNF • Hardcopy Print Quality Edition', font=f['meta'], fill='#2563EB', anchor='mm')

    # Frame 1: Module 1 (Cafeteria Pre-Ordering)
    draw_module_frame(draw, f, 30, 155, 2340, 1120, "MODULE 1: SMART CAFETERIA PRE-ORDERING & FIFO QUEUE ENGINE", "Vendor stalls, dynamic digital menu, live stock tracking, FIFO token orders and itemized lines", "#D97706")
    draw_card(draw, f, 60, 225, 500, "Cafeteria_Vendors", [("PK", "vendor_id (INT)"), ("REG", "vendor_name (VARCHAR)"), ("FK", "block_id (INT -> Blocks)"), ("REG", "contact_phone (VARCHAR)"), ("REG", "is_open (BOOLEAN)")], "#B45309")
    draw_card(draw, f, 620, 225, 520, "Cafeteria_Items", [("PK", "item_id (INT)"), ("FK", "vendor_id (INT -> Vendors)"), ("REG", "item_name (VARCHAR)"), ("REG", "category (VARCHAR)"), ("REG", "price (NUMERIC 8,2 >= 0)"), ("REG", "is_available (BOOLEAN)"), ("REG", "current_stock_qty (INT >= 0)")], "#B45309")
    draw_card(draw, f, 1200, 225, 520, "Cafeteria_Orders", [("PK", "order_id (INT)"), ("FK", "user_id (INT -> Users)"), ("FK", "vendor_id (INT -> Vendors)"), ("REG", "order_timestamp (TIMESTAMP)"), ("REG", "token_number (INT FIFO)"), ("REG", "total_amount (NUMERIC >= 0)"), ("REG", "payment_mode (CHECK)"), ("REG", "order_status (CHECK)")], "#B45309")
    draw_card(draw, f, 1780, 225, 540, "Cafeteria_Order_Items", [("PK", "order_item_id (INT)"), ("FK", "order_id (INT -> Orders)"), ("FK", "item_id (INT -> Items)"), ("REG", "quantity (INT > 0)"), ("REG", "unit_price (NUMERIC 8,2)"), ("REG", "subtotal (NUMERIC 8,2 = qty * price)")], "#D97706")

    # Connectors Frame 1
    draw_rel(draw, f, 560, 290, 620, 290, "1:N", 590, 290)
    draw_rel(draw, f, 1140, 290, 1200, 290, "1:N", 1170, 290)
    draw_rel(draw, f, 1720, 290, 1780, 290, "1:N", 1750, 290)

    # Frame 2: Module 2 (Bookstore & Uniforms)
    draw_module_frame(draw, f, 30, 1310, 2340, 780, "MODULE 2: CAMPUS BOOKSTORE & UNIFORM MERCHANDISE", "Textbook & apparel catalog, stock management, student uniform bookings & purchase receipts", "#E11D48")
    draw_card(draw, f, 60, 1380, 500, "Store_Categories", [("PK", "category_id (INT)"), ("REG", "category_name (VARCHAR) UQ"), ("REG", "description (VARCHAR)")], "#BE123C")
    draw_card(draw, f, 620, 1380, 520, "Store_Inventory", [("PK", "product_id (INT)"), ("FK", "category_id (INT -> Categories)"), ("REG", "product_code (VARCHAR) UQ"), ("REG", "product_name (VARCHAR)"), ("REG", "unit_price (NUMERIC 10,2 >= 0)"), ("REG", "stock_quantity (INT >= 0)")], "#BE123C")
    draw_card(draw, f, 1200, 1380, 520, "Store_Orders", [("PK", "store_order_id (INT)"), ("FK", "user_id (INT -> Users)"), ("REG", "order_date (DATE)"), ("REG", "total_amount (NUMERIC >= 0)"), ("REG", "order_status (CHECK)")], "#BE123C")
    draw_card(draw, f, 1780, 1380, 540, "Store_Order_Items", [("PK", "store_order_item_id (INT)"), ("FK", "store_order_id (INT -> Store_Orders)"), ("FK", "product_id (INT -> Inventory)"), ("REG", "quantity (INT > 0)"), ("REG", "unit_price (NUMERIC 10,2)"), ("REG", "subtotal (NUMERIC 10,2)")], "#E11D48")

    # Connectors Frame 2
    draw_rel(draw, f, 560, 1450, 620, 1450, "1:N", 590, 1450)
    draw_rel(draw, f, 1140, 1450, 1200, 1450, "1:N", 1170, 1450)
    draw_rel(draw, f, 1720, 1450, 1780, 1450, "1:N", 1750, 1450)

    # Frame 3: Modules 3 & 4 (Health Clinic & Lost and Found)
    draw_module_frame(draw, f, 30, 2120, 2340, 740, "MODULES 3 & 4: CAMPUS CLINIC TRIAGE & LOST-AND-FOUND VAULT", "Medical visits, nurse duty triage, medicine dispensing, recovered lost articles and verification claims", "#0D9488")
    draw_card(draw, f, 60, 2190, 520, "Medical_Visits", [("PK", "visit_id (INT)"), ("FK", "student_id (INT -> Users)"), ("FK", "attending_staff_id (INT -> Users)"), ("REG", "checkin_time (TIMESTAMP)"), ("REG", "symptoms_observed (TEXT)"), ("REG", "temp_c / bp_systolic"), ("REG", "disposition (CHECK: REST, EMERGENCY)")], "#0E7490")
    draw_card(draw, f, 620, 2190, 520, "Medical_Prescriptions", [("PK", "prescription_id (INT)"), ("FK", "visit_id (INT -> Medical_Visits)"), ("REG", "medicine_name (VARCHAR)"), ("REG", "dosage (VARCHAR)"), ("REG", "quantity_dispensed (INT > 0)"), ("REG", "instructions (VARCHAR)")], "#0E7490")
    draw_card(draw, f, 1200, 2190, 520, "Lost_Found_Items", [("PK", "item_id (INT)"), ("FK", "reported_by_user_id (INT -> Users)"), ("REG", "item_title (VARCHAR)"), ("REG", "category (VARCHAR)"), ("REG", "photo_url (VARCHAR)"), ("FK", "found_at_room_id (INT -> Rooms)"), ("REG", "status (CHECK: OPEN, CLAIMED)")], "#0F766E")
    draw_card(draw, f, 1780, 2190, 540, "Lost_Found_Claims", [("PK", "claim_id (INT)"), ("FK", "item_id (INT -> Lost_Found_Items)"), ("FK", "claimed_by_user_id (INT -> Users)"), ("REG", "claim_description (TEXT)"), ("REG", "verification_status (CHECK)"), ("FK", "handed_over_by (INT -> Users)")], "#0F766E")

    # Connectors Frame 3
    draw_rel(draw, f, 580, 2260, 620, 2260, "1:N", 600, 2260)
    draw_rel(draw, f, 1720, 2260, 1780, 2260, "1:N", 1750, 2260)

    # Bottom Footer
    draw.rounded_rectangle([30, 2890, 2370, 2975], radius=8, fill='#FFFFFF', outline='#CBD5E1', width=2)
    draw.text((60, 2932), 'CHRIST (Deemed to be University) • Department of Computer Science • Course: BCA381-4 (DBMS Project) • Team 12', font=f['meta'], fill='#1E3A8A', anchor='lm')
    draw.text((2340, 2932), 'Sheet 2 of 3 (Commerce & Welfare)', font=f['frame_title'], fill='#D97706', anchor='rm')

    out_path = 'images/erd_part2.png'
    im.save(out_path, format='PNG', optimize=True)
    print(f"[OK] Generated {out_path} ({os.path.getsize(out_path)} bytes)")

# =============================================================================
# PART 3: LOGISTICS, LIBRARY & STUDENT LIFE
# =============================================================================
def generate_erd_part3():
    W, H = 2400, 3000
    im = Image.new('RGB', (W, H), color='#F8FAFC')
    draw = ImageDraw.Draw(im)
    f = get_fonts()

    # Top Banner
    draw.rounded_rectangle([30, 20, 2370, 135], radius=12, fill='#FFFFFF', outline='#CBD5E1', width=3)
    draw.text((1200, 48), 'UniChrist : Relational ER Diagram — Part 3 of 3', font=f['title'], fill='#0F172A', anchor='mm')
    draw.text((1200, 84), 'Central Library OPAC, Smart Parking & EV Telemetry, Student Clubs & Campus Events', font=f['sub'], fill='#475569', anchor='mm')
    draw.text((1200, 112), 'Modules 5, 6, 7 & 8 • Fully Normalized to BCNF • Hardcopy Print Quality Edition', font=f['meta'], fill='#2563EB', anchor='mm')

    # Frame 1: Module 5 (Library OPAC)
    draw_module_frame(draw, f, 30, 155, 2340, 780, "MODULE 5: CENTRAL LIBRARY OPAC & CIRCULATION ENGINE", "Subject taxonomy, ISBN catalogs, multi-copy shelf inventory, student borrowing and automated fines", "#475569")
    draw_card(draw, f, 60, 225, 460, "Book_Categories", [("PK", "category_id (INT)"), ("REG", "category_name (VARCHAR) UQ")], "#334155")
    draw_card(draw, f, 560, 225, 560, "Library_Books", [("PK", "book_id (INT)"), ("REG", "isbn (VARCHAR 20) UQ"), ("REG", "title (VARCHAR)"), ("REG", "author (VARCHAR)"), ("FK", "category_id (INT -> Categories)"), ("REG", "total_copies (INT >= 0)"), ("REG", "shelf_location (VARCHAR)")], "#334155")
    draw_card(draw, f, 1160, 225, 580, "Library_Circulation", [("PK", "issue_id (INT)"), ("FK", "book_id (INT -> Books)"), ("FK", "user_id (INT -> Users)"), ("REG", "issued_date (DATE)"), ("REG", "due_date (DATE)"), ("REG", "returned_date (DATE)"), ("REG", "fine_amount (NUMERIC >= 0)"), ("REG", "circulation_status (CHECK)")], "#334155")

    # Connectors Frame 1
    draw_rel(draw, f, 520, 290, 560, 290, "1:N", 540, 290)
    draw_rel(draw, f, 1120, 290, 1160, 290, "1:N", 1140, 290)

    # Frame 2: Module 6 (Smart Parking)
    draw_module_frame(draw, f, 30, 960, 2340, 760, "MODULE 6: SMART PARKING SENSOR & EV TELEMETRY", "Bay sensor telemetry, dedicated 2W/4W/EV parking bays, entry barriers and vehicle audit timestamps", "#EA580C")
    draw_card(draw, f, 60, 1030, 560, "Parking_Slots", [("PK", "slot_id (INT)"), ("FK", "block_id (INT -> Blocks)"), ("REG", "slot_code (VARCHAR 20) UQ"), ("REG", "vehicle_type (CHECK: TWO_WHEELER, FOUR_WHEELER)"), ("REG", "is_ev_charging (BOOLEAN)"), ("REG", "is_occupied (BOOLEAN)")], "#C2410C")
    draw_card(draw, f, 660, 1030, 580, "Parking_Logs", [("PK", "log_id (INT)"), ("FK", "slot_id (INT -> Slots)"), ("FK", "user_id (INT -> Users)"), ("REG", "vehicle_reg_number (VARCHAR 20)"), ("REG", "entry_timestamp (TIMESTAMP)"), ("REG", "exit_timestamp (TIMESTAMP)")], "#C2410C")

    # Connectors Frame 2
    draw_rel(draw, f, 620, 1100, 660, 1100, "1:N", 640, 1100)

    # Frame 3: Modules 7 & 8 (Clubs & Campus Events)
    draw_module_frame(draw, f, 30, 1745, 2340, 800, "MODULES 7 & 8: STUDENT SOCIETIES & SECURE QR EVENT ADMISSIONS", "Academic club governance, member rosters, campus fest event scheduling and SHA-256 digital entry passes", "#C026D3")
    draw_card(draw, f, 60, 1815, 520, "Student_Clubs", [("PK", "club_id (INT)"), ("FK", "school_id (INT -> Schools)"), ("REG", "club_name (VARCHAR) UQ"), ("REG", "club_tagline (VARCHAR)"), ("FK", "faculty_coordinator_id (INT -> Faculties)"), ("REG", "founded_year (INT)")], "#A21CAF")
    draw_card(draw, f, 620, 1815, 520, "Club_Memberships", [("PK", "membership_id (INT)"), ("FK", "club_id (INT -> Clubs)"), ("FK", "student_id (INT -> Students)"), ("REG", "joined_date (DATE)"), ("REG", "member_role (CHECK: MEMBER, EXECUTIVE)")], "#A21CAF")
    draw_card(draw, f, 1180, 1815, 540, "Campus_Events", [("PK", "event_id (INT)"), ("FK", "club_id (INT -> Clubs)"), ("REG", "event_title (VARCHAR)"), ("REG", "event_type (CHECK)"), ("FK", "venue_room_id (INT -> Rooms)"), ("REG", "max_registrations (INT > 0)")], "#A21CAF")
    draw_card(draw, f, 1760, 1815, 560, "Event_Registrations", [("PK", "registration_id (INT)"), ("FK", "event_id (INT -> Events)"), ("FK", "user_id (INT -> Users)"), ("REG", "registered_time (TIMESTAMP)"), ("REG", "qr_ticket_hash (VARCHAR 128) UQ"), ("REG", "has_attended (BOOLEAN)")], "#A21CAF")

    # Connectors Frame 3
    draw_rel(draw, f, 580, 1885, 620, 1885, "1:N", 600, 1885)
    draw_rel(draw, f, 1140, 1885, 1180, 1885, "1:N", 1160, 1885)
    draw_rel(draw, f, 1720, 1885, 1760, 1885, "1:N", 1740, 1885)

    # Frame 4: Legend Bar
    draw.rounded_rectangle([30, 2575, 2370, 2870], radius=10, fill='#FFFFFF', outline='#94A3B8', width=2)
    draw.text((60, 2605), 'FIGMA / FIGJAM ER DIAGRAM NOTATION KEY & BCNF INTEGRITY ASSURANCE', font=f['legend_hdr'], fill='#0F172A')

    draw.rounded_rectangle([60, 2635, 110, 2665], radius=4, fill='#FEF3C7', outline='#F59E0B', width=2)
    draw.text((85, 2650), 'PK', font=f['pill'], fill='#B45309', anchor='mm')
    draw.text((125, 2650), 'Primary Key (Entity Identifier)', font=f['legend_txt'], fill='#334155', anchor='lm')

    draw.rounded_rectangle([440, 2635, 490, 2665], radius=4, fill='#DBEAFE', outline='#3B82F6', width=2)
    draw.text((465, 2650), 'FK', font=f['pill'], fill='#1D4ED8', anchor='mm')
    draw.text((505, 2650), 'Foreign Key (Referential Constraint)', font=f['legend_txt'], fill='#334155', anchor='lm')

    draw.rounded_rectangle([860, 2635, 930, 2665], radius=4, fill='#F3E8FF', outline='#A855F7', width=2)
    draw.text((895, 2650), 'PK,FK', font=f['pill'], fill='#7E22CE', anchor='mm')
    draw.text((945, 2650), 'Subtype Entity Key (Inherited PK)', font=f['legend_txt'], fill='#334155', anchor='lm')

    pts = [(1350, 2650-10), (1364, 2650), (1350, 2650+10), (1336, 2650)]
    draw.polygon(pts, fill='#FFFFFF', outline='#1D4ED8', width=2)
    draw.text((1380, 2650), '1:1, 1:N, M:N Cardinality (Crow\'s Foot Decomposed Relationships)', font=f['legend_txt'], fill='#334155', anchor='lm')

    draw.text((60, 2715), '• BCNF Compliance: All 34 tables strictly satisfy Boyce-Codd Normal Form with every determinant as a candidate superkey.', font=f['legend_txt'], fill='#475569')
    draw.text((60, 2750), '• Live Interactive Figma Board: https://www.figma.com/board/13lZxvTOg5Z2wCOcCwvhm5', font=f['meta'], fill='#2563EB')
    draw.text((60, 2785), '• DBML Specification: Exported in UniChrist_Schema.dbml for dbdiagram.io / MySQL Workbench EER rendering.', font=f['legend_txt'], fill='#475569')

    # Bottom Footer
    draw.rounded_rectangle([30, 2890, 2370, 2975], radius=8, fill='#FFFFFF', outline='#CBD5E1', width=2)
    draw.text((60, 2932), 'CHRIST (Deemed to be University) • Department of Computer Science • Course: BCA381-4 (DBMS Project) • Team 12', font=f['meta'], fill='#1E3A8A', anchor='lm')
    draw.text((2340, 2932), 'Sheet 3 of 3 (Logistics, Library & Student Life)', font=f['frame_title'], fill='#C026D3', anchor='rm')

    out_path = 'images/erd_part3.png'
    im.save(out_path, format='PNG', optimize=True)
    print(f"[OK] Generated {out_path} ({os.path.getsize(out_path)} bytes)")

if __name__ == '__main__':
    os.makedirs('images', exist_ok=True)
    generate_erd_part1()
    generate_erd_part2()
    generate_erd_part3()
