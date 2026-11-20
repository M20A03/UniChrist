#!/usr/bin/env python3
"""
Generate 3 FigJam-authentic, high-contrast, non-linear (scattered/clustered) ERD sheets.
Features:
- FigJam canvas dot grid pattern
- Organic, clustered relational layout (hub-and-spoke, converging diamond junctions, NOT rigid straight lines)
- Rounded entity cards with bold drop shadows and distinct primary/foreign key pill badges
- FigJam-style sticky note callouts for architectural workflows and constraint notes
- Orthogonal elbow connector lines with Crow's Foot markers and relationship pill tags
- High-contrast typography designed specifically for crisp physical A4/Letter hardcopy printing
"""

import os
from PIL import Image, ImageDraw, ImageFont

def get_fonts():
    font_bold = '/usr/share/fonts/google-carlito-fonts/Carlito-Bold.ttf'
    font_reg = '/usr/share/fonts/google-carlito-fonts/Carlito-Regular.ttf'
    font_mono = '/usr/share/fonts/adwaita-mono-fonts/AdwaitaMono-Regular.ttf'
    font_mono_bold = '/usr/share/fonts/adwaita-mono-fonts/AdwaitaMono-Bold.ttf'
    
    return {
        'sheet_title': ImageFont.truetype(font_bold, 36),
        'sheet_sub': ImageFont.truetype(font_reg, 20),
        'sheet_meta': ImageFont.truetype(font_bold, 17),
        'section_pill': ImageFont.truetype(font_bold, 18),
        'section_desc': ImageFont.truetype(font_reg, 16),
        'card_title': ImageFont.truetype(font_bold, 22),
        'badge': ImageFont.truetype(font_bold, 14),
        'attr_name': ImageFont.truetype(font_mono, 17),
        'attr_bold': ImageFont.truetype(font_mono_bold, 17),
        'tag_pill': ImageFont.truetype(font_bold, 14),
        'sticky_title': ImageFont.truetype(font_bold, 17),
        'sticky_body': ImageFont.truetype(font_reg, 15),
        'legend_hdr': ImageFont.truetype(font_bold, 19),
        'legend_body': ImageFont.truetype(font_reg, 16)
    }

def draw_figjam_background(draw, W, H):
    # Base canvas background
    draw.rectangle([0, 0, W, H], fill='#F8FAFC')
    # Subtle FigJam canvas dot grid (every 40px)
    dot_color = '#CBD5E1'
    for x in range(30, W-30, 40):
        for y in range(160, H-120, 40):
            draw.ellipse([x-1.5, y-1.5, x+1.5, y+1.5], fill=dot_color)

def draw_top_header(draw, f, title, sub, meta):
    # Header card with FigJam style
    draw.rounded_rectangle([30, 20, 2370, 140], radius=14, fill='#FFFFFF', outline='#64748B', width=3)
    draw.text((1200, 48), title, font=f['sheet_title'], fill='#0F172A', anchor='mm')
    draw.text((1200, 86), sub, font=f['sheet_sub'], fill='#334155', anchor='mm')
    draw.text((1200, 116), meta, font=f['sheet_meta'], fill='#1D4ED8', anchor='mm')

def draw_bottom_footer(draw, f, left_text, right_text, color='#1D4ED8'):
    draw.rounded_rectangle([30, 2890, 2370, 2975], radius=10, fill='#FFFFFF', outline='#64748B', width=2)
    draw.text((60, 2932), left_text, font=f['sheet_meta'], fill='#0F172A', anchor='lm')
    draw.text((2340, 2932), right_text, font=f['sheet_meta'], fill=color, anchor='rm')

def draw_section_boundary(draw, f, x, y, w, h, title, sub, color):
    # FigJam section container with solid background
    draw.rounded_rectangle([x, y, x+w, y+h], radius=16, fill='#FFFFFF', outline=color, width=3)
    # Section header tab pill
    tw = len(title) * 12 + 40
    draw.rounded_rectangle([x+20, y-18, x+20+tw, y+24], radius=8, fill=color)
    draw.text((x+20+tw/2, y+3), title, font=f['section_pill'], fill='#FFFFFF', anchor='mm')
    draw.text((x+30+tw+16, y+24), sub, font=f['section_desc'], fill='#475569', anchor='lm')

