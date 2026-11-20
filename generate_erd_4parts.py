#!/usr/bin/env python3
"""
Generate 4 FigJam-authentic, ultra-high-contrast, spacious ERD sheets.
Features:
- 4 Dedicated Sheets (Modules 0,9,11,12 | Modules 10,6 | Modules 1,2 | Modules 3,4,5,7,8 + Legend)
- Prominent "UniChrist Core Platform Hub" in the center of all sheets
- All arrows connect directly from the edge of one box to the edge of another box
- Massive 22-26pt monospace attributes and 26-30pt bold titles for crystal-clear physical printouts
- Crow's foot forks and directional arrowheads with clear relationship verb pills
- FigJam canvas dot grid and whiteboard sticky note annotations
"""

import os
from PIL import Image, ImageDraw, ImageFont

def get_fonts():
    font_bold = '/usr/share/fonts/google-carlito-fonts/Carlito-Bold.ttf'
    font_reg = '/usr/share/fonts/google-carlito-fonts/Carlito-Regular.ttf'
    font_mono = '/usr/share/fonts/adwaita-mono-fonts/AdwaitaMono-Regular.ttf'
    font_mono_bold = '/usr/share/fonts/adwaita-mono-fonts/AdwaitaMono-Bold.ttf'
    
    return {
        'sheet_title': ImageFont.truetype(font_bold, 38),
        'sheet_sub': ImageFont.truetype(font_reg, 22),
        'sheet_meta': ImageFont.truetype(font_bold, 18),
        'hub_title': ImageFont.truetype(font_bold, 28),
        'hub_sub': ImageFont.truetype(font_reg, 20),
        'hub_desc': ImageFont.truetype(font_mono, 18),
        'card_title': ImageFont.truetype(font_bold, 24),
        'badge': ImageFont.truetype(font_bold, 15),
        'attr_name': ImageFont.truetype(font_mono, 19),
        'attr_bold': ImageFont.truetype(font_mono_bold, 19),
        'tag_pill': ImageFont.truetype(font_bold, 16),
        'sticky_title': ImageFont.truetype(font_bold, 20),
        'sticky_body': ImageFont.truetype(font_reg, 17),
        'legend_hdr': ImageFont.truetype(font_bold, 21),
        'legend_body': ImageFont.truetype(font_reg, 17)
    }

def draw_figjam_background(draw, W, H):
    draw.rectangle([0, 0, W, H], fill='#F8FAFC')
    dot_color = '#CBD5E1'
    for x in range(30, W-30, 40):
        for y in range(160, H-120, 40):
            draw.ellipse([x-1.5, y-1.5, x+1.5, y+1.5], fill=dot_color)

def draw_top_header(draw, f, title, sub, meta):
    draw.rounded_rectangle([30, 20, 2370, 140], radius=14, fill='#FFFFFF', outline='#475569', width=3)
    draw.text((1200, 46), title, font=f['sheet_title'], fill='#0F172A', anchor='mm')
    draw.text((1200, 86), sub, font=f['sheet_sub'], fill='#334155', anchor='mm')
    draw.text((1200, 118), meta, font=f['sheet_meta'], fill='#1D4ED8', anchor='mm')

def draw_bottom_footer(draw, f, left_text, right_text, color='#1D4ED8'):
    draw.rounded_rectangle([30, 2890, 2370, 2975], radius=10, fill='#FFFFFF', outline='#475569', width=2)
    draw.text((60, 2932), left_text, font=f['sheet_meta'], fill='#0F172A', anchor='lm')
    draw.text((2340, 2932), right_text, font=f['sheet_meta'], fill=color, anchor='rm')

def draw_figma_card(draw, f, cards, title, x, y, w, attrs, theme_color):
    hh = 52
    rh = 38
    bh = len(attrs) * rh + 18
    th = hh + bh
    
    # Store card rect for anchor calculations
    cards[title] = {'x': x, 'y': y, 'w': w, 'h': th}
    
    # Drop shadow
    draw.rounded_rectangle([x+6, y+6, x+w+6, y+th+6], radius=12, fill='#CBD5E1')
    # Card surface
    draw.rounded_rectangle([x, y, x+w, y+th], radius=12, fill='#FFFFFF', outline='#334155', width=3)
    # Header strip
    draw.rounded_rectangle([x, y, x+w, y+hh], radius=12, fill=theme_color)
    draw.text((x + w/2, y + 26), title, font=f['card_title'], fill='#FFFFFF', anchor='mm')
    
    # Rows
    cy = y + hh + 24
    for idx, (atype, aname) in enumerate(attrs):
        if idx % 2 == 1:
            draw.rounded_rectangle([x+4, cy-17, x+w-4, cy+17], radius=4, fill='#F1F5F9')
        
        if 'PK,FK' in atype or 'PK/FK' in atype:
            draw.rounded_rectangle([x+12, cy-15, x+80, cy+14], radius=6, fill='#F3E8FF', outline='#9333EA', width=2)
            draw.text((x+46, cy-1), 'PK,FK', font=f['badge'], fill='#6B21A8', anchor='mm')
            draw.text((x+92, cy-1), aname, font=f['attr_bold'], fill='#0F172A', anchor='lm')
        elif 'PK' in atype:
            draw.rounded_rectangle([x+12, cy-15, x+58, cy+14], radius=6, fill='#FEF3C7', outline='#D97706', width=2)
            draw.text((x+35, cy-1), 'PK', font=f['badge'], fill='#92400E', anchor='mm')
            draw.text((x+70, cy-1), aname, font=f['attr_bold'], fill='#0F172A', anchor='lm')
        elif 'FK' in atype:
            draw.rounded_rectangle([x+12, cy-15, x+58, cy+14], radius=6, fill='#DBEAFE', outline='#2563EB', width=2)
            draw.text((x+35, cy-1), 'FK', font=f['badge'], fill='#1E40AF', anchor='mm')
            draw.text((x+70, cy-1), aname, font=f['attr_name'], fill='#0F172A', anchor='lm')
        else:
            draw.text((x+24, cy-1), aname, font=f['attr_name'], fill='#1E293B', anchor='lm')
        cy += rh
    return th

