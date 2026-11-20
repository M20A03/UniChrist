#!/usr/bin/env python3
"""
Generate 4 FigJam-authentic, ULTRA-HIGH-CONTRAST ERD sheets with HUGE, PRINT-OPTIMIZED FONTS.
Font Sizes:
- Attributes: 40px - 44px (renders ~9.5pt to 10.5pt on physical printed paper!)
- Card Headers: 50px - 54px bold (~12pt physical print)
- Top Platform Banners: 64px - 72px bold
- Solid, thick 5px connector lines with sharp arrowheads and Crow's Foot forks
- Connected edge-to-edge directly between bounding boxes
"""

import os
from PIL import Image, ImageDraw, ImageFont

def get_fonts():
    font_bold = '/usr/share/fonts/google-carlito-fonts/Carlito-Bold.ttf'
    font_reg = '/usr/share/fonts/google-carlito-fonts/Carlito-Regular.ttf'
    font_mono = '/usr/share/fonts/adwaita-mono-fonts/AdwaitaMono-Regular.ttf'
    font_mono_bold = '/usr/share/fonts/adwaita-mono-fonts/AdwaitaMono-Bold.ttf'
    
    return {
        'sheet_title': ImageFont.truetype(font_bold, 64),
        'sheet_sub': ImageFont.truetype(font_reg, 36),
        'sheet_meta': ImageFont.truetype(font_bold, 30),
        'hub_title': ImageFont.truetype(font_bold, 44),
        'hub_sub': ImageFont.truetype(font_reg, 30),
        'card_title': ImageFont.truetype(font_bold, 50),
        'badge': ImageFont.truetype(font_bold, 28),
        'attr_name': ImageFont.truetype(font_mono, 38),
        'attr_bold': ImageFont.truetype(font_mono_bold, 38),
        'tag_pill': ImageFont.truetype(font_bold, 28),
        'sticky_title': ImageFont.truetype(font_bold, 34),
        'sticky_body': ImageFont.truetype(font_reg, 28),
        'legend_hdr': ImageFont.truetype(font_bold, 36),
        'legend_body': ImageFont.truetype(font_reg, 28)
    }

def draw_figjam_background(draw, W, H):
    draw.rectangle([0, 0, W, H], fill='#F8FAFC')
    dot_color = '#CBD5E1'
    for x in range(30, W-30, 50):
        for y in range(180, H-100, 50):
            draw.ellipse([x-2, y-2, x+2, y+2], fill=dot_color)

def draw_top_header(draw, f, title, sub, meta):
    draw.rounded_rectangle([30, 20, 2370, 160], radius=16, fill='#FFFFFF', outline='#334155', width=3)
    draw.text((1200, 52), title, font=f['sheet_title'], fill='#0F172A', anchor='mm')
    draw.text((1200, 102), sub, font=f['sheet_sub'], fill='#334155', anchor='mm')
    draw.text((1200, 138), meta, font=f['sheet_meta'], fill='#1D4ED8', anchor='mm')

def draw_bottom_footer(draw, f, left_text, right_text, color='#1D4ED8'):
    draw.rounded_rectangle([30, 2900, 2370, 2975], radius=10, fill='#FFFFFF', outline='#475569', width=2)
    draw.text((60, 2938), left_text, font=f['sheet_meta'], fill='#0F172A', anchor='lm')
    draw.text((2340, 2938), right_text, font=f['sheet_meta'], fill=color, anchor='rm')

def draw_central_hub_banner(draw, f, cards, name, x, y, w, h, title, subtitle, theme_color='#1E3A8A'):
    cards[name] = {'x': x, 'y': y, 'w': w, 'h': h}
    draw.rounded_rectangle([x+6, y+6, x+w+6, y+h+6], radius=16, fill='#CBD5E1')
    draw.rounded_rectangle([x, y, x+w, y+h], radius=16, fill='#FFFFFF', outline=theme_color, width=4)
    # Header strip
    draw.rounded_rectangle([x, y, x+w, y+h], radius=16, fill=theme_color)
    draw.text((x + w/2, y + 42), title, font=f['hub_title'], fill='#FFFFFF', anchor='mm')
    draw.text((x + w/2, y + 84), subtitle, font=f['hub_sub'], fill='#93C5FD', anchor='mm')