def draw_figma_card(draw, f, x, y, w, title, attrs, theme_color):
    hh = 46
    rh = 33
    bh = len(attrs) * rh + 16
    th = hh + bh
    
    # Realistic soft drop shadow
    draw.rounded_rectangle([x+4, y+4, x+w+4, y+th+4], radius=10, fill='#CBD5E1')
    # Card surface
    draw.rounded_rectangle([x, y, x+w, y+th], radius=10, fill='#FFFFFF', outline='#475569', width=2)
    # Header strip
    draw.rounded_rectangle([x, y, x+w, y+hh], radius=10, fill=theme_color)
    draw.text((x + w/2, y + 23), title, font=f['card_title'], fill='#FFFFFF', anchor='mm')
    
    # Rows
    cy = y + hh + 22
    for idx, (atype, aname) in enumerate(attrs):
        # Zebra row highlight for crisp readability
        if idx % 2 == 1:
            draw.rounded_rectangle([x+3, cy-15, x+w-3, cy+15], radius=4, fill='#F1F5F9')
        
        # High-contrast Pill Badges
        if 'PK,FK' in atype or 'PK/FK' in atype:
            draw.rounded_rectangle([x+10, cy-14, x+72, cy+12], radius=5, fill='#F3E8FF', outline='#9333EA', width=2)
            draw.text((x+41, cy-1), 'PK,FK', font=f['badge'], fill='#6B21A8', anchor='mm')
            draw.text((x+82, cy-1), aname, font=f['attr_bold'], fill='#0F172A', anchor='lm')
        elif 'PK' in atype:
            draw.rounded_rectangle([x+10, cy-14, x+52, cy+12], radius=5, fill='#FEF3C7', outline='#D97706', width=2)
            draw.text((x+31, cy-1), 'PK', font=f['badge'], fill='#92400E', anchor='mm')
            draw.text((x+62, cy-1), aname, font=f['attr_bold'], fill='#0F172A', anchor='lm')
        elif 'FK' in atype:
            draw.rounded_rectangle([x+10, cy-14, x+52, cy+12], radius=5, fill='#DBEAFE', outline='#2563EB', width=2)
            draw.text((x+31, cy-1), 'FK', font=f['badge'], fill='#1E40AF', anchor='mm')
            draw.text((x+62, cy-1), aname, font=f['attr_name'], fill='#0F172A', anchor='lm')
        else:
            draw.text((x+22, cy-1), aname, font=f['attr_name'], fill='#1E293B', anchor='lm')
        cy += rh
    return th

def draw_sticky_note(draw, f, x, y, w, h, title, bullets, bg_color='#FEF08A', border_color='#CA8A04', header_color='#854D0E'):
    """Draw an authentic FigJam sticky note card for annotations, workflow logic and constraints."""
    # Drop shadow
    draw.rounded_rectangle([x+4, y+4, x+w+4, y+h+4], radius=8, fill='#CBD5E1')
    # Sticky body
    draw.rounded_rectangle([x, y, x+w, y+h], radius=8, fill=bg_color, outline=border_color, width=2)
    # Sticky pin / header
    draw.rectangle([x+12, y+10, x+w-12, y+14], fill=border_color)
    draw.text((x+20, y+32), title, font=f['sticky_title'], fill=header_color, anchor='lm')
    # Bullet points
    cy = y + 62
    for b in bullets:
        draw.text((x+20, cy), "• " + b, font=f['sticky_body'], fill='#1E293B', anchor='lm')
        cy += 24

def draw_elbow_rel(draw, f, points, label="", pill_pos=None):
    # Draw polyline with elbow bends
    draw.line(points, fill='#334155', width=3)
    # Draw Crow's foot fork at the end
    end_x, end_y = points[-1]
    prev_x, prev_y = points[-2]
    if end_x > prev_x: # pointing right
        draw.line([(end_x-14, end_y-10), (end_x, end_y)], fill='#334155', width=3)
        draw.line([(end_x-14, end_y+10), (end_x, end_y)], fill='#334155', width=3)
        draw.line([(end_x-10, end_y-10), (end_x-10, end_y+10)], fill='#334155', width=2)
    elif end_y > prev_y: # pointing down
        draw.line([(end_x-10, end_y-14), (end_x, end_y)], fill='#334155', width=3)
        draw.line([(end_x+10, end_y-14), (end_x, end_y)], fill='#334155', width=3)
        draw.line([(end_x-10, end_y-10), (end_x+10, end_y-10)], fill='#334155', width=2)
    elif end_x < prev_x: # pointing left
        draw.line([(end_x+14, end_y-10), (end_x, end_y)], fill='#334155', width=3)
        draw.line([(end_x+14, end_y+10), (end_x, end_y)], fill='#334155', width=3)
        draw.line([(end_x+10, end_y-10), (end_x+10, end_y+10)], fill='#334155', width=2)
    elif end_y < prev_y: # pointing up
        draw.line([(end_x-10, end_y+14), (end_x, end_y)], fill='#334155', width=3)
        draw.line([(end_x+10, end_y+14), (end_x, end_y)], fill='#334155', width=3)
        draw.line([(end_x-10, end_y+10), (end_x+10, end_y+10)], fill='#334155', width=2)

    # Optional label pill
    if label and pill_pos:
        px, py = pill_pos
        lw = len(label) * 9 + 22
        draw.rounded_rectangle([px-lw/2, py-13, px+lw/2, py+13], radius=6, fill='#FFFFFF', outline='#2563EB', width=2)
        draw.text((px, py), label, font=f['tag_pill'], fill='#1D4ED8', anchor='mm')