def draw_central_hub(draw, f, cards, name, x, y, w, h, title, subtitle, bullets, theme_color='#1E3A8A'):
    cards[name] = {'x': x, 'y': y, 'w': w, 'h': h}
    
    # Outer drop shadow
    draw.rounded_rectangle([x+8, y+8, x+w+8, y+h+8], radius=18, fill='#94A3B8')
    # Card background
    draw.rounded_rectangle([x, y, x+w, y+h], radius=18, fill='#FFFFFF', outline=theme_color, width=4)
    # Header badge
    draw.rounded_rectangle([x+4, y+4, x+w-4, y+68], radius=14, fill=theme_color)
    draw.text((x + w/2, y + 26), title, font=f['hub_title'], fill='#FFFFFF', anchor='mm')
    draw.text((x + w/2, y + 52), subtitle, font=f['hub_sub'], fill='#93C5FD', anchor='mm')
    
    # Bullets
    cy = y + 100
    for b in bullets:
        draw.text((x + 28, cy), "❖  " + b, font=f['hub_desc'], fill='#0F172A', anchor='lm')
        cy += 36

def draw_sticky_note(draw, f, x, y, w, h, title, bullets, bg_color='#FEF08A', border_color='#CA8A04', header_color='#854D0E'):
    draw.rounded_rectangle([x+6, y+6, x+w+6, y+h+6], radius=10, fill='#CBD5E1')
    draw.rounded_rectangle([x, y, x+w, y+h], radius=10, fill=bg_color, outline=border_color, width=2)
    draw.rectangle([x+16, y+12, x+w-16, y+18], fill=border_color)
    draw.text((x+24, y+38), title, font=f['sticky_title'], fill=header_color, anchor='lm')
    cy = y + 74
    for b in bullets:
        draw.text((x+24, cy), "• " + b, font=f['sticky_body'], fill='#1E293B', anchor='lm')
        cy += 28

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

def draw_connected_arrow(draw, f, cards, from_card, to_card, from_side, to_side, label="", waypoints=None, color='#1E293B'):
    p_start = get_anchor(cards[from_card], from_side)
    p_end = get_anchor(cards[to_card], to_side)
    
    points = [p_start]
    if waypoints:
        points.extend(waypoints)
    else:
        # Default orthogonal elbow routing
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
    
    # Draw polyline
    draw.line(points, fill=color, width=4)
    
    # Draw arrowhead / Crow's foot pointing to p_end
    end_x, end_y = p_end
    prev_x, prev_y = points[-2]
    
    # Draw arrowhead pointing right
    if to_side == 'left' or end_x > prev_x:
        draw.polygon([(end_x, end_y), (end_x-18, end_y-10), (end_x-18, end_y+10)], fill=color)
        draw.line([(end_x-24, end_y-14), (end_x-24, end_y+14)], fill=color, width=3)
    elif to_side == 'right' or end_x < prev_x:
        draw.polygon([(end_x, end_y), (end_x+18, end_y-10), (end_x+18, end_y+10)], fill=color)
        draw.line([(end_x+24, end_y-14), (end_x+24, end_y+14)], fill=color, width=3)
    elif to_side == 'top' or end_y > prev_y:
        draw.polygon([(end_x, end_y), (end_x-10, end_y-18), (end_x+10, end_y-18)], fill=color)
        draw.line([(end_x-14, end_y-24), (end_x+14, end_y-24)], fill=color, width=3)
    elif to_side == 'bottom' or end_y < prev_y:
        draw.polygon([(end_x, end_y), (end_x-10, end_y+18), (end_x+10, end_y+18)], fill=color)
        draw.line([(end_x-14, end_y+24), (end_x+14, end_y+24)], fill=color, width=3)
    
    # Draw label pill in the middle
    if label:
        if len(points) >= 2:
            idx = len(points) // 2
            lx = (points[idx-1][0] + points[idx][0]) / 2
            ly = (points[idx-1][1] + points[idx][1]) / 2
            lw = len(label) * 10 + 26
            draw.rounded_rectangle([lx-lw/2, ly-15, lx+lw/2, ly+15], radius=6, fill='#FFFFFF', outline='#2563EB', width=2)
            draw.text((lx, ly), label, font=f['tag_pill'], fill='#1D4ED8', anchor='mm')