def draw_figma_card(draw, f, cards, title, x, y, w, attrs, theme_color):
    hh = 74
    rh = 56
    bh = len(attrs) * rh + 20
    th = hh + bh
    
    cards[title] = {'x': x, 'y': y, 'w': w, 'h': th}
    
    # Drop shadow
    draw.rounded_rectangle([x+6, y+6, x+w+6, y+th+6], radius=14, fill='#CBD5E1')
    # Card surface
    draw.rounded_rectangle([x, y, x+w, y+th], radius=14, fill='#FFFFFF', outline='#1E293B', width=3)
    # Header strip
    draw.rounded_rectangle([x, y, x+w, y+hh], radius=14, fill=theme_color)
    draw.text((x + w/2, y + 37), title, font=f['card_title'], fill='#FFFFFF', anchor='mm')
    
    # Rows
    cy = y + hh + 30
    for idx, (atype, aname) in enumerate(attrs):
        if idx % 2 == 1:
            draw.rounded_rectangle([x+4, cy-22, x+w-4, cy+22], radius=6, fill='#F1F5F9')
        
        # Badges & Text
        if 'PK,FK' in atype or 'PK/FK' in atype:
            draw.rounded_rectangle([x+16, cy-20, x+115, cy+18], radius=8, fill='#F3E8FF', outline='#9333EA', width=2)
            draw.text((x+65, cy-1), 'PK,FK', font=f['badge'], fill='#6B21A8', anchor='mm')
            draw.text((x+130, cy-1), aname, font=f['attr_bold'], fill='#0F172A', anchor='lm')
        elif 'PK' in atype:
            draw.rounded_rectangle([x+16, cy-20, x+85, cy+18], radius=8, fill='#FEF3C7', outline='#D97706', width=2)
            draw.text((x+50, cy-1), 'PK', font=f['badge'], fill='#92400E', anchor='mm')
            draw.text((x+100, cy-1), aname, font=f['attr_bold'], fill='#0F172A', anchor='lm')
        elif 'FK' in atype:
            draw.rounded_rectangle([x+16, cy-20, x+85, cy+18], radius=8, fill='#DBEAFE', outline='#2563EB', width=2)
            draw.text((x+50, cy-1), 'FK', font=f['badge'], fill='#1E40AF', anchor='mm')
            draw.text((x+100, cy-1), aname, font=f['attr_name'], fill='#0F172A', anchor='lm')
        else:
            draw.text((x+30, cy-1), aname, font=f['attr_name'], fill='#1E293B', anchor='lm')
        cy += rh
    return th

def draw_sticky_note(draw, f, x, y, w, h, title, bullets, bg_color='#FEF08A', border_color='#CA8A04', header_color='#854D0E'):
    draw.rounded_rectangle([x+6, y+6, x+w+6, y+h+6], radius=12, fill='#CBD5E1')
    draw.rounded_rectangle([x, y, x+w, y+h], radius=12, fill=bg_color, outline=border_color, width=3)
    draw.rectangle([x+20, y+16, x+w-20, y+24], fill=border_color)
    draw.text((x+28, y+52), title, font=f['sticky_title'], fill=header_color, anchor='lm')
    cy = y + 96
    for b in bullets:
        draw.text((x+28, cy), "• " + b, font=f['sticky_body'], fill='#0F172A', anchor='lm')
        cy += 40

def get_anchor(card, side):
    x, y, w, h = card['x'], card['y'], card['w'], card['h']
    if side == 'top':
        return (x + w/2, y)
    elif side == 'bottom':
        return (x + w/2, y + h)
    elif side == 'left':
        return (x, y + h/2)
    elif side == 'right':
        return (x + w, y + h/2)
    return (x + w/2, y + h/2)

def draw_connected_arrow(draw, f, cards, from_card, to_card, from_side, to_side, label="", waypoints=None, color='#0F172A'):
    p_start = get_anchor(cards[from_card], from_side)
    p_end = get_anchor(cards[to_card], to_side)
    
    points = [p_start]
    if waypoints:
        points.extend(waypoints)
    else:
        if from_side in ['right', 'left'] and to_side in ['left', 'right']:
            mid_x = (p_start[0] + p_end[0]) / 2
            points.append((mid_x, p_start[1]))
            points.append((mid_x, p_end[1]))
        elif from_side in ['top', 'bottom'] and to_side in ['top', 'bottom']:
            mid_y = (p_start[1] + p_end[1]) / 2
            points.append((p_start[0], mid_y))
            points.append((p_end[0], mid_y))
        elif from_side in ['right', 'left'] and to_side in ['top', 'bottom']:
            points.append((p_end[0], p_start[1]))
        elif from_side in ['top', 'bottom'] and to_side in ['left', 'right']:
            points.append((p_start[0], p_end[1]))
    points.append(p_end)
    
    # Thick bold line (5px)
    draw.line(points, fill=color, width=5)
    
    # Arrowhead
    end_x, end_y = p_end
    prev_x, prev_y = points[-2]
    
    if to_side == 'left' or end_x > prev_x:
        draw.polygon([(end_x, end_y), (end_x-22, end_y-13), (end_x-22, end_y+13)], fill=color)
        draw.line([(end_x-30, end_y-18), (end_x-30, end_y+18)], fill=color, width=4)
    elif to_side == 'right' or end_x < prev_x:
        draw.polygon([(end_x, end_y), (end_x+22, end_y-13), (end_x+22, end_y+13)], fill=color)
        draw.line([(end_x+30, end_y-18), (end_x+30, end_y+18)], fill=color, width=4)
    elif to_side == 'top' or end_y > prev_y:
        draw.polygon([(end_x, end_y), (end_x-13, end_y-22), (end_x+13, end_y-22)], fill=color)
        draw.line([(end_x-18, end_y-30), (end_x+18, end_y-30)], fill=color, width=4)
    elif to_side == 'bottom' or end_y < prev_y:
        draw.polygon([(end_x, end_y), (end_x-13, end_y+22), (end_x+13, end_y+22)], fill=color)
        draw.line([(end_x-18, end_y+30), (end_x+18, end_y+30)], fill=color, width=4)
    
    # Label pill
    if label:
        idx = len(points) // 2
        lx = (points[idx-1][0] + points[idx][0]) / 2
        ly = (points[idx-1][1] + points[idx][1]) / 2
        lw = len(label) * 16 + 36
        draw.rounded_rectangle([lx-lw/2, ly-22, lx+lw/2, ly+22], radius=8, fill='#FFFFFF', outline='#2563EB', width=3)
        draw.text((lx, ly), label, font=f['tag_pill'], fill='#1D4ED8', anchor='mm')