# =============================================================================
# SHEET 1: CLUSTERED ACADEMIC & SPATIAL DIRECTORY ENGINE
# =============================================================================
def generate_sheet1():
    W, H = 2400, 3000
    im = Image.new('RGB', (W, H))
    draw = ImageDraw.Draw(im)
    f = get_fonts()
    draw_figjam_background(draw, W, H)

    draw_top_header(draw, f,
        "UniChrist : Relational ER Diagram — Sheet 1 of 3",
        "Clustered Architecture: Core Demographics, Academic Structure & Spatial Timetables",
        "Modules 0, 9, 12, 10 & 11 • Fully Normalized to BCNF • High-Contrast Hardcopy Printout"
    )

    # Section A: Academic Hierarchy & Subtypes (Top Half)
    draw_section_boundary(draw, f, 30, 180, 2340, 1280, "SECTION A: DEMOGRAPHICS, GOVERNANCE & SUBTYPES", "Multi-role RBAC, university schools, departments, student/faculty inheritance and issue tracking", "#1D4ED8")
    
    # 1. Left Cluster: Roles -> Users (Central Demographic Anchor)
    draw_figma_card(draw, f, 60, 250, 380, "Roles", [
        ("PK", "role_id (INT)"),
        ("REG", "role_name (VARCHAR) UQ"),
        ("REG", "role_description (VARCHAR)")
    ], "#1E40AF")

    draw_figma_card(draw, f, 510, 250, 480, "Users", [
        ("PK", "user_id (INT)"),
        ("FK", "role_id (INT -> Roles)"),
        ("REG", "register_number (VARCHAR) UQ"),
        ("REG", "full_name (VARCHAR)"),
        ("REG", "email (VARCHAR) UQ"),
        ("REG", "password_hash (VARCHAR)"),
        ("REG", "is_active (BOOLEAN)")
    ], "#1D4ED8")

    # 2. Top-Right Cluster: Schools -> Departments (Academic Structure)
    draw_figma_card(draw, f, 1150, 250, 440, "Schools", [
        ("PK", "school_id (INT)"),
        ("REG", "school_name (VARCHAR) UQ"),
        ("REG", "school_dean (VARCHAR)")
    ], "#1E40AF")

    draw_figma_card(draw, f, 1680, 250, 480, "Departments", [
        ("PK", "dept_id (INT)"),
        ("FK", "school_id (INT -> Schools)"),
        ("REG", "dept_name (VARCHAR) UQ"),
        ("REG", "hod_name (VARCHAR)")
    ], "#1D4ED8")

    # 3. Subtype Split & Academic Resources (Scattered Hub-and-Spoke below)
    draw_figma_card(draw, f, 100, 700, 490, "Students", [
        ("PK,FK", "student_id (INT -> Users)"),
        ("FK", "dept_id (INT -> Depts)"),
        ("REG", "class_section (VARCHAR)"),
        ("REG", "semester (INT 1-8)"),
        ("REG", "batch_year (INT >= 2020)")
    ], "#2563EB")

    draw_figma_card(draw, f, 670, 700, 510, "Faculties", [
        ("PK,FK", "faculty_id (INT -> Users)"),
        ("FK", "dept_id (INT -> Depts)"),
        ("REG", "designation (VARCHAR)"),
        ("FK", "cabin_room_id (INT -> Rooms)"),
        ("REG", "office_extension (VARCHAR)")
    ], "#2563EB")

    draw_figma_card(draw, f, 1260, 700, 520, "Academic_Resources", [
        ("PK", "resource_id (INT)"),
        ("FK", "dept_id (INT -> Depts)"),
        ("FK", "uploaded_by_faculty_id (INT)"),
        ("REG", "resource_type (CHECK)"),
        ("REG", "course_code (VARCHAR)"),
        ("REG", "document_title (VARCHAR)"),
        ("REG", "download_count (INT)")
    ], "#334155")

    # 4. Grievance Redressal Pod (Right Wing)
    draw_figma_card(draw, f, 1840, 680, 480, "Grievances", [
        ("PK", "ticket_id (INT)"),
        ("FK", "student_id (INT -> Users)"),
        ("REG", "category (CHECK)"),
        ("FK", "room_id (INT -> Rooms)"),
        ("REG", "ticket_subject (VARCHAR)"),
        ("REG", "priority (CHECK)"),
        ("REG", "status (CHECK)")
    ], "#B91C1C")

    draw_figma_card(draw, f, 1840, 1080, 480, "Grievance_Audit_Logs", [
        ("PK", "log_id (INT)"),
        ("FK", "ticket_id (INT -> Grievances)"),
        ("FK", "changed_by_user_id (INT)"),
        ("REG", "previous_status (CHECK)"),
        ("REG", "new_status (CHECK)"),
        ("REG", "action_timestamp (TIME)")
    ], "#B91C1C")

    # FigJam Sticky Note in Section A
    draw_sticky_note(draw, f, 100, 1140, 600, 240,
        "RBAC & Subtype Specialization",
        [
            "Users entity handles authentication credentials.",
            "Students & Faculties inherit user_id via 1:1 subtype.",
            "Referential integrity enforced with CASCADE DELETE.",
            "Depts link both Students (major) & Faculties (staff)."
        ],
        bg_color='#EFF6FF', border_color='#3B82F6', header_color='#1E40AF'
    )

    draw_sticky_note(draw, f, 780, 1140, 600, 240,
        "Grievance Escalation Policy",
        [
            "Tickets tagged with room_id for physical maintenance.",
            "Grievance_Audit_Logs tracks status state transitions.",
            "Audit trail prevents silent ticket closure or tampering.",
            "Student identity validated via student_id FK."
        ],
        bg_color='#FEF2F2', border_color='#EF4444', header_color='#991B1B'
    )

    # Elbow Connectors for Section A
    draw_elbow_rel(draw, f, [(440, 310), (510, 310)], "assigns", (475, 290))
    draw_elbow_rel(draw, f, [(1590, 310), (1680, 310)], "contains", (1635, 290))
    # Users to Students
    draw_elbow_rel(draw, f, [(620, 540), (620, 620), (340, 620), (340, 700)], "1:1 subtype", (480, 620))
    # Users to Faculties
    draw_elbow_rel(draw, f, [(840, 540), (840, 620), (920, 620), (920, 700)], "1:1 subtype", (880, 620))
    # Departments to Academic_Resources
    draw_elbow_rel(draw, f, [(1920, 540), (1920, 620), (1520, 620), (1520, 700)], "categorizes", (1720, 620))
    # Grievances to Audit Logs
    draw_elbow_rel(draw, f, [(2080, 980), (2080, 1080)], "audited_by", (2080, 1030))

    # Section B: Spatial Engine & Faculty Weekly Timetables (Bottom Half)
    draw_section_boundary(draw, f, 30, 1510, 2340, 1340, "SECTION B: SPATIAL DIRECTORY & AUTOMATED FACULTY TIMETABLE ENGINE", "Campus block coordinates, room allocations, conflict-free period scheduling and live consultation overrides", "#059669")
    
    # Campus_Blocks (spatial anchor on left)
    draw_figma_card(draw, f, 80, 1600, 500, "Campus_Blocks", [
        ("PK", "block_id (INT)"),
        ("REG", "block_code (VARCHAR) UQ"),
        ("REG", "block_name (VARCHAR)"),
        ("REG", "total_floors (INT > 0)"),
        ("REG", "latitude (NUMERIC)"),
        ("REG", "longitude (NUMERIC)")
    ], "#059669")
    
    # Campus_Rooms (staggered right)
    draw_figma_card(draw, f, 660, 1600, 540, "Campus_Rooms", [
        ("PK", "room_id (INT)"),
        ("FK", "block_id (INT -> Blocks)"),
        ("REG", "room_number (VARCHAR)"),
        ("REG", "floor_number (INT >= 0)"),
        ("REG", "room_type (CHECK)"),
        ("REG", "seating_capacity (INT >= 0)")
    ], "#059669")
    
    # Faculty_Timetables (central schedule matrix)
    draw_figma_card(draw, f, 1280, 1600, 620, "Faculty_Timetables", [
        ("PK", "schedule_id (INT)"),
        ("FK", "faculty_id (INT -> Faculties)"),
        ("REG", "day_of_week (CHECK MONDAY-SAT)"),
        ("REG", "period_number (INT 1-8)"),
        ("REG", "start_time (TIME) / end_time (TIME)"),
        ("FK", "room_id (INT -> Rooms)"),
        ("REG", "course_code (VARCHAR)"),
        ("REG", "class_section (VARCHAR)")
    ], "#7C3AED")
    
    # Faculty_Status_Overrides (staggered down-right)
    draw_figma_card(draw, f, 1420, 2120, 640, "Faculty_Status_Overrides", [
        ("PK", "override_id (INT)"),
        ("FK", "faculty_id (INT -> Faculties)"),
        ("REG", "override_date (DATE)"),
        ("REG", "start_time (TIME) / end_time (TIME)"),
        ("REG", "status_type (CHECK: ON_LEAVE, MEETING)"),
        ("FK", "assigned_room_id (INT -> Rooms)"),
        ("REG", "notes (VARCHAR)")
    ], "#7C3AED")

    # FigJam Sticky Note for Spatial Conflict Resolver
    draw_sticky_note(draw, f, 80, 2120, 680, 270,
        "Spatial Conflict & Timetable Matrix",
        [
            "Unique constraint on (room_id, day_of_week, period_number)",
            "prevents double-booking any physical room in the campus.",
            "Unique constraint on (faculty_id, day_of_week, period_number)",
            "ensures no teacher is assigned two simultaneous lectures.",
            "Faculty_Status_Overrides dynamically supersedes regular periods",
            "enabling live student consultation room lookups."
        ],
        bg_color='#ECFDF5', border_color='#10B981', header_color='#065F46'
    )

    # Connectors for Section B
    draw_elbow_rel(draw, f, [(580, 1700), (660, 1700)], "houses", (620, 1680))
    draw_elbow_rel(draw, f, [(1200, 1700), (1280, 1700)], "schedules", (1240, 1680))
    draw_elbow_rel(draw, f, [(1650, 1980), (1650, 2050), (1740, 2050), (1740, 2120)], "overrides", (1700, 2050))

    draw_bottom_footer(draw, f,
        "CHRIST (Deemed to be University) • Department of Computer Science • Course: BCA381-4 • Team 12",
        "Sheet 1: Core Academic & Spatial Models",
        "#1D4ED8"
    )

    out = 'images/erd_part1.png'
    im.save(out, format='PNG', optimize=True)
    print(f"[OK] Rendered Sheet 1 (Clustered): {out}")