# =============================================================================
# SHEET 1: CORE DEMOGRAPHICS, GOVERNANCE & GRIEVANCES (CENTRAL USERS HUB)
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
        "Demographics, Multi-Role RBAC, Academic Governance & Grievances",
        "Modules 0, 9, 11 & 12 • Fully Normalized to BCNF • High-Contrast Hardcopy Printout"
    )

    # 1. CENTRAL PLATFORM CORE HUB
    draw_central_hub(draw, f, cards, 'Hub_Core', 860, 800, 680, 420,
        "UniChrist Central Core Engine",
        "Demographic Identity & Authentication Hub",
        [
            "Master Users directory validates campus identity.",
            "Dynamic RBAC enforces Role-Based Access Control.",
            "Dispatches authentication tokens across all 12 modules.",
            "Subtype inheritance for Students and Faculty members.",
            "Central foreign key anchor for Audit Logs & Grievances."
        ],
        theme_color='#1E40AF'
    )

    # 2. Roles (Top-Left)
    draw_figma_card(draw, f, cards, 'Roles', 100, 240, 580, [
        ("PK", "role_id (INT)"),
        ("REG", "role_name (VARCHAR 30) UQ"),
        ("REG", "role_description (VARCHAR 150)")
    ], '#1E40AF')

    # 3. Users (Central Auth Table directly inside Hub area)
    draw_figma_card(draw, f, cards, 'Users', 880, 240, 640, [
        ("PK", "user_id (INT)"),
        ("FK", "role_id (INT -> Roles)"),
        ("REG", "register_number (VARCHAR 20) UQ"),
        ("REG", "full_name (VARCHAR 100)"),
        ("REG", "email (VARCHAR 100) UQ"),
        ("REG", "password_hash (VARCHAR 255)"),
        ("REG", "is_active (BOOLEAN DEFAULT TRUE)")
    ], '#1D4ED8')

    # 4. Schools (Top-Right)
    draw_figma_card(draw, f, cards, 'Schools', 1680, 240, 620, [
        ("PK", "school_id (INT)"),
        ("REG", "school_name (VARCHAR 100) UQ"),
        ("REG", "school_dean (VARCHAR 100)")
    ], '#1E40AF')

    # 5. Departments (Mid-Right)
    draw_figma_card(draw, f, cards, 'Departments', 1680, 680, 620, [
        ("PK", "dept_id (INT)"),
        ("FK", "school_id (INT -> Schools)"),
        ("REG", "dept_name (VARCHAR 100) UQ"),
        ("REG", "hod_name (VARCHAR 100)")
    ], '#1D4ED8')

    # 6. Students (Bottom-Left)
    draw_figma_card(draw, f, cards, 'Students', 100, 1420, 600, [
        ("PK,FK", "student_id (INT -> Users)"),
        ("FK", "dept_id (INT -> Depts)"),
        ("REG", "class_section (VARCHAR 10)"),
        ("REG", "semester (INT 1-8)"),
        ("REG", "batch_year (INT >= 2020)")
    ], '#2563EB')

    # 7. Faculties (Bottom-Center)
    draw_figma_card(draw, f, cards, 'Faculties', 880, 1420, 640, [
        ("PK,FK", "faculty_id (INT -> Users)"),
        ("FK", "dept_id (INT -> Depts)"),
        ("REG", "designation (VARCHAR 50)"),
        ("FK", "cabin_room_id (INT -> Rooms)"),
        ("REG", "office_extension (VARCHAR 10)")
    ], '#2563EB')

    # 8. Academic_Resources (Bottom-Right)
    draw_figma_card(draw, f, cards, 'Academic_Resources', 1680, 1420, 620, [
        ("PK", "resource_id (INT)"),
        ("FK", "dept_id (INT -> Depts)"),
        ("FK", "uploaded_by_faculty_id (INT -> Users)"),
        ("REG", "resource_type (CHECK)"),
        ("REG", "course_code (VARCHAR 20)"),
        ("REG", "document_title (VARCHAR 150)"),
        ("REG", "download_count (INT >= 0)")
    ], '#334155')

    # 9. Grievances (Mid-Left)
    draw_figma_card(draw, f, cards, 'Grievances', 100, 780, 600, [
        ("PK", "ticket_id (INT)"),
        ("FK", "student_id (INT -> Users)"),
        ("REG", "category (CHECK)"),
        ("FK", "room_id (INT -> Rooms)"),
        ("REG", "ticket_subject (VARCHAR 150)"),
        ("REG", "priority (CHECK)"),
        ("REG", "status (CHECK)")
    ], '#B91C1C')

    # 10. Grievance_Audit_Logs (Bottom-Far-Left)
    draw_figma_card(draw, f, cards, 'Grievance_Audit_Logs', 100, 2060, 600, [
        ("PK", "log_id (INT)"),
        ("FK", "ticket_id (INT -> Grievances)"),
        ("FK", "changed_by_user_id (INT -> Users)"),
        ("REG", "previous_status (CHECK)"),
        ("REG", "new_status (CHECK)"),
        ("REG", "action_timestamp (TIMESTAMP)")
    ], '#B91C1C')

    # FigJam Sticky Notes
    draw_sticky_note(draw, f, 880, 2060, 640, 310,
        "RBAC & Subtype Architecture",
        [
            "Users entity holds login credentials & role_id.",
            "Students & Faculties inherit user_id via 1:1 subtype.",
            "Enforces polymorphic access control across portal.",
            "Depts link both Students (major) & Faculties (staff).",
            "Referential integrity verified up to Boyce-Codd (BCNF)."
        ],
        bg_color='#EFF6FF', border_color='#3B82F6', header_color='#1E40AF'
    )

    draw_sticky_note(draw, f, 1680, 2060, 620, 310,
        "Grievance Redressal Audit Trail",
        [
            "Students submit facility tickets with room_id.",
            "Status transitions recorded in Grievance_Audit_Logs.",
            "Prevents silent ticket closure or staff tampering.",
            "SLA priorities: LOW, MEDIUM, HIGH, URGENT.",
            "Audit trail guarantees institutional accountability."
        ],
        bg_color='#FEF2F2', border_color='#EF4444', header_color='#991B1B'
    )

    # CONNECTING ARROWS (EDGE-TO-EDGE)
    # Roles -> Users
    draw_connected_arrow(draw, f, cards, 'Roles', 'Users', 'right', 'left', "assigns_role [1:N]")
    # Schools -> Departments
    draw_connected_arrow(draw, f, cards, 'Schools', 'Departments', 'bottom', 'top', "contains [1:N]")
    # Users -> Hub_Core
    draw_connected_arrow(draw, f, cards, 'Users', 'Hub_Core', 'bottom', 'top', "authenticates")
    # Hub_Core -> Students
    draw_connected_arrow(draw, f, cards, 'Hub_Core', 'Students', 'bottom', 'top', "1:1 subtype", waypoints=[(1200, 1340), (400, 1340)])
    # Hub_Core -> Faculties
    draw_connected_arrow(draw, f, cards, 'Hub_Core', 'Faculties', 'bottom', 'top', "1:1 subtype")
    # Departments -> Students
    draw_connected_arrow(draw, f, cards, 'Departments', 'Students', 'bottom', 'right', "enrolled_in [1:N]", waypoints=[(1990, 1380), (700, 1380)])
    # Departments -> Faculties
    draw_connected_arrow(draw, f, cards, 'Departments', 'Faculties', 'bottom', 'right', "employs [1:N]", waypoints=[(1990, 1400), (1520, 1400)])
    # Faculties -> Academic_Resources
    draw_connected_arrow(draw, f, cards, 'Faculties', 'Academic_Resources', 'right', 'left', "uploads [1:N]")
    # Students -> Grievances
    draw_connected_arrow(draw, f, cards, 'Students', 'Grievances', 'top', 'bottom', "files_ticket [1:N]")
    # Grievances -> Grievance_Audit_Logs
    draw_connected_arrow(draw, f, cards, 'Grievances', 'Grievance_Audit_Logs', 'bottom', 'top', "audit_trail [1:N]")

    draw_bottom_footer(draw, f,
        "CHRIST (Deemed to be University) • Department of Computer Science • Course: BCA381-4 • Team 12",
        "Sheet 1: Core Demographics, Governance & Grievances",
        "#1D4ED8"
    )

    out = 'images/erd_part1.png'
    im.save(out, format='PNG', optimize=True)
    print(f"[OK] Rendered Sheet 1 (Spacious 4-Page): {out}")