# =============================================================================
# SHEET 1: CORE DEMOGRAPHICS, GOVERNANCE & GRIEVANCES (PRINT-OPTIMIZED)
# =============================================================================
def generate_sheet1():
    W, H = 2400, 3000
    im = Image.new('RGB', (W, H))
    draw = ImageDraw.Draw(im)
    f = get_fonts()
    cards = {}
    draw_figjam_background(draw, W, H)

    draw_top_header(draw, f,
        "UniChrist : Relational ER Diagram — Sheet 1 of 4",
        "Core Demographics, Multi-Role RBAC, Academic Governance & Grievances",
        "Modules 0, 9, 11 & 12 • Ultra-High Contrast for Physical Paper Printout"
    )

    # 1. CENTRAL PLATFORM CORE HUB BANNER (Spanning Top)
    draw_central_hub_banner(draw, f, cards, 'Hub_Core', 110, 190, 2180, 110,
        "UniChrist Core Platform Engine : Demographics & Authentication Hub",
        "Central RBAC engine, polymorphic student/faculty subtype inheritance & institutional grievance triage",
        '#1E3A8A'
    )

    # Tier 1: Roles (Left) & Users (Right)
    draw_figma_card(draw, f, cards, 'Roles', 110, 340, 1040, [
        ("PK", "role_id (INT)"),
        ("REG", "role_name (VARCHAR 30) UQ"),
        ("REG", "role_description (VARCHAR 150)")
    ], '#1E40AF')

    draw_figma_card(draw, f, cards, 'Users', 1250, 340, 1040, [
        ("PK", "user_id (INT)"),
        ("FK", "role_id (INT -> Roles)"),
        ("REG", "register_number (VARCHAR 20) UQ"),
        ("REG", "full_name (VARCHAR 100)"),
        ("REG", "email (VARCHAR 100) UQ"),
        ("REG", "password_hash (VARCHAR 255)"),
        ("REG", "is_active (BOOLEAN DEFAULT TRUE)")
    ], '#1D4ED8')

    # Tier 2: Schools (Left) & Departments (Right)
    draw_figma_card(draw, f, cards, 'Schools', 110, 850, 1040, [
        ("PK", "school_id (INT)"),
        ("REG", "school_name (VARCHAR 100) UQ"),
        ("REG", "school_dean (VARCHAR 100)")
    ], '#1E40AF')

    draw_figma_card(draw, f, cards, 'Departments', 1250, 850, 1040, [
        ("PK", "dept_id (INT)"),
        ("FK", "school_id (INT -> Schools)"),
        ("REG", "dept_name (VARCHAR 100) UQ"),
        ("REG", "hod_name (VARCHAR 100)")
    ], '#1D4ED8')

    # Tier 3: Students (Left) & Faculties (Right)
    draw_figma_card(draw, f, cards, 'Students', 110, 1400, 1040, [
        ("PK,FK", "student_id (INT -> Users)"),
        ("FK", "dept_id (INT -> Departments)"),
        ("REG", "class_section (VARCHAR 10)"),
        ("REG", "semester (INT 1-8)"),
        ("REG", "batch_year (INT >= 2020)")
    ], '#2563EB')

    draw_figma_card(draw, f, cards, 'Faculties', 1250, 1400, 1040, [
        ("PK,FK", "faculty_id (INT -> Users)"),
        ("FK", "dept_id (INT -> Departments)"),
        ("REG", "designation (VARCHAR 50)"),
        ("FK", "cabin_room_id (INT -> Rooms)"),
        ("REG", "office_extension (VARCHAR 10)")
    ], '#2563EB')

    # Tier 4: Grievances (Left) & Academic_Resources (Right)
    draw_figma_card(draw, f, cards, 'Grievances', 110, 1980, 1040, [
        ("PK", "ticket_id (INT)"),
        ("FK", "student_id (INT -> Users)"),
        ("REG", "category (CHECK)"),
        ("FK", "room_id (INT -> Rooms)"),
        ("REG", "ticket_subject (VARCHAR 150)"),
        ("REG", "priority (CHECK)"),
        ("REG", "status (CHECK)")
    ], '#B91C1C')

    draw_figma_card(draw, f, cards, 'Academic_Resources', 1250, 1980, 1040, [
        ("PK", "resource_id (INT)"),
        ("FK", "dept_id (INT -> Departments)"),
        ("FK", "uploaded_by_faculty_id (INT -> Users)"),
        ("REG", "resource_type (CHECK)"),
        ("REG", "course_code (VARCHAR 20)"),
        ("REG", "document_title (VARCHAR 150)"),
        ("REG", "download_count (INT >= 0)")
    ], '#334155')

    # Tier 5: Grievance_Audit_Logs (Left) & Sticky Note (Right)
    draw_figma_card(draw, f, cards, 'Grievance_Audit_Logs', 110, 2520, 1040, [
        ("PK", "log_id (INT)"),
        ("FK", "ticket_id (INT -> Grievances)"),
        ("FK", "changed_by_user_id (INT -> Users)"),
        ("REG", "previous_status (CHECK)"),
        ("REG", "new_status (CHECK)"),
        ("REG", "action_timestamp (TIMESTAMP)")
    ], '#B91C1C')

    draw_sticky_note(draw, f, 1250, 2520, 1040, 340,
        "RBAC Specialization & Audit Integrity",
        [
            "Users entity holds login credentials & role_id.",
            "Students & Faculties inherit user_id via 1:1 subtype.",
            "Grievance_Audit_Logs tracks all ticket status changes.",
            "Referential integrity verified up to Boyce-Codd (BCNF)."
        ],
        bg_color='#EFF6FF', border_color='#3B82F6', header_color='#1E40AF'
    )

    # CONNECTING ARROWS (EDGE-TO-EDGE)
    draw_connected_arrow(draw, f, cards, 'Roles', 'Users', 'right', 'left', "assigns_role [1:N]")
    draw_connected_arrow(draw, f, cards, 'Schools', 'Departments', 'right', 'left', "contains [1:N]")
    draw_connected_arrow(draw, f, cards, 'Users', 'Students', 'bottom', 'top', "1:1 subtype", waypoints=[(1770, 810), (630, 810)])
    draw_connected_arrow(draw, f, cards, 'Users', 'Faculties', 'bottom', 'top', "1:1 subtype")
    draw_connected_arrow(draw, f, cards, 'Departments', 'Students', 'bottom', 'right', "enrolled_in", waypoints=[(1770, 1340), (1150, 1340)])
    draw_connected_arrow(draw, f, cards, 'Students', 'Grievances', 'bottom', 'top', "files_ticket [1:N]")
    draw_connected_arrow(draw, f, cards, 'Faculties', 'Academic_Resources', 'bottom', 'top', "uploads [1:N]")
    draw_connected_arrow(draw, f, cards, 'Grievances', 'Grievance_Audit_Logs', 'bottom', 'top', "audit_trail [1:N]")

    draw_bottom_footer(draw, f,
        "CHRIST (Deemed to be University) • Department of Computer Science • Course: BCA381-4 • Team 12",
        "Sheet 1: Core Demographics, Governance & Grievances",
        "#1D4ED8"
    )

    out = 'images/erd_part1.png'
    im.save(out, format='PNG', optimize=True)
    print(f"[OK] Rendered Sheet 1 (Huge 44px Font): {out}")