# =============================================================================
# SHEET 2: COMMERCIAL SERVICES & WELFARE RELATIONAL HUBS (SCATTERED LAYOUT)
# =============================================================================
def generate_sheet2():
    W, H = 2400, 3000
    im = Image.new('RGB', (W, H))
    draw = ImageDraw.Draw(im)
    f = get_fonts()
    draw_figjam_background(draw, W, H)

    draw_top_header(draw, f,
        "UniChrist : Relational ER Diagram — Sheet 2 of 3",
        "Clustered Architecture: Campus Commercial Services, Health Triage & Lost Vault",
        "Modules 1, 2, 3 & 4 • Fully Normalized to BCNF • High-Contrast Hardcopy Printout"
    )

    # =========================================================================
    # Section A: Smart Cafeteria Pre-Ordering (Diamond Junction & FIFO Queue)
    # =========================================================================
    draw_section_boundary(draw, f, 30, 180, 2340, 1140, "SECTION A: SMART CAFETERIA PRE-ORDERING & FIFO QUEUE ENGINE", "Vendor stalls, digital live menu catalog, FIFO token queue, customer orders and itemized lines", "#D97706")
    
    # Non-linear Diamond Clustered Architecture:
    # Vendors (top-left)  -> Items (top-center)
    #      |                       |
    #      v                       v
    # Orders (mid-left)   -> Order_Items (mid-center junction)
    # Sticky Note (right wing) explains FIFO queue & stock decrements
    draw_figma_card(draw, f, 80, 250, 480, "Cafeteria_Vendors", [
        ("PK", "vendor_id (INT)"),
        ("REG", "vendor_name (VARCHAR)"),
        ("FK", "block_id (INT -> Blocks)"),
        ("REG", "contact_phone (VARCHAR)"),
        ("REG", "is_open (BOOLEAN)")
    ], "#B45309")

    draw_figma_card(draw, f, 720, 240, 540, "Cafeteria_Items", [
        ("PK", "item_id (INT)"),
        ("FK", "vendor_id (INT -> Vendors)"),
        ("REG", "item_name (VARCHAR)"),
        ("REG", "category (VARCHAR)"),
        ("REG", "price (NUMERIC 8,2 >= 0)"),
        ("REG", "is_available (BOOLEAN)"),
        ("REG", "current_stock_qty (INT >= 0)")
    ], "#B45309")
    
    draw_figma_card(draw, f, 140, 710, 520, "Cafeteria_Orders", [
        ("PK", "order_id (INT)"),
        ("FK", "user_id (INT -> Users)"),
        ("FK", "vendor_id (INT -> Vendors)"),
        ("REG", "order_timestamp (TIMESTAMP)"),
        ("REG", "token_number (INT FIFO)"),
        ("REG", "total_amount (NUMERIC >= 0)"),
        ("REG", "payment_mode (CHECK)"),
        ("REG", "order_status (CHECK)")
    ], "#B45309")

    draw_figma_card(draw, f, 820, 720, 540, "Cafeteria_Order_Items", [
        ("PK", "order_item_id (INT)"),
        ("FK", "order_id (INT -> Orders)"),
        ("FK", "item_id (INT -> Items)"),
        ("REG", "quantity (INT > 0)"),
        ("REG", "unit_price (NUMERIC 8,2)"),
        ("REG", "subtotal (NUMERIC 8,2)")
    ], "#D97706")

    # FigJam Sticky Card for Cafeteria Queue Architecture
    draw_sticky_note(draw, f, 1500, 280, 800, 420,
        "FIFO Token Counter & Order State Machine",
        [
            "Vendors establish physical presence via Campus_Blocks block_id.",
            "Orders generate sequential token_number per vendor per calendar day.",
            "Order_Items acts as associative junction between Orders & Items.",
            "Subtotal computed as quantity * unit_price (redundancy eliminated).",
            "State machine transitions: PLACED -> PREPARING -> READY -> PICKED_UP.",
            "Atomic transaction updates inventory current_stock_qty on checkout.",
            "BCNF verified: all functional dependencies have candidate keys as determinants."
        ],
        bg_color='#FEF3C7', border_color='#F59E0B', header_color='#B45309'
    )

    # Elbow Connectors for Cafeteria (Diamond routing)
    # Vendors -> Items (menus)
    draw_elbow_rel(draw, f, [(560, 320), (720, 320)], "menus", (640, 300))
    # Vendors -> Orders (places)
    draw_elbow_rel(draw, f, [(320, 490), (320, 600), (380, 600), (380, 710)], "places", (350, 600))
    # Orders -> Order_Items (itemized)
    draw_elbow_rel(draw, f, [(660, 830), (820, 830)], "itemized", (740, 810))
    # Items -> Order_Items (ordered_in)
    draw_elbow_rel(draw, f, [(1080, 540), (1080, 720)], "ordered_in", (1080, 630))

    # =========================================================================
    # Section B: Bookstore & Uniform Merchandise (Staggered Converging Hub)
    # =========================================================================
    draw_section_boundary(draw, f, 30, 1360, 2340, 760, "SECTION B: CAMPUS BOOKSTORE & UNIFORM MERCHANDISE", "Textbook taxonomy, stock inventory, uniform bookings, purchase receipts and line details", "#E11D48")
    
    # Non-linear Staggered Positioning:
    # Categories (top-left) -> Inventory (top-center)
    # Orders (mid-left)     -> Order_Items (mid-center junction)
    # Sticky Note (right wing) explains textbook issuing & size variants
    draw_figma_card(draw, f, 80, 1420, 460, "Store_Categories", [
        ("PK", "category_id (INT)"),
        ("REG", "category_name (VARCHAR) UQ"),
        ("REG", "description (VARCHAR)")
    ], "#BE123C")

    draw_figma_card(draw, f, 660, 1420, 540, "Store_Inventory", [
        ("PK", "product_id (INT)"),
        ("FK", "category_id (INT -> Categories)"),
        ("REG", "product_code (VARCHAR) UQ"),
        ("REG", "product_name (VARCHAR)"),
        ("REG", "unit_price (NUMERIC 10,2 >= 0)"),
        ("REG", "stock_quantity (INT >= 0)")
    ], "#BE123C")

    draw_figma_card(draw, f, 160, 1740, 500, "Store_Orders", [
        ("PK", "store_order_id (INT)"),
        ("FK", "user_id (INT -> Users)"),
        ("REG", "order_date (DATE)"),
        ("REG", "total_amount (NUMERIC >= 0)"),
        ("REG", "order_status (CHECK)")
    ], "#BE123C")

    draw_figma_card(draw, f, 780, 1740, 540, "Store_Order_Items", [
        ("PK", "store_order_item_id (INT)"),
        ("FK", "store_order_id (INT -> Orders)"),
        ("FK", "product_id (INT -> Inventory)"),
        ("REG", "quantity (INT > 0)"),
        ("REG", "unit_price (NUMERIC 10,2)"),
        ("REG", "subtotal (NUMERIC 10,2)")
    ], "#E11D48")

    # FigJam Sticky Card for Bookstore
    draw_sticky_note(draw, f, 1460, 1440, 840, 310,
        "Bookstore Inventory & Uniform Slotting",
        [
            "Store_Categories segregates Course Textbooks, Lab Coats & Blazers.",
            "Store_Inventory tracks individual SKU stock_quantity.",
            "Orders placed by authenticated Users (students or parents).",
            "Store_Order_Items decomposes M:N relationship to BCNF.",
            "Integrity constraint ensures subtotal matches unit_price * quantity.",
            "Prevents stock overselling during beginning-of-semester rushes."
        ],
        bg_color='#FFE4E6', border_color='#FB7185', header_color='#BE123C'
    )

    # Elbow Connectors for Bookstore
    draw_elbow_rel(draw, f, [(540, 1490), (660, 1490)], "classifies", (600, 1470))
    draw_elbow_rel(draw, f, [(660, 1850), (780, 1850)], "buys", (720, 1830))
    draw_elbow_rel(draw, f, [(1020, 1680), (1020, 1740)], "contains", (1020, 1710))

    # =========================================================================
    # Section C: Health Clinic & Lost-and-Found Vault (Split Pod Architecture)
    # =========================================================================
    draw_section_boundary(draw, f, 30, 2160, 2340, 700, "SECTION C: HEALTH CLINIC TRIAGE & LOST-AND-FOUND VAULT", "Medical visits, prescription issuance, recovered campus articles and claim verification", "#0D9488")
    
    # Health Clinic Pod (Left Side)
    draw_figma_card(draw, f, 80, 2220, 520, "Medical_Visits", [
        ("PK", "visit_id (INT)"),
        ("FK", "student_id (INT -> Users)"),
        ("FK", "attending_staff_id (INT -> Users)"),
        ("REG", "checkin_time (TIMESTAMP)"),
        ("REG", "symptoms_observed (TEXT)"),
        ("REG", "temp_c / bp_systolic"),
        ("REG", "disposition (CHECK)")
    ], "#0E7490")

    draw_figma_card(draw, f, 660, 2280, 500, "Medical_Prescriptions", [
        ("PK", "prescription_id (INT)"),
        ("FK", "visit_id (INT -> Medical_Visits)"),
        ("REG", "medicine_name (VARCHAR)"),
        ("REG", "dosage (VARCHAR)"),
        ("REG", "quantity_dispensed (INT > 0)"),
        ("REG", "instructions (VARCHAR)")
    ], "#0E7490")
    
    # Lost and Found Vault Pod (Right Side)
    draw_figma_card(draw, f, 1220, 2220, 520, "Lost_Found_Items", [
        ("PK", "item_id (INT)"),
        ("FK", "reported_by_user_id (INT -> Users)"),
        ("REG", "item_title (VARCHAR)"),
        ("REG", "category (VARCHAR)"),
        ("REG", "photo_url (VARCHAR)"),
        ("FK", "found_at_room_id (INT -> Rooms)"),
        ("REG", "status (CHECK)")
    ], "#0F766E")

    draw_figma_card(draw, f, 1800, 2280, 520, "Lost_Found_Claims", [
        ("PK", "claim_id (INT)"),
        ("FK", "item_id (INT -> Items)"),
        ("FK", "claimed_by_user_id (INT -> Users)"),
        ("REG", "claim_description (TEXT)"),
        ("REG", "verification_status (CHECK)"),
        ("FK", "handed_over_by (INT -> Users)")
    ], "#0F766E")

    # Connectors Clinic & Lost
    draw_elbow_rel(draw, f, [(600, 2350), (660, 2350)], "prescribes", (630, 2330))
    draw_elbow_rel(draw, f, [(1740, 2350), (1800, 2350)], "claims", (1770, 2330))

    draw_bottom_footer(draw, f,
        "CHRIST (Deemed to be University) • Department of Computer Science • Course: BCA381-4 • Team 12",
        "Sheet 2: Campus Commercial & Welfare Services",
        "#D97706"
    )

    out = 'images/erd_part2.png'
    im.save(out, format='PNG', optimize=True)
    print(f"[OK] Rendered Sheet 2 (Clustered): {out}")