# =============================================================================
# SHEET 2: SPATIAL DIRECTORY, TIMETABLES & PARKING (CENTRAL SPATIAL HUB)
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
        "Campus Spatial Directory, Faculty Timetables & Smart IoT Parking",
        "Modules 6 & 10 • Fully Normalized to BCNF • High-Contrast Hardcopy Printout"
    )

    # 1. CENTRAL SPATIAL & TIMETABLE HUB
    draw_central_hub(draw, f, cards, 'Hub_Spatial', 860, 800, 680, 440,
        "UniChrist Spatial & Scheduling Engine",
        "Autonomous Faculty Schedule & Navigation Engine",
        [
            "Queries faculty weekly timetables against real-time clock periods.",
            "Dynamically resolves active lecture rooms vs designated staff cabins.",
            "Replaces costly physical Bluetooth hardware beacons with smart DB query.",
            "Enforces composite UNIQUE constraints on (room, day, period).",
            "Coordinates physical campus block coordinates with IoT parking."
        ],
        theme_color='#059669'
    )

    # 2. Campus_Blocks (Top-Center)
    draw_figma_card(draw, f, cards, 'Campus_Blocks', 860, 240, 680, [
        ("PK", "block_id (INT)"),
        ("REG", "block_code (VARCHAR 10) UQ"),
        ("REG", "block_name (VARCHAR 80)"),
        ("REG", "total_floors (INT > 0)"),
        ("REG", "latitude (NUMERIC 10,7)"),
        ("REG", "longitude (NUMERIC 10,7)")
    ], '#059669')

    # 3. Campus_Rooms (Center-Left)
    draw_figma_card(draw, f, cards, 'Campus_Rooms', 100, 780, 640, [
        ("PK", "room_id (INT)"),
        ("FK", "block_id (INT -> Blocks)"),
        ("REG", "room_number (VARCHAR 20)"),
        ("REG", "floor_number (INT >= 0)"),
        ("REG", "room_type (CHECK: LAB, CLASS, CABIN)"),
        ("REG", "seating_capacity (INT >= 0)")
    ], '#059669')

    # 4. Parking_Slots (Center-Right)
    draw_figma_card(draw, f, cards, 'Parking_Slots', 1660, 780, 640, [
        ("PK", "slot_id (INT)"),
        ("FK", "block_id (INT -> Blocks)"),
        ("REG", "slot_code (VARCHAR 20) UQ"),
        ("REG", "vehicle_type (CHECK: 2W, 4W)"),
        ("REG", "is_ev_charging (BOOLEAN)"),
        ("REG", "is_occupied (BOOLEAN)")
    ], '#C2410C')

    # 5. Parking_Logs (Bottom-Right)
    draw_figma_card(draw, f, cards, 'Parking_Logs', 1660, 1440, 640, [
        ("PK", "log_id (INT)"),
        ("FK", "slot_id (INT -> Slots)"),
        ("FK", "user_id (INT -> Users)"),
        ("REG", "vehicle_reg_number (VARCHAR 20)"),
        ("REG", "entry_timestamp (TIMESTAMP)"),
        ("REG", "exit_timestamp (TIMESTAMP)")
    ], '#C2410C')

    # 6. Faculty_Timetables (Bottom-Left)
    draw_figma_card(draw, f, cards, 'Faculty_Timetables', 100, 1440, 660, [
        ("PK", "schedule_id (INT)"),
        ("FK", "faculty_id (INT -> Faculties)"),
        ("REG", "day_of_week (CHECK: MON-SAT)"),
        ("REG", "period_number (INT 1-8)"),
        ("REG", "start_time (TIME) / end_time (TIME)"),
        ("FK", "room_id (INT -> Rooms)"),
        ("REG", "course_code (VARCHAR 20)"),
        ("REG", "class_section (VARCHAR 10)")
    ], '#7C3AED')

    # 7. Faculty_Status_Overrides (Bottom-Center)
    draw_figma_card(draw, f, cards, 'Faculty_Status_Overrides', 860, 1440, 680, [
        ("PK", "override_id (INT)"),
        ("FK", "faculty_id (INT -> Faculties)"),
        ("REG", "override_date (DATE)"),
        ("REG", "start_time (TIME) / end_time (TIME)"),
        ("REG", "status_type (CHECK: LEAVE, MEETING)"),
        ("FK", "assigned_room_id (INT -> Rooms)"),
        ("REG", "notes (VARCHAR 255)")
    ], '#7C3AED')

    # FigJam Sticky Notes
    draw_sticky_note(draw, f, 100, 2120, 660, 310,
        "Timetable BCNF Superkey Rules",
        [
            "{room_id, day, period} -> composite candidate superkey.",
            "{faculty_id, day, period} -> candidate superkey.",
            "Completely eliminates classroom double-booking.",
            "Guarantees a professor cannot be in two rooms at once.",
            "Satisfies BCNF: every determinant is a candidate key."
        ],
        bg_color='#ECFDF5', border_color='#10B981', header_color='#065F46'
    )

    draw_sticky_note(draw, f, 860, 2120, 680, 310,
        "IoT Parking Sensor Telemetry",
        [
            "slot_id mapped to physical Campus_Blocks block_id.",
            "Ultrasonic sensors update is_occupied boolean state.",
            "Boom barrier logs vehicle_reg_number upon entry.",
            "Exit event resets occupancy flag to FALSE dynamically.",
            "Dedicated slots flagged with is_ev_charging indicator."
        ],
        bg_color='#FFF7ED', border_color='#FB923C', header_color='#C2410C'
    )

    # CONNECTING ARROWS (EDGE-TO-EDGE)
    # Campus_Blocks -> Campus_Rooms
    draw_connected_arrow(draw, f, cards, 'Campus_Blocks', 'Campus_Rooms', 'left', 'top', "houses [1:N]", waypoints=[(420, 370)])
    # Campus_Blocks -> Parking_Slots
    draw_connected_arrow(draw, f, cards, 'Campus_Blocks', 'Parking_Slots', 'right', 'top', "allocates [1:N]", waypoints=[(1980, 370)])
    # Campus_Blocks -> Hub_Spatial
    draw_connected_arrow(draw, f, cards, 'Campus_Blocks', 'Hub_Spatial', 'bottom', 'top', "anchors_spatial")
    # Campus_Rooms -> Faculty_Timetables
    draw_connected_arrow(draw, f, cards, 'Campus_Rooms', 'Faculty_Timetables', 'bottom', 'top', "allocated_room [1:N]")
    # Hub_Spatial -> Faculty_Timetables
    draw_connected_arrow(draw, f, cards, 'Hub_Spatial', 'Faculty_Timetables', 'bottom', 'right', "computes_slot", waypoints=[(1200, 1340), (760, 1340), (760, 1560)])
    # Faculty_Timetables -> Faculty_Status_Overrides
    draw_connected_arrow(draw, f, cards, 'Faculty_Timetables', 'Faculty_Status_Overrides', 'right', 'left', "superseded_by [1:N]")
    # Parking_Slots -> Parking_Logs
    draw_connected_arrow(draw, f, cards, 'Parking_Slots', 'Parking_Logs', 'bottom', 'top', "tracks_barrier [1:N]")

    draw_bottom_footer(draw, f,
        "CHRIST (Deemed to be University) • Department of Computer Science • Course: BCA381-4 • Team 12",
        "Sheet 2: Campus Spatial Directory, Faculty Timetables & Smart Parking",
        "#059669"
    )

    out = 'images/erd_part2.png'
    im.save(out, format='PNG', optimize=True)
    print(f"[OK] Rendered Sheet 2 (Spacious 4-Page): {out}")

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
        "Campus Commercial Services: Smart Cafeteria & Campus Bookstore",
        "Modules 1 & 2 • Fully Normalized to BCNF • High-Contrast Hardcopy Printout"
    )

    # 1. CENTRAL COMMERCIAL & ORDER PROCESSING HUB
    draw_central_hub(draw, f, cards, 'Hub_Comm', 860, 800, 680, 440,
        "UniChrist Commercial Platform",
        "Unified Ordering & FIFO Token Management",
        [
            "Handles multi-vendor digital menu browsing and checkout.",
            "Generates daily sequential token_number per vendor stall.",
            "Decomposes M:N transactions into BCNF order item lines.",
            "Tracks order lifecycle: PLACED -> PREPARING -> READY -> PICKED_UP.",
            "Enforces atomic stock decrement to prevent item overselling."
        ],
        theme_color='#B45309'
    )

    # 2. Cafeteria_Vendors (Top-Left)
    draw_figma_card(draw, f, cards, 'Cafeteria_Vendors', 100, 240, 640, [
        ("PK", "vendor_id (INT)"),
        ("REG", "vendor_name (VARCHAR 80)"),
        ("FK", "block_id (INT -> Blocks)"),
        ("REG", "contact_phone (VARCHAR 15)"),
        ("REG", "is_open (BOOLEAN)")
    ], '#B45309')

    # 3. Cafeteria_Items (Mid-Left)
    draw_figma_card(draw, f, cards, 'Cafeteria_Items', 100, 780, 640, [
        ("PK", "item_id (INT)"),
        ("FK", "vendor_id (INT -> Vendors)"),
        ("REG", "item_name (VARCHAR 80)"),
        ("REG", "category (VARCHAR 40)"),
        ("REG", "price (NUMERIC 8,2 >= 0)"),
        ("REG", "is_available (BOOLEAN)"),
        ("REG", "current_stock_qty (INT >= 0)")
    ], '#B45309')

    # 4. Cafeteria_Orders (Lower-Left)
    draw_figma_card(draw, f, cards, 'Cafeteria_Orders', 100, 1440, 640, [
        ("PK", "order_id (INT)"),
        ("FK", "user_id (INT -> Users)"),
        ("FK", "vendor_id (INT -> Vendors)"),
        ("REG", "order_timestamp (TIMESTAMP)"),
        ("REG", "token_number (INT FIFO)"),
        ("REG", "total_amount (NUMERIC 10,2 >= 0)"),
        ("REG", "payment_mode (CHECK)"),
        ("REG", "order_status (CHECK)")
    ], '#B45309')

    # 5. Cafeteria_Order_Items (Bottom-Left)
    draw_figma_card(draw, f, cards, 'Cafeteria_Order_Items', 100, 2100, 640, [
        ("PK", "order_item_id (INT)"),
        ("FK", "order_id (INT -> Orders)"),
        ("FK", "item_id (INT -> Items)"),
        ("REG", "quantity (INT > 0)"),
        ("REG", "unit_price (NUMERIC 8,2)"),
        ("REG", "subtotal (NUMERIC 8,2)")
    ], '#D97706')

    # 6. Store_Categories (Top-Right)
    draw_figma_card(draw, f, cards, 'Store_Categories', 1660, 240, 640, [
        ("PK", "category_id (INT)"),
        ("REG", "category_name (VARCHAR 50) UQ"),
        ("REG", "description (VARCHAR 150)")
    ], '#BE123C')

    # 7. Store_Inventory (Mid-Right)
    draw_figma_card(draw, f, cards, 'Store_Inventory', 1660, 780, 640, [
        ("PK", "product_id (INT)"),
        ("FK", "category_id (INT -> Categories)"),
        ("REG", "product_code (VARCHAR 30) UQ"),
        ("REG", "product_name (VARCHAR 100)"),
        ("REG", "unit_price (NUMERIC 10,2 >= 0)"),
        ("REG", "stock_quantity (INT >= 0)")
    ], '#BE123C')

    # 8. Store_Orders (Lower-Right)
    draw_figma_card(draw, f, cards, 'Store_Orders', 1660, 1440, 640, [
        ("PK", "store_order_id (INT)"),
        ("FK", "user_id (INT -> Users)"),
        ("REG", "order_date (DATE)"),
        ("REG", "total_amount (NUMERIC 10,2 >= 0)"),
        ("REG", "order_status (CHECK)")
    ], '#BE123C')

    # 9. Store_Order_Items (Bottom-Right)
    draw_figma_card(draw, f, cards, 'Store_Order_Items', 1660, 2100, 640, [
        ("PK", "store_order_item_id (INT)"),
        ("FK", "store_order_id (INT -> Orders)"),
        ("FK", "product_id (INT -> Inventory)"),
        ("REG", "quantity (INT > 0)"),
        ("REG", "unit_price (NUMERIC 10,2)"),
        ("REG", "subtotal (NUMERIC 10,2)")
    ], '#E11D48')

    # FigJam Sticky Notes
    draw_sticky_note(draw, f, 860, 1440, 680, 310,
        "FIFO Queue & Stock Consistency",
        [
            "Vendors link to physical Campus_Blocks block_id.",
            "Daily sequential token_number eliminates queuing crowds.",
            "Subtotal verified: quantity * unit_price (redundancy removed).",
            "Atomic transaction updates stock upon checkout completion.",
            "Decomposed M:N relations satisfy BCNF criteria."
        ],
        bg_color='#FEF3C7', border_color='#F59E0B', header_color='#B45309'
    )

    draw_sticky_note(draw, f, 860, 1850, 680, 280,
        "Bookstore & Uniform Issuance",
        [
            "Store_Categories segregates Textbooks, Lab Coats & Blazers.",
            "Store_Inventory manages individual SKU stock_quantity.",
            "Orders booked by authenticated Users (students or parents).",
            "Store_Order_Items maps order lines with verified unit price."
        ],
        bg_color='#FFE4E6', border_color='#FB7185', header_color='#BE123C'
    )

    # CONNECTING ARROWS (EDGE-TO-EDGE)
    # Cafeteria_Vendors -> Cafeteria_Items
    draw_connected_arrow(draw, f, cards, 'Cafeteria_Vendors', 'Cafeteria_Items', 'bottom', 'top', "menus [1:N]")
    # Cafeteria_Vendors -> Cafeteria_Orders
    draw_connected_arrow(draw, f, cards, 'Cafeteria_Vendors', 'Cafeteria_Orders', 'bottom', 'top', "receives [1:N]", waypoints=[(220, 600), (220, 1440)])
    # Hub_Comm -> Cafeteria_Orders
    draw_connected_arrow(draw, f, cards, 'Hub_Comm', 'Cafeteria_Orders', 'left', 'right', "processes_order")
    # Cafeteria_Orders -> Cafeteria_Order_Items
    draw_connected_arrow(draw, f, cards, 'Cafeteria_Orders', 'Cafeteria_Order_Items', 'bottom', 'top', "itemized [1:N]")
    # Cafeteria_Items -> Cafeteria_Order_Items
    draw_connected_arrow(draw, f, cards, 'Cafeteria_Items', 'Cafeteria_Order_Items', 'bottom', 'right', "ordered_in [1:N]", waypoints=[(420, 1350), (740, 1350), (740, 2250)])
    
    # Store_Categories -> Store_Inventory
    draw_connected_arrow(draw, f, cards, 'Store_Categories', 'Store_Inventory', 'bottom', 'top', "classifies [1:N]")
    # Hub_Comm -> Store_Orders
    draw_connected_arrow(draw, f, cards, 'Hub_Comm', 'Store_Orders', 'right', 'left', "processes_payment")
    # Store_Orders -> Store_Order_Items
    draw_connected_arrow(draw, f, cards, 'Store_Orders', 'Store_Order_Items', 'bottom', 'top', "contains [1:N]")
    # Store_Inventory -> Store_Order_Items
    draw_connected_arrow(draw, f, cards, 'Store_Inventory', 'Store_Order_Items', 'bottom', 'left', "sold_in [1:N]", waypoints=[(1980, 1350), (1600, 1350), (1600, 2250)])

    draw_bottom_footer(draw, f,
        "CHRIST (Deemed to be University) • Department of Computer Science • Course: BCA381-4 • Team 12",
        "Sheet 3: Commercial Services & Order Junctions",
        "#B45309"
    )

    out = 'images/erd_part3.png'
    im.save(out, format='PNG', optimize=True)
    print(f"[OK] Rendered Sheet 3 (Spacious 4-Page): {out}")