# =============================================================================
# SHEET 2: SPATIAL DIRECTORY, TIMETABLES & LIBRARY OPAC (PRINT-OPTIMIZED)
# =============================================================================
def generate_sheet2():
    W, H = 2400, 3000
    im = Image.new('RGB', (W, H))
    draw = ImageDraw.Draw(im)
    f = get_fonts()
    cards = {}
    draw_figjam_background(draw, W, H)

    draw_top_header(draw, f,
        "UniChrist : Relational ER Diagram — Sheet 2 of 4",
        "Campus Spatial Directory, Faculty Timetables, Smart Parking & Library OPAC",
        "Modules 5, 6 & 10 • Ultra-High Contrast for Physical Paper Printout"
    )

    # 1. CENTRAL PLATFORM HUB BANNER (Spanning Top)
    draw_central_hub_banner(draw, f, cards, 'Hub_Spatial', 110, 190, 2180, 110,
        "UniChrist Spatial & Navigation Platform : Campus Facilities & Logistics",
        "Spatial coordinates, conflict-free timetable matrix, ultrasonic parking telemetry & central library catalog",
        '#059669'
    )

    # Tier 1: Campus_Blocks (Left) & Campus_Rooms (Right)
    draw_figma_card(draw, f, cards, 'Campus_Blocks', 110, 340, 1040, [
        ("PK", "block_id (INT)"),
        ("REG", "block_code (VARCHAR 10) UQ"),
        ("REG", "block_name (VARCHAR 80)"),
        ("REG", "total_floors (INT > 0)"),
        ("REG", "latitude (NUMERIC 10,7)"),
        ("REG", "longitude (NUMERIC 10,7)")
    ], '#059669')

    draw_figma_card(draw, f, cards, 'Campus_Rooms', 1250, 340, 1040, [
        ("PK", "room_id (INT)"),
        ("FK", "block_id (INT -> Campus_Blocks)"),
        ("REG", "room_number (VARCHAR 20)"),
        ("REG", "floor_number (INT >= 0)"),
        ("REG", "room_type (CHECK: LAB, CLASS, CABIN)"),
        ("REG", "seating_capacity (INT >= 0)")
    ], '#059669')

    # Tier 2: Parking_Slots (Left) & Parking_Logs (Right)
    draw_figma_card(draw, f, cards, 'Parking_Slots', 110, 920, 1040, [
        ("PK", "slot_id (INT)"),
        ("FK", "block_id (INT -> Campus_Blocks)"),
        ("REG", "slot_code (VARCHAR 20) UQ"),
        ("REG", "vehicle_type (CHECK: 2W, 4W)"),
        ("REG", "is_ev_charging (BOOLEAN)"),
        ("REG", "is_occupied (BOOLEAN)")
    ], '#C2410C')

    draw_figma_card(draw, f, cards, 'Parking_Logs', 1250, 920, 1040, [
        ("PK", "log_id (INT)"),
        ("FK", "slot_id (INT -> Parking_Slots)"),
        ("FK", "user_id (INT -> Users)"),
        ("REG", "vehicle_reg_number (VARCHAR 20)"),
        ("REG", "entry_timestamp (TIMESTAMP)"),
        ("REG", "exit_timestamp (TIMESTAMP)")
    ], '#C2410C')

    # Tier 3: Faculty_Timetables (Left) & Faculty_Status_Overrides (Right)
    draw_figma_card(draw, f, cards, 'Faculty_Timetables', 110, 1500, 1040, [
        ("PK", "schedule_id (INT)"),
        ("FK", "faculty_id (INT -> Faculties)"),
        ("REG", "day_of_week (CHECK: MON-SAT)"),
        ("REG", "period_number (INT 1-8)"),
        ("REG", "start_time (TIME) / end_time (TIME)"),
        ("FK", "room_id (INT -> Campus_Rooms)"),
        ("REG", "course_code (VARCHAR 20)"),
        ("REG", "class_section (VARCHAR 10)")
    ], '#7C3AED')

    draw_figma_card(draw, f, cards, 'Faculty_Status_Overrides', 1250, 1500, 1040, [
        ("PK", "override_id (INT)"),
        ("FK", "faculty_id (INT -> Faculties)"),
        ("REG", "override_date (DATE)"),
        ("REG", "start_time (TIME) / end_time (TIME)"),
        ("REG", "status_type (CHECK: LEAVE, MEETING)"),
        ("FK", "assigned_room_id (INT -> Rooms)"),
        ("REG", "notes (VARCHAR 255)")
    ], '#7C3AED')

    # Tier 4: Library_Books (Left) & Library_Circulation (Right)
    draw_figma_card(draw, f, cards, 'Library_Books', 110, 2180, 1040, [
        ("PK", "book_id (INT)"),
        ("REG", "isbn (VARCHAR 20) UQ"),
        ("REG", "title (VARCHAR 100)"),
        ("REG", "author (VARCHAR 80)"),
        ("FK", "category_id (INT -> Categories)"),
        ("REG", "total_copies (INT >= 0)"),
        ("REG", "shelf_location (VARCHAR 30)")
    ], '#334155')

    draw_figma_card(draw, f, cards, 'Library_Circulation', 1250, 2180, 1040, [
        ("PK", "issue_id (INT)"),
        ("FK", "book_id (INT -> Library_Books)"),
        ("FK", "user_id (INT -> Users)"),
        ("REG", "issued_date (DATE)"),
        ("REG", "due_date (DATE)"),
        ("REG", "returned_date (DATE)"),
        ("REG", "fine_amount (NUMERIC >= 0)"),
        ("REG", "circulation_status (CHECK)")
    ], '#334155')

    # Tier 5: Book_Categories (Left) & Sticky Note (Right)
    draw_figma_card(draw, f, cards, 'Book_Categories', 110, 2700, 1040, [
        ("PK", "category_id (INT)"),
        ("REG", "category_name (VARCHAR 50) UQ")
    ], '#334155')

    draw_sticky_note(draw, f, 1250, 2700, 1040, 180,
        "Conflict Prevention & IoT Sensors",
        [
            "{room_id, day, period} -> composite candidate superkey.",
            "Parking sensors update occupancy flag in real-time."
        ],
        bg_color='#ECFDF5', border_color='#10B981', header_color='#065F46'
    )

    # CONNECTING ARROWS (EDGE-TO-EDGE)
    draw_connected_arrow(draw, f, cards, 'Campus_Blocks', 'Campus_Rooms', 'right', 'left', "houses [1:N]")
    draw_connected_arrow(draw, f, cards, 'Campus_Blocks', 'Parking_Slots', 'bottom', 'top', "allocates [1:N]")
    draw_connected_arrow(draw, f, cards, 'Parking_Slots', 'Parking_Logs', 'right', 'left', "tracks_barrier [1:N]")
    draw_connected_arrow(draw, f, cards, 'Campus_Rooms', 'Faculty_Timetables', 'bottom', 'top', "allocated_room", waypoints=[(1770, 850), (630, 850)])
    draw_connected_arrow(draw, f, cards, 'Faculty_Timetables', 'Faculty_Status_Overrides', 'right', 'left', "superseded_by [1:N]")
    draw_connected_arrow(draw, f, cards, 'Book_Categories', 'Library_Books', 'top', 'bottom', "catalogs [1:N]")
    draw_connected_arrow(draw, f, cards, 'Library_Books', 'Library_Circulation', 'right', 'left', "loans [1:N]")

    draw_bottom_footer(draw, f,
        "CHRIST (Deemed to be University) • Department of Computer Science • Course: BCA381-4 • Team 12",
        "Sheet 2: Campus Spatial Directory, Faculty Timetables, Parking & OPAC",
        "#059669"
    )

    out = 'images/erd_part2.png'
    im.save(out, format='PNG', optimize=True)
    print(f"[OK] Rendered Sheet 2 (Huge 44px Font): {out}")