# =============================================================================
# SHEET 3: LOGISTICS, LIBRARY & STUDENT SOCIETIES (ORGANIC SCATTERED LAYOUT)
# =============================================================================
def generate_sheet3():
    W, H = 2400, 3000
    im = Image.new('RGB', (W, H))
    draw = ImageDraw.Draw(im)
    f = get_fonts()
    draw_figjam_background(draw, W, H)

    draw_top_header(draw, f,
        "UniChrist : Relational ER Diagram — Sheet 3 of 3",
        "Clustered Architecture: Library OPAC, Smart Parking & Student Societies with Blueprint Legend",
        "Modules 5, 6, 7 & 8 • Fully Normalized to BCNF • High-Contrast Hardcopy Printout"
    )

    # =========================================================================
    # Section A: Central Library OPAC & Multi-Copy Circulation (Staggered)
    # =========================================================================
    draw_section_boundary(draw, f, 30, 180, 2340, 780, "SECTION A: CENTRAL LIBRARY OPAC & MULTI-COPY CIRCULATION", "Subject taxonomy, ISBN catalogs, physical shelf copies, circulation loans and automated fine calculations", "#475569")
    
    draw_figma_card(draw, f, 80, 240, 460, "Book_Categories", [
        ("PK", "category_id (INT)"),
        ("REG", "category_name (VARCHAR) UQ")
    ], "#334155")

    draw_figma_card(draw, f, 620, 240, 560, "Library_Books", [
        ("PK", "book_id (INT)"),
        ("REG", "isbn (VARCHAR 20) UQ"),
        ("REG", "title (VARCHAR)"),
        ("REG", "author (VARCHAR)"),
        ("FK", "category_id (INT -> Categories)"),
        ("REG", "total_copies (INT >= 0)"),
        ("REG", "shelf_location (VARCHAR)")
    ], "#334155")

    draw_figma_card(draw, f, 1260, 240, 600, "Library_Circulation", [
        ("PK", "issue_id (INT)"),
        ("FK", "book_id (INT -> Books)"),
        ("FK", "user_id (INT -> Users)"),
        ("REG", "issued_date (DATE)"),
        ("REG", "due_date (DATE)"),
        ("REG", "returned_date (DATE)"),
        ("REG", "fine_amount (NUMERIC >= 0)"),
        ("REG", "circulation_status (CHECK)")
    ], "#334155")

    # FigJam Sticky Card for Library OPAC
    draw_sticky_note(draw, f, 1920, 240, 420, 360,
        "Library OPAC Rules",
        [
            "Unique constraint on isbn.",
            "Borrower validated via user_id FK.",
            "fine_amount calculated dynamically",
            "based on overdue days past due_date.",
            "total_copies decremented on ISSUE",
            "and restored upon RETURNED status."
        ],
        bg_color='#F1F5F9', border_color='#94A3B8', header_color='#334155'
    )

    # Connectors Library
    draw_elbow_rel(draw, f, [(540, 310), (620, 310)], "catalogs", (580, 290))
    draw_elbow_rel(draw, f, [(1180, 310), (1260, 310)], "loans", (1220, 290))

    # =========================================================================
    # Section B: Smart Parking Sensor & EV Telemetry (Staggered Pod)
    # =========================================================================
    draw_section_boundary(draw, f, 30, 1000, 2340, 720, "SECTION B: SMART PARKING SENSOR & EV TELEMETRY", "Bay sensor telemetry, 2W/4W/EV dedicated bays, barrier gates, vehicle logs and entry/exit timestamps", "#EA580C")
    
    draw_figma_card(draw, f, 100, 1060, 560, "Parking_Slots", [
        ("PK", "slot_id (INT)"),
        ("FK", "block_id (INT -> Blocks)"),
        ("REG", "slot_code (VARCHAR 20) UQ"),
        ("REG", "vehicle_type (CHECK: 2W, 4W)"),
        ("REG", "is_ev_charging (BOOLEAN)"),
        ("REG", "is_occupied (BOOLEAN)")
    ], "#C2410C")

    draw_figma_card(draw, f, 760, 1120, 580, "Parking_Logs", [
        ("PK", "log_id (INT)"),
        ("FK", "slot_id (INT -> Slots)"),
        ("FK", "user_id (INT -> Users)"),
        ("REG", "vehicle_reg_number (VARCHAR 20)"),
        ("REG", "entry_timestamp (TIMESTAMP)"),
        ("REG", "exit_timestamp (TIMESTAMP)")
    ], "#C2410C")

    # FigJam Sticky Card for Smart Parking
    draw_sticky_note(draw, f, 1420, 1060, 880, 320,
        "IoT Sensor Telemetry & Boom Barrier Automation",
        [
            "slot_id mapped to physical Campus_Blocks block_id for spatial navigation.",
            "Ultrasonic sensors update is_occupied boolean state in real-time.",
            "Barrier gate logs vehicle_reg_number with automated timestamp capture.",
            "exit_timestamp triggers slot status reset to AVAILABLE (is_occupied=FALSE).",
            "EV charging points segregated via is_ev_charging filter flag."
        ],
        bg_color='#FFF7ED', border_color='#FB923C', header_color='#C2410C'
    )

    # Connectors Parking
    draw_elbow_rel(draw, f, [(660, 1200), (760, 1200)], "tracks", (710, 1180))

    # =========================================================================
    # Section C: Student Societies & QR Fest Admissions (Hub-and-Spoke Clustered)
    # =========================================================================
    draw_section_boundary(draw, f, 30, 1760, 2340, 780, "SECTION C: STUDENT SOCIETIES & SECURE QR EVENT ADMISSIONS", "Academic club governance, member rosters, campus fest event scheduling and SHA-256 digital entry passes", "#C026D3")
    
    # Hub-and-Spoke Clustered Architecture:
    # Student_Clubs is central hub!
    #   |-> Club_Memberships (staggered down-left)
    #   |-> Campus_Events (staggered top-right) -> Event_Registrations (down-right)
    draw_figma_card(draw, f, 80, 1820, 520, "Student_Clubs", [
        ("PK", "club_id (INT)"),
        ("FK", "school_id (INT -> Schools)"),
        ("REG", "club_name (VARCHAR) UQ"),
        ("REG", "club_tagline (VARCHAR)"),
        ("FK", "faculty_coordinator_id (INT)"),
        ("REG", "founded_year (INT)")
    ], "#A21CAF")

    draw_figma_card(draw, f, 80, 2220, 520, "Club_Memberships", [
        ("PK", "membership_id (INT)"),
        ("FK", "club_id (INT -> Clubs)"),
        ("FK", "student_id (INT -> Students)"),
        ("REG", "joined_date (DATE)"),
        ("REG", "member_role (CHECK: MEMBER, EXEC)")
    ], "#A21CAF")

    draw_figma_card(draw, f, 740, 1820, 520, "Campus_Events", [
        ("PK", "event_id (INT)"),
        ("FK", "club_id (INT -> Clubs)"),
        ("REG", "event_title (VARCHAR)"),
        ("REG", "event_type (CHECK)"),
        ("FK", "venue_room_id (INT -> Rooms)"),
        ("REG", "max_registrations (INT > 0)")
    ], "#A21CAF")

    draw_figma_card(draw, f, 1360, 1880, 540, "Event_Registrations", [
        ("PK", "registration_id (INT)"),
        ("FK", "event_id (INT -> Events)"),
        ("FK", "user_id (INT -> Users)"),
        ("REG", "registered_time (TIMESTAMP)"),
        ("REG", "qr_ticket_hash (VARCHAR 128) UQ"),
        ("REG", "has_attended (BOOLEAN)")
    ], "#A21CAF")

    # FigJam Sticky Card for Events
    draw_sticky_note(draw, f, 1960, 1820, 380, 420,
        "QR Ticket Validation",
        [
            "Unique qr_ticket_hash",
            "prevents duplicate passes.",
            "venue_room_id verifies",
            "capacity against max seats.",
            "has_attended boolean set",
            "by volunteer scanner app.",
            "Decomposed M:N relations",
            "ensure strict BCNF status."
        ],
        bg_color='#FDF4FF', border_color='#E879F9', header_color='#A21CAF'
    )

    # Connectors Clubs & Events (Hub-and-spoke routing)
    draw_elbow_rel(draw, f, [(340, 2100), (340, 2220)], "enrolls", (340, 2160))
    draw_elbow_rel(draw, f, [(600, 1900), (740, 1900)], "hosts", (670, 1880))
    draw_elbow_rel(draw, f, [(1260, 1960), (1360, 1960)], "tickets", (1310, 1940))

    # =========================================================================
    # Blueprint Legend Box (Crisp High-Contrast Key)
    # =========================================================================
    draw.rounded_rectangle([30, 2570, 2370, 2870], radius=12, fill='#FFFFFF', outline='#475569', width=2)
    draw.text((60, 2595), 'FIGMA / FIGJAM ER DIAGRAM NOTATION KEY & BCNF INTEGRITY ASSURANCE', font=f['legend_hdr'], fill='#0F172A')

    # Legend pills
    draw.rounded_rectangle([60, 2625, 110, 2655], radius=5, fill='#FEF3C7', outline='#D97706', width=2)
    draw.text((85, 2640), 'PK', font=f['badge'], fill='#92400E', anchor='mm')
    draw.text((125, 2640), 'Primary Key (Entity Identifier)', font=f['legend_body'], fill='#0F172A', anchor='lm')

    draw.rounded_rectangle([480, 2625, 530, 2655], radius=5, fill='#DBEAFE', outline='#2563EB', width=2)
    draw.text((505, 2640), 'FK', font=f['badge'], fill='#1E40AF', anchor='mm')
    draw.text((545, 2640), 'Foreign Key (Referential Constraint)', font=f['legend_body'], fill='#0F172A', anchor='lm')

    draw.rounded_rectangle([920, 2625, 990, 2655], radius=5, fill='#F3E8FF', outline='#9333EA', width=2)
    draw.text((955, 2640), 'PK,FK', font=f['badge'], fill='#6B21A8', anchor='mm')
    draw.text((1005, 2640), 'Subtype Entity Key (Inherits Users PK)', font=f['legend_body'], fill='#0F172A', anchor='lm')

    draw.text((60, 2685), '• Crow\'s Foot Cardinality: 1:1, 1:N, and M:N relationships decomposed into associative junction tables with cascade rules.', font=f['legend_body'], fill='#334155')
    draw.text((60, 2720), '• BCNF Compliance: All 34 relational entities satisfy Boyce-Codd Normal Form with every determinant as a candidate superkey.', font=f['legend_body'], fill='#334155')
    draw.text((60, 2755), '• Live Interactive Figma Canvas: https://www.figma.com/board/13lZxvTOg5Z2wCOcCwvhm5', font=f['sheet_meta'], fill='#1D4ED8')
    draw.text((60, 2790), '• Tool Interoperability: Direct DBML schema export available in UniChrist_Schema.dbml for dbdiagram.io / MySQL Workbench.', font=f['legend_body'], fill='#334155')

    draw_bottom_footer(draw, f,
        "CHRIST (Deemed to be University) • Department of Computer Science • Course: BCA381-4 • Team 12",
        "Sheet 3: Campus Logistics, Library & Student Life",
        "#C026D3"
    )

    out = 'images/erd_part3.png'
    im.save(out, format='PNG', optimize=True)
    print(f"[OK] Rendered Sheet 3 (Clustered): {out}")

if __name__ == '__main__':
    os.makedirs('images', exist_ok=True)
    generate_sheet1()
    generate_sheet2()
    generate_sheet3()