# =============================================================================
# SHEET 4: WELFARE, SOCIETIES, OPAC & BLUEPRINT LEGEND
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
        "Campus Welfare, Student Societies, Library OPAC & Blueprint Legend",
        "Modules 3, 4, 5, 7 & 8 • Fully Normalized to BCNF • High-Contrast Hardcopy Printout"
    )

    # 1. CENTRAL STUDENT ENGAGEMENT HUB
    draw_central_hub(draw, f, cards, 'Hub_Life', 860, 800, 680, 420,
        "UniChrist Campus Life & Welfare",
        "Student Societies, Health Clinic & OPAC Gateway",
        [
            "Central library book circulation and overdue fine tracking.",
            "First-aid emergency clinic triage and prescription logs.",
            "Campus lost-and-found repository with custody claim receipts.",
            "Student club governance and executive membership rosters.",
            "Campus fests, inter-collegiate event signups and QR passes."
        ],
        theme_color='#A21CAF'
    )

    # 2. Book_Categories (Top-Left)
    draw_figma_card(draw, f, cards, 'Book_Categories', 100, 240, 500, [
        ("PK", "category_id (INT)"),
        ("REG", "category_name (VARCHAR 50) UQ")
    ], '#334155')

    # 3. Library_Books (Top-Center)
    draw_figma_card(draw, f, cards, 'Library_Books', 660, 240, 560, [
        ("PK", "book_id (INT)"),
        ("REG", "isbn (VARCHAR 20) UQ"),
        ("REG", "title (VARCHAR 100)"),
        ("REG", "author (VARCHAR 80)"),
        ("FK", "category_id (INT -> Categories)"),
        ("REG", "total_copies (INT >= 0)"),
        ("REG", "shelf_location (VARCHAR 30)")
    ], '#334155')

    # 4. Library_Circulation (Top-Right)
    draw_figma_card(draw, f, cards, 'Library_Circulation', 1280, 240, 600, [
        ("PK", "issue_id (INT)"),
        ("FK", "book_id (INT -> Books)"),
        ("FK", "user_id (INT -> Users)"),
        ("REG", "issued_date (DATE)"),
        ("REG", "due_date (DATE)"),
        ("REG", "returned_date (DATE)"),
        ("REG", "fine_amount (NUMERIC >= 0)"),
        ("REG", "circulation_status (CHECK)")
    ], '#334155')

    # 5. Medical_Visits (Mid-Left)
    draw_figma_card(draw, f, cards, 'Medical_Visits', 80, 780, 580, [
        ("PK", "visit_id (INT)"),
        ("FK", "student_id (INT -> Users)"),
        ("FK", "attending_staff_id (INT -> Users)"),
        ("REG", "checkin_time (TIMESTAMP)"),
        ("REG", "symptoms_observed (TEXT)"),
        ("REG", "temp_c / bp_systolic"),
        ("REG", "disposition (CHECK)")
    ], '#0E7490')

    # 6. Medical_Prescriptions (Lower-Left)
    draw_figma_card(draw, f, cards, 'Medical_Prescriptions', 80, 1380, 580, [
        ("PK", "prescription_id (INT)"),
        ("FK", "visit_id (INT -> Visits)"),
        ("REG", "medicine_name (VARCHAR 80)"),
        ("REG", "dosage (VARCHAR 30)"),
        ("REG", "quantity_dispensed (INT > 0)"),
        ("REG", "instructions (VARCHAR 150)")
    ], '#0E7490')

    # 7. Lost_Found_Items (Lower-Mid-Left)
    draw_figma_card(draw, f, cards, 'Lost_Found_Items', 720, 1380, 560, [
        ("PK", "item_id (INT)"),
        ("FK", "reported_by_user_id (INT -> Users)"),
        ("REG", "item_title (VARCHAR 100)"),
        ("REG", "category (VARCHAR 40)"),
        ("REG", "photo_url (VARCHAR 200)"),
        ("FK", "found_at_room_id (INT -> Rooms)"),
        ("REG", "status (CHECK)")
    ], '#0F766E')

    # 8. Lost_Found_Claims (Lower-Mid-Right)
    draw_figma_card(draw, f, cards, 'Lost_Found_Claims', 1340, 1380, 560, [
        ("PK", "claim_id (INT)"),
        ("FK", "item_id (INT -> Items)"),
        ("FK", "claimed_by_user_id (INT -> Users)"),
        ("REG", "claim_description (TEXT)"),
        ("REG", "verification_status (CHECK)"),
        ("FK", "handed_over_by (INT -> Users)")
    ], '#0F766E')

    # 9. Student_Clubs (Mid-Right)
    draw_figma_card(draw, f, cards, 'Student_Clubs', 1620, 780, 680, [
        ("PK", "club_id (INT)"),
        ("FK", "school_id (INT -> Schools)"),
        ("REG", "club_name (VARCHAR 80) UQ"),
        ("REG", "club_tagline (VARCHAR 150)"),
        ("FK", "faculty_coordinator_id (INT -> Users)"),
        ("REG", "founded_year (INT >= 1969)")
    ], '#A21CAF')

    # 10. Club_Memberships (Lower-Right)
    draw_figma_card(draw, f, cards, 'Club_Memberships', 1960, 1380, 410, [
        ("PK", "membership_id (INT)"),
        ("FK", "club_id (INT -> Clubs)"),
        ("FK", "student_id (INT -> Users)"),
        ("REG", "joined_date (DATE)"),
        ("REG", "member_role (CHECK: MEMBER, EXEC)")
    ], '#A21CAF')

    # 11. Campus_Events (Bottom-Center-Left)
    draw_figma_card(draw, f, cards, 'Campus_Events', 720, 1920, 580, [
        ("PK", "event_id (INT)"),
        ("FK", "club_id (INT -> Clubs)"),
        ("REG", "event_title (VARCHAR 100)"),
        ("REG", "event_type (CHECK)"),
        ("FK", "venue_room_id (INT -> Rooms)"),
        ("REG", "max_registrations (INT > 0)")
    ], '#A21CAF')

    # 12. Event_Registrations (Bottom-Center-Right)
    draw_figma_card(draw, f, cards, 'Event_Registrations', 1360, 1920, 600, [
        ("PK", "registration_id (INT)"),
        ("FK", "event_id (INT -> Events)"),
        ("FK", "user_id (INT -> Users)"),
        ("REG", "registered_time (TIMESTAMP)"),
        ("REG", "qr_ticket_hash (VARCHAR 128) UQ"),
        ("REG", "has_attended (BOOLEAN)")
    ], '#A21CAF')

    # CONNECTING ARROWS (EDGE-TO-EDGE)
    # Book_Categories -> Library_Books
    draw_connected_arrow(draw, f, cards, 'Book_Categories', 'Library_Books', 'right', 'left', "catalogs [1:N]")
    # Library_Books -> Library_Circulation
    draw_connected_arrow(draw, f, cards, 'Library_Books', 'Library_Circulation', 'right', 'left', "loans [1:N]")
    # Medical_Visits -> Medical_Prescriptions
    draw_connected_arrow(draw, f, cards, 'Medical_Visits', 'Medical_Prescriptions', 'bottom', 'top', "prescribes [1:N]")
    # Lost_Found_Items -> Lost_Found_Claims
    draw_connected_arrow(draw, f, cards, 'Lost_Found_Items', 'Lost_Found_Claims', 'right', 'left', "claims [1:N]")
    # Student_Clubs -> Club_Memberships
    draw_connected_arrow(draw, f, cards, 'Student_Clubs', 'Club_Memberships', 'bottom', 'top', "enrolls [1:N]", waypoints=[(2160, 1300)])
    # Student_Clubs -> Campus_Events
    draw_connected_arrow(draw, f, cards, 'Student_Clubs', 'Campus_Events', 'bottom', 'right', "hosts [1:N]", waypoints=[(1800, 1850), (1300, 1850)])
    # Campus_Events -> Event_Registrations
    draw_connected_arrow(draw, f, cards, 'Campus_Events', 'Event_Registrations', 'right', 'left', "tickets [1:N]")

    # =========================================================================
    # BLUEPRINT NOTATION LEGEND (CRISP HIGH-CONTRAST KEY)
    # =========================================================================
    draw.rounded_rectangle([30, 2520, 2370, 2870], radius=14, fill='#FFFFFF', outline='#334155', width=3)
    draw.text((60, 2548), 'FIGMA / FIGJAM ER DIAGRAM NOTATION KEY & BCNF INTEGRITY ASSURANCE', font=f['legend_hdr'], fill='#0F172A')

    # Badges
    draw.rounded_rectangle([60, 2580, 120, 2615], radius=6, fill='#FEF3C7', outline='#D97706', width=2)
    draw.text((90, 2597), 'PK', font=f['badge'], fill='#92400E', anchor='mm')
    draw.text((135, 2597), 'Primary Key (Entity Identifier)', font=f['legend_body'], fill='#0F172A', anchor='lm')

    draw.rounded_rectangle([520, 2580, 580, 2615], radius=6, fill='#DBEAFE', outline='#2563EB', width=2)
    draw.text((550, 2597), 'FK', font=f['badge'], fill='#1E40AF', anchor='mm')
    draw.text((595, 2597), 'Foreign Key (Referential Constraint)', font=f['legend_body'], fill='#0F172A', anchor='lm')

    draw.rounded_rectangle([980, 2580, 1060, 2615], radius=6, fill='#F3E8FF', outline='#9333EA', width=2)
    draw.text((1020, 2597), 'PK,FK', font=f['badge'], fill='#6B21A8', anchor='mm')
    draw.text((1075, 2597), 'Subtype Entity Key (Inherits Users PK)', font=f['legend_body'], fill='#0F172A', anchor='lm')

    draw.text((60, 2650), '• Crow\'s Foot Cardinality: 1:1, 1:N, and M:N relationships decomposed into associative junction tables with cascade rules.', font=f['legend_body'], fill='#1E293B')
    draw.text((60, 2690), '• BCNF Compliance: All 34 relational entities satisfy Boyce-Codd Normal Form with every determinant as a candidate superkey.', font=f['legend_body'], fill='#1E293B')
    draw.text((60, 2730), '• Live Interactive Figma Canvas: https://www.figma.com/board/13lZxvTOg5Z2wCOcCwvhm5', font=f['sheet_meta'], fill='#1D4ED8')
    draw.text((60, 2770), '• Tool Interoperability: Direct DBML schema export available in UniChrist_Schema.dbml for dbdiagram.io / MySQL Workbench.', font=f['legend_body'], fill='#1E293B')

    draw_bottom_footer(draw, f,
        "CHRIST (Deemed to be University) • Department of Computer Science • Course: BCA381-4 • Team 12",
        "Sheet 4: Student Life, Campus Welfare & Architecture Legend",
        "#A21CAF"
    )

    out = 'images/erd_part4.png'
    im.save(out, format='PNG', optimize=True)
    print(f"[OK] Rendered Sheet 4 (Spacious 4-Page): {out}")

if __name__ == '__main__':
    os.makedirs('images', exist_ok=True)
    generate_sheet1()
    generate_sheet2()
    generate_sheet3()
    generate_sheet4()