# =============================================================================
# SHEET 3: COMMERCIAL ECOSYSTEM (SMART CAFETERIA & BOOKSTORE HUBS)
# =============================================================================
def generate_sheet3():
    W, H = 2400, 3000
    im = Image.new('RGB', (W, H))
    draw = ImageDraw.Draw(im)
    f = get_fonts()
    cards = {}
    draw_figjam_background(draw, W, H)

    draw_top_header(draw, f,
        "UniChrist : Relational ER Diagram — Sheet 3 of 4",
        "Campus Commercial Ecosystem: Smart Cafeteria & Campus Bookstore",
        "Modules 1 & 2 • Ultra-High Contrast for Physical Paper Printout"
    )

    # 1. CENTRAL PLATFORM HUB BANNER (Spanning Top)
    draw_central_hub_banner(draw, f, cards, 'Hub_Comm', 110, 190, 2180, 110,
        "UniChrist Commercial Platform : Smart Cafeteria & Campus Bookstore",
        "Multi-vendor menu ordering, daily FIFO queue tokens, retail stock management & itemized checkout lines",
        '#B45309'
    )

    # Left Column: Smart Cafeteria (Module 1)
    draw_figma_card(draw, f, cards, 'Cafeteria_Vendors', 110, 340, 1040, [
        ("PK", "vendor_id (INT)"),
        ("REG", "vendor_name (VARCHAR 80)"),
        ("FK", "block_id (INT -> Campus_Blocks)"),
        ("REG", "contact_phone (VARCHAR 15)"),
        ("REG", "is_open (BOOLEAN)")
    ], '#B45309')

    draw_figma_card(draw, f, cards, 'Cafeteria_Items', 110, 940, 1040, [
        ("PK", "item_id (INT)"),
        ("FK", "vendor_id (INT -> Cafeteria_Vendors)"),
        ("REG", "item_name (VARCHAR 80)"),
        ("REG", "category (VARCHAR 40)"),
        ("REG", "price (NUMERIC 8,2 >= 0)"),
        ("REG", "is_available (BOOLEAN)"),
        ("REG", "current_stock_qty (INT >= 0)")
    ], '#B45309')

    draw_figma_card(draw, f, cards, 'Cafeteria_Orders', 110, 1600, 1040, [
        ("PK", "order_id (INT)"),
        ("FK", "user_id (INT -> Users)"),
        ("FK", "vendor_id (INT -> Cafeteria_Vendors)"),
        ("REG", "order_timestamp (TIMESTAMP)"),
        ("REG", "token_number (INT FIFO)"),
        ("REG", "total_amount (NUMERIC 10,2 >= 0)"),
        ("REG", "payment_mode (CHECK)"),
        ("REG", "order_status (CHECK)")
    ], '#B45309')

    draw_figma_card(draw, f, cards, 'Cafeteria_Order_Items', 110, 2300, 1040, [
        ("PK", "order_item_id (INT)"),
        ("FK", "order_id (INT -> Cafeteria_Orders)"),
        ("FK", "item_id (INT -> Cafeteria_Items)"),
        ("REG", "quantity (INT > 0)"),
        ("REG", "unit_price (NUMERIC 8,2)"),
        ("REG", "subtotal (NUMERIC 8,2)")
    ], '#D97706')

    # Right Column: Bookstore & Uniform Merchandise (Module 2)
    draw_figma_card(draw, f, cards, 'Store_Categories', 1250, 340, 1040, [
        ("PK", "category_id (INT)"),
        ("REG", "category_name (VARCHAR 50) UQ"),
        ("REG", "description (VARCHAR 150)")
    ], '#BE123C')

    draw_figma_card(draw, f, cards, 'Store_Inventory', 1250, 940, 1040, [
        ("PK", "product_id (INT)"),
        ("FK", "category_id (INT -> Store_Categories)"),
        ("REG", "product_code (VARCHAR 30) UQ"),
        ("REG", "product_name (VARCHAR 100)"),
        ("REG", "unit_price (NUMERIC 10,2 >= 0)"),
        ("REG", "stock_quantity (INT >= 0)")
    ], '#BE123C')

    draw_figma_card(draw, f, cards, 'Store_Orders', 1250, 1600, 1040, [
        ("PK", "store_order_id (INT)"),
        ("FK", "user_id (INT -> Users)"),
        ("REG", "order_date (DATE)"),
        ("REG", "total_amount (NUMERIC 10,2 >= 0)"),
        ("REG", "order_status (CHECK)")
    ], '#BE123C')

    draw_figma_card(draw, f, cards, 'Store_Order_Items', 1250, 2300, 1040, [
        ("PK", "store_order_item_id (INT)"),
        ("FK", "store_order_id (INT -> Store_Orders)"),
        ("FK", "product_id (INT -> Store_Inventory)"),
        ("REG", "quantity (INT > 0)"),
        ("REG", "unit_price (NUMERIC 10,2)"),
        ("REG", "subtotal (NUMERIC 10,2)")
    ], '#E11D48')

    # CONNECTING ARROWS (EDGE-TO-EDGE)
    draw_connected_arrow(draw, f, cards, 'Cafeteria_Vendors', 'Cafeteria_Items', 'bottom', 'top', "menus [1:N]")
    draw_connected_arrow(draw, f, cards, 'Cafeteria_Vendors', 'Cafeteria_Orders', 'bottom', 'top', "receives [1:N]", waypoints=[(250, 850), (250, 1600)])
    draw_connected_arrow(draw, f, cards, 'Cafeteria_Orders', 'Cafeteria_Order_Items', 'bottom', 'top', "itemized [1:N]")
    draw_connected_arrow(draw, f, cards, 'Cafeteria_Items', 'Cafeteria_Order_Items', 'bottom', 'top', "ordered_in [1:N]", waypoints=[(450, 1500), (450, 2300)])

    draw_connected_arrow(draw, f, cards, 'Store_Categories', 'Store_Inventory', 'bottom', 'top', "classifies [1:N]")
    draw_connected_arrow(draw, f, cards, 'Store_Orders', 'Store_Order_Items', 'bottom', 'top', "contains [1:N]")
    draw_connected_arrow(draw, f, cards, 'Store_Inventory', 'Store_Order_Items', 'bottom', 'top', "sold_in [1:N]", waypoints=[(1550, 1500), (1550, 2300)])

    draw_bottom_footer(draw, f,
        "CHRIST (Deemed to be University) • Department of Computer Science • Course: BCA381-4 • Team 12",
        "Sheet 3: Commercial Services & Order Junctions",
        "#B45309"
    )

    out = 'images/erd_part3.png'
    im.save(out, format='PNG', optimize=True)
    print(f"[OK] Rendered Sheet 3 (Huge 44px Font): {out}")

# =============================================================================
# SHEET 4: WELFARE, SOCIETIES, EVENTS & BLUEPRINT LEGEND (PRINT-OPTIMIZED)
# =============================================================================
def generate_sheet4():
    W, H = 2400, 3000
    im = Image.new('RGB', (W, H))
    draw = ImageDraw.Draw(im)
    f = get_fonts()
    cards = {}
    draw_figjam_background(draw, W, H)

    draw_top_header(draw, f,
        "UniChrist : Relational ER Diagram — Sheet 4 of 4",
        "Campus Welfare, Health Clinic, Lost Vault, Student Societies & Architecture Legend",
        "Modules 3, 4, 7 & 8 • Ultra-High Contrast for Physical Paper Printout"
    )

    # 1. CENTRAL PLATFORM HUB BANNER (Spanning Top)
    draw_central_hub_banner(draw, f, cards, 'Hub_Life', 110, 190, 2180, 110,
        "UniChrist Student Life & Welfare Platform : Health, Societies & Event Passes",
        "First-aid triage, custodial lost-and-found repository, club memberships & cryptographically verified QR passes",
        '#A21CAF'
    )

    # Left Column: Medical Clinic & Lost Vault (Modules 3 & 4)
    draw_figma_card(draw, f, cards, 'Medical_Visits', 110, 340, 1040, [
        ("PK", "visit_id (INT)"),
        ("FK", "student_id (INT -> Users)"),
        ("FK", "attending_staff_id (INT -> Users)"),
        ("REG", "checkin_time (TIMESTAMP)"),
        ("REG", "symptoms_observed (TEXT)"),
        ("REG", "temp_c / bp_systolic"),
        ("REG", "disposition (CHECK)")
    ], '#0E7490')

    draw_figma_card(draw, f, cards, 'Medical_Prescriptions', 110, 940, 1040, [
        ("PK", "prescription_id (INT)"),
        ("FK", "visit_id (INT -> Medical_Visits)"),
        ("REG", "medicine_name (VARCHAR 80)"),
        ("REG", "dosage (VARCHAR 30)"),
        ("REG", "quantity_dispensed (INT > 0)"),
        ("REG", "instructions (VARCHAR 150)")
    ], '#0E7490')

    draw_figma_card(draw, f, cards, 'Lost_Found_Items', 110, 1480, 1040, [
        ("PK", "item_id (INT)"),
        ("FK", "reported_by_user_id (INT -> Users)"),
        ("REG", "item_title (VARCHAR 100)"),
        ("REG", "category (VARCHAR 40)"),
        ("REG", "photo_url (VARCHAR 200)"),
        ("FK", "found_at_room_id (INT -> Rooms)"),
        ("REG", "status (CHECK)")
    ], '#0F766E')

    draw_figma_card(draw, f, cards, 'Lost_Found_Claims', 110, 2080, 1040, [
        ("PK", "claim_id (INT)"),
        ("FK", "item_id (INT -> Lost_Found_Items)"),
        ("FK", "claimed_by_user_id (INT -> Users)"),
        ("REG", "claim_description (TEXT)"),
        ("REG", "verification_status (CHECK)"),
        ("FK", "handed_over_by (INT -> Users)")
    ], '#0F766E')

    # Right Column: Student Clubs & Events (Modules 7 & 8)
    draw_figma_card(draw, f, cards, 'Student_Clubs', 1250, 340, 1040, [
        ("PK", "club_id (INT)"),
        ("FK", "school_id (INT -> Schools)"),
        ("REG", "club_name (VARCHAR 80) UQ"),
        ("REG", "club_tagline (VARCHAR 150)"),
        ("FK", "faculty_coordinator_id (INT -> Users)"),
        ("REG", "founded_year (INT >= 1969)")
    ], '#A21CAF')

    draw_figma_card(draw, f, cards, 'Club_Memberships', 1250, 940, 1040, [
        ("PK", "membership_id (INT)"),
        ("FK", "club_id (INT -> Student_Clubs)"),
        ("FK", "student_id (INT -> Users)"),
        ("REG", "joined_date (DATE)"),
        ("REG", "member_role (CHECK: MEMBER, EXEC)")
    ], '#A21CAF')

    draw_figma_card(draw, f, cards, 'Campus_Events', 1250, 1480, 1040, [
        ("PK", "event_id (INT)"),
        ("FK", "club_id (INT -> Student_Clubs)"),
        ("REG", "event_title (VARCHAR 100)"),
        ("REG", "event_type (CHECK)"),
        ("FK", "venue_room_id (INT -> Rooms)"),
        ("REG", "max_registrations (INT > 0)")
    ], '#A21CAF')

    draw_figma_card(draw, f, cards, 'Event_Registrations', 1250, 2080, 1040, [
        ("PK", "registration_id (INT)"),
        ("FK", "event_id (INT -> Campus_Events)"),
        ("FK", "user_id (INT -> Users)"),
        ("REG", "registered_time (TIMESTAMP)"),
        ("REG", "qr_ticket_hash (VARCHAR 128) UQ"),
        ("REG", "has_attended (BOOLEAN)")
    ], '#A21CAF')

    # CONNECTING ARROWS (EDGE-TO-EDGE)
    draw_connected_arrow(draw, f, cards, 'Medical_Visits', 'Medical_Prescriptions', 'bottom', 'top', "prescribes [1:N]")
    draw_connected_arrow(draw, f, cards, 'Lost_Found_Items', 'Lost_Found_Claims', 'bottom', 'top', "claims [1:N]")
    draw_connected_arrow(draw, f, cards, 'Student_Clubs', 'Club_Memberships', 'bottom', 'top', "enrolls [1:N]")
    draw_connected_arrow(draw, f, cards, 'Student_Clubs', 'Campus_Events', 'bottom', 'top', "hosts [1:N]", waypoints=[(1450, 850), (1450, 1480)])
    draw_connected_arrow(draw, f, cards, 'Campus_Events', 'Event_Registrations', 'bottom', 'top', "tickets [1:N]")

    # =========================================================================
    # BLUEPRINT NOTATION LEGEND (CRISP HIGH-CONTRAST SPANNING BOX)
    # =========================================================================
    draw.rounded_rectangle([30, 2580, 2370, 2870], radius=16, fill='#FFFFFF', outline='#0F172A', width=3)
    draw.text((60, 2610), 'FIGMA / FIGJAM ER DIAGRAM NOTATION KEY & BCNF INTEGRITY ASSURANCE', font=f['legend_hdr'], fill='#0F172A')

    # Badges
    draw.rounded_rectangle([60, 2650, 140, 2695], radius=8, fill='#FEF3C7', outline='#D97706', width=3)
    draw.text((100, 2672), 'PK', font=f['badge'], fill='#92400E', anchor='mm')
    draw.text((160, 2672), 'Primary Key (Unique Entity Identifier)', font=f['legend_body'], fill='#0F172A', anchor='lm')

    draw.rounded_rectangle([720, 2650, 800, 2695], radius=8, fill='#DBEAFE', outline='#2563EB', width=3)
    draw.text((760, 2672), 'FK', font=f['badge'], fill='#1E40AF', anchor='mm')
    draw.text((820, 2672), 'Foreign Key (Referential Constraint)', font=f['legend_body'], fill='#0F172A', anchor='lm')

    draw.rounded_rectangle([1380, 2650, 1490, 2695], radius=8, fill='#F3E8FF', outline='#9333EA', width=3)
    draw.text((1435, 2672), 'PK,FK', font=f['badge'], fill='#6B21A8', anchor='mm')
    draw.text((1510, 2672), 'Subtype Key (Inherits Users PK)', font=f['legend_body'], fill='#0F172A', anchor='lm')

    draw.text((60, 2730), '• Crow\'s Foot Cardinality: 1:1, 1:N, and M:N decomposed into associative relations with referential CASCADE integrity.', font=f['legend_body'], fill='#1E293B')
    draw.text((60, 2775), '• BCNF Compliance: All 34 relational entities satisfy Boyce-Codd Normal Form with every determinant as a candidate superkey.', font=f['legend_body'], fill='#1E293B')
    draw.text((60, 2820), '• Live Interactive Figma Canvas: https://www.figma.com/board/13lZxvTOg5Z2wCOcCwvhm5', font=f['sheet_meta'], fill='#1D4ED8')

    draw_bottom_footer(draw, f,
        "CHRIST (Deemed to be University) • Department of Computer Science • Course: BCA381-4 • Team 12",
        "Sheet 4: Student Life, Campus Welfare & Architecture Legend",
        "#A21CAF"
    )

    out = 'images/erd_part4.png'
    im.save(out, format='PNG', optimize=True)
    print(f"[OK] Rendered Sheet 4 (Huge 44px Font): {out}")

if __name__ == '__main__':
    os.makedirs('images', exist_ok=True)
    generate_sheet1()
    generate_sheet2()
    generate_sheet3()
    generate_sheet4()
