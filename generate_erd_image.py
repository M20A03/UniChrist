#!/usr/bin/env python3
"""
Generate a Figma-style high-resolution Entity-Relationship Diagram (ERD)
for the UniChrist 12-Module Enterprise Architecture (34 BCNF Relational Tables).
Styled with Figma UI design system components: rounded entity cards, color-coded
module frames, pill badges for PK/FK, clean diamond connectors, and metadata bar.
Sized to fit cleanly on a single page.
"""
import os
import shutil
import subprocess

def create_figma_erd():
    w = 2800
    h = 1950
    
    svg = []
    svg.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <defs>
    <style>
      .canvas {{ fill: #F8FAFC; }}
      .grid-dot {{ fill: #E2E8F0; }}
      
      .canvas-title {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 30px; font-weight: 800; fill: #0F172A; text-anchor: middle; letter-spacing: -0.5px; }}
      .canvas-sub {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 14px; fill: #64748B; text-anchor: middle; }}
      .badge-brand {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 11px; font-weight: 700; fill: #2563EB; text-anchor: middle; }}
      
      .module-frame {{ fill: #FFFFFF; stroke: #CBD5E1; stroke-width: 1.5; rx: 10; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.03)); }}
      .module-pill {{ rx: 5; }}
      .module-pill-txt {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 11px; font-weight: 800; fill: #FFFFFF; text-transform: uppercase; letter-spacing: 0.6px; }}
      .module-sub {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 10.5px; fill: #64748B; }}

      .card-body {{ fill: #FFFFFF; stroke: #CBD5E1; stroke-width: 1.2; rx: 6; }}
      .card-hdr {{ rx: 6; }}
      .card-title {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 12px; font-weight: 700; fill: #FFFFFF; text-anchor: middle; }}
      
      .attr-txt {{ font-family: 'Consolas', 'Courier New', monospace; font-size: 10px; fill: #1E293B; }}
      .pk-txt {{ font-weight: bold; fill: #B45309; }}
      .fk-txt {{ fill: #1D4ED8; font-style: italic; }}
      .pkfk-txt {{ font-weight: bold; fill: #7E22CE; }}
      
      .pill-pk {{ fill: #FEF3C7; stroke: #F59E0B; stroke-width: 0.8; rx: 3; }}
      .pill-pk-txt {{ font-family: Arial, sans-serif; font-size: 8.5px; font-weight: bold; fill: #B45309; text-anchor: middle; }}
      
      .pill-fk {{ fill: #DBEAFE; stroke: #3B82F6; stroke-width: 0.8; rx: 3; }}
      .pill-fk-txt {{ font-family: Arial, sans-serif; font-size: 8.5px; font-weight: bold; fill: #1D4ED8; text-anchor: middle; }}
      
      .pill-pkfk {{ fill: #F3E8FF; stroke: #A855F7; stroke-width: 0.8; rx: 3; }}
      .pill-pkfk-txt {{ font-family: Arial, sans-serif; font-size: 8px; font-weight: bold; fill: #7E22CE; text-anchor: middle; }}

      .conn-line {{ stroke: #64748B; stroke-width: 1.6; fill: none; }}
      .rel-diamond {{ fill: #FFFFFF; stroke: #2563EB; stroke-width: 1.2; transform-origin: center; }}
      .rel-txt {{ font-family: Arial, sans-serif; font-size: 8.5px; font-weight: bold; fill: #1E293B; text-anchor: middle; }}
    </style>
  </defs>

  <!-- Canvas Background -->
  <rect width="100%" height="100%" class="canvas"/>

  <!-- Top Figma Frame Header -->
  <g transform="translate(1400, 42)">
    <rect x="-380" y="-28" width="760" height="74" fill="#FFFFFF" stroke="#E2E8F0" rx="8"/>
    <text y="-2" class="canvas-title">UniChrist : Entity-Relationship Diagram (ERD)</text>
    <text y="20" class="canvas-sub">34 Relational Entities &bull; Normalized to BCNF &bull; 12 Functional Modules &bull; BCA381-4 DBMS Project</text>
    <text y="38" class="badge-brand">CHRIST (Deemed to be University) &bull; Dept of Computer Science &bull; Team 12: Mayank Raj, Aslesha Sonti, Aadiya Naresh &bull; Guide: Dr Hemanth K S</text>
  </g>
''')

    # Helper function to draw Figma Entity Card
    def draw_card(x, y, w, title, attrs, hdr_color):
        hh = 22
        rh = 15.5
        bh = len(attrs) * rh + 6
        th = hh + bh
        out = [f'  <g transform="translate({x}, {y})">']
        # Card Body
        out.append(f'    <rect width="{w}" height="{th}" class="card-body"/>')
        # Card Header
        out.append(f'    <rect width="{w}" height="{hh}" class="card-hdr" fill="{hdr_color}"/>')
        out.append(f'    <text x="{w/2}" y="15" class="card-title">{title}</text>')
        # Attribute rows
        cy = hh + 12
        for atype, aname in attrs:
            if 'PK,FK' in atype or 'PK/FK' in atype:
                out.append(f'    <rect x="6" y="{cy-9}" width="30" height="12" class="pill-pkfk"/>')
                out.append(f'    <text x="21" y="{cy}" class="pill-pkfk-txt">PK,FK</text>')
                out.append(f'    <text x="40" y="{cy}" class="attr-txt pkfk-txt">{aname}</text>')
            elif 'PK' in atype:
                out.append(f'    <rect x="6" y="{cy-9}" width="18" height="12" class="pill-pk"/>')
                out.append(f'    <text x="15" y="{cy}" class="pill-pk-txt">PK</text>')
                out.append(f'    <text x="28" y="{cy}" class="attr-txt pk-txt">{aname}</text>')
            elif 'FK' in atype:
                out.append(f'    <rect x="6" y="{cy-9}" width="18" height="12" class="pill-fk"/>')
                out.append(f'    <text x="15" y="{cy}" class="pill-fk-txt">FK</text>')
                out.append(f'    <text x="28" y="{cy}" class="attr-txt fk-txt">{aname}</text>')
            else:
                out.append(f'    <text x="18" y="{cy}" class="attr-txt">{aname}</text>')
            cy += rh
        out.append('  </g>')
        return '\n'.join(out)

    # Helper function to draw Figma Module Frame
    def draw_frame(x, y, w, h, title, sub, pill_color):
        return f'''  <!-- Module Frame: {title} -->
  <rect x="{x}" y="{y}" width="{w}" height="{h}" class="module-frame"/>
  <rect x="{x+12}" y="{y+10}" width="{len(title)*7.5 + 16}" height="18" class="module-pill" fill="{pill_color}"/>
  <text x="{x+20}" y="{y+23}" class="module-pill-txt">{title}</text>
  <text x="{x+20 + len(title)*7.5 + 24}" y="{y+23}" class="module-sub">{sub}</text>'''

    # Layout Grid: 3 Rows
    # ROW 1 (y: 95 to 680)
    # Zone 1: Demographics & Auth (w: 920, h: 575)
    # Zone 2: Spatial & Timetable (w: 920, h: 575)
    # Zone 3: Cafeteria Pre-Ordering (w: 860, h: 575)
    
    # Module 0: Demographics & Auth (Indigo #2563EB)
    svg.append(draw_frame(30, 95, 920, 565, "Module 0: Core Demographics & RBAC", "Authentication, Academic Hierarchy, Subtypes", "#2563EB"))
    svg.append(draw_card(50, 135, 190, "Roles", [("PK", "role_id"), ("REG", "role_name (UQ)"), ("REG", "role_description")], "#1D4ED8"))
    svg.append(draw_card(260, 135, 230, "Users", [("PK", "user_id"), ("FK", "role_id"), ("REG", "register_number (UQ)"), ("REG", "full_name"), ("REG", "email (UQ)"), ("REG", "password_hash"), ("REG", "is_active")], "#1D4ED8"))
    svg.append(draw_card(510, 135, 195, "Schools", [("PK", "school_id"), ("REG", "school_name (UQ)"), ("REG", "school_dean")], "#1D4ED8"))
    svg.append(draw_card(725, 135, 205, "Departments", [("PK", "dept_id"), ("FK", "school_id"), ("REG", "dept_name (UQ)"), ("REG", "hod_name")], "#1D4ED8"))
    svg.append(draw_card(120, 395, 210, "Students", [("PK,FK", "student_id (Users)"), ("FK", "dept_id"), ("REG", "class_section"), ("REG", "semester"), ("REG", "batch_year")], "#3B82F6"))
    svg.append(draw_card(420, 395, 230, "Faculties", [("PK,FK", "faculty_id (Users)"), ("FK", "dept_id"), ("REG", "designation"), ("FK", "cabin_room_id"), ("REG", "office_extension")], "#3B82F6"))

    # Modules 9 & 12: Spatial Directory & Faculty Schedule Engine (Emerald #059669 / Violet #7C3AED)
    svg.append(draw_frame(970, 95, 920, 565, "Modules 9 & 12: Spatial Directory & Faculty Timetables", "Dynamic period timetable & real-time location resolution", "#7C3AED"))
    svg.append(draw_card(990, 135, 200, "Campus_Blocks", [("PK", "block_id"), ("REG", "block_code (UQ)"), ("REG", "block_name"), ("REG", "total_floors"), ("REG", "latitude/longitude")], "#059669"))
    svg.append(draw_card(1210, 135, 215, "Campus_Rooms", [("PK", "room_id"), ("FK", "block_id"), ("REG", "room_number"), ("REG", "floor_number"), ("REG", "room_type"), ("REG", "seating_capacity")], "#059669"))
    svg.append(draw_card(1445, 135, 235, "Faculty_Timetables", [("PK", "schedule_id"), ("FK", "faculty_id"), ("REG", "day_of_week"), ("REG", "period_number"), ("REG", "start/end_time"), ("FK", "room_id"), ("REG", "course_code"), ("REG", "class_section")], "#6D28D9"))
    svg.append(draw_card(1210, 395, 235, "Faculty_Status_Overrides", [("PK", "override_id"), ("FK", "faculty_id"), ("REG", "override_date"), ("REG", "start/end_time"), ("REG", "status_type"), ("FK", "assigned_room_id"), ("REG", "notes")], "#6D28D9"))

    # Module 1: Smart Cafeteria Pre-Ordering (Amber #D97706)
    svg.append(draw_frame(1910, 95, 860, 565, "Module 1: Smart Cafeteria Pre-Ordering", "Counters, live stock menu, digital token queue & bill lines", "#D97706"))
    svg.append(draw_card(1930, 135, 195, "Cafeteria_Vendors", [("PK", "vendor_id"), ("REG", "vendor_name"), ("FK", "block_id"), ("REG", "contact_phone"), ("REG", "is_open")], "#B45309"))
    svg.append(draw_card(2145, 135, 205, "Cafeteria_Items", [("PK", "item_id"), ("FK", "vendor_id"), ("REG", "item_name"), ("REG", "category"), ("REG", "price"), ("REG", "is_available"), ("REG", "stock_qty")], "#B45309"))
    svg.append(draw_card(2370, 135, 205, "Cafeteria_Orders", [("PK", "order_id"), ("FK", "user_id"), ("FK", "vendor_id"), ("REG", "order_time"), ("REG", "token_number"), ("REG", "total_amount"), ("REG", "order_status")], "#B45309"))
    svg.append(draw_card(2145, 395, 205, "Cafeteria_Order_Items", [("PK", "order_item_id"), ("FK", "order_id"), ("FK", "item_id"), ("REG", "quantity"), ("REG", "unit_price"), ("REG", "subtotal")], "#D97706"))

    # ROW 2 (y: 680 to 1240)
    # Zone 4: Bookstore (Module 2) (w: 660, h: 540)
    # Zone 5: Medical Clinic (Module 3) (w: 640, h: 540)
    # Zone 6: Lost & Found (Module 4) (w: 670, h: 540)
    # Zone 7: Library OPAC (Module 5) (w: 750, h: 540)

    # Module 2: Bookstore (Rose #E11D48)
    svg.append(draw_frame(30, 680, 660, 540, "Module 2: Bookstore & Uniforms", "Merchandise, inventory & booking orders", "#E11D48"))
    svg.append(draw_card(50, 720, 180, "Store_Categories", [("PK", "category_id"), ("REG", "category_name (UQ)")], "#BE123C"))
    svg.append(draw_card(250, 720, 215, "Store_Inventory", [("PK", "product_id"), ("FK", "category_id"), ("REG", "product_code (UQ)"), ("REG", "product_name"), ("REG", "unit_price"), ("REG", "stock_qty"), ("REG", "reorder_level")], "#BE123C"))
    svg.append(draw_card(485, 720, 185, "Store_Orders", [("PK", "store_order_id"), ("FK", "user_id"), ("REG", "order_date"), ("REG", "total_amount"), ("REG", "order_status")], "#BE123C"))
    svg.append(draw_card(250, 990, 215, "Store_Order_Items", [("PK", "order_item_id"), ("FK", "store_order_id"), ("FK", "product_id"), ("REG", "quantity"), ("REG", "unit_price"), ("REG", "subtotal")], "#E11D48"))

    # Module 3: Health Clinic (Cyan #0891B2)
    svg.append(draw_frame(710, 680, 640, 540, "Module 3: Health & Medical Room", "Patient check-ins, vitals & prescriptions", "#0891B2"))
    svg.append(draw_card(730, 720, 220, "Medical_Visits", [("PK", "visit_id"), ("FK", "student_id"), ("FK", "attending_staff_id"), ("REG", "checkin_time"), ("REG", "symptoms"), ("REG", "temp/bp"), ("REG", "is_emergency"), ("REG", "disposition")], "#0E7490"))
    svg.append(draw_card(970, 720, 215, "Medical_Prescriptions", [("PK", "prescription_id"), ("FK", "visit_id"), ("REG", "medicine_name"), ("REG", "dosage"), ("REG", "quantity"), ("REG", "instructions")], "#0E7490"))

    # Module 4: Lost & Found (Teal #0D9488)
    svg.append(draw_frame(1370, 680, 670, 540, "Module 4: Lost & Found Vault", "Recovered property, claims & handovers", "#0D9488"))
    svg.append(draw_card(1390, 720, 215, "Lost_Found_Items", [("PK", "item_id"), ("FK", "reported_by_user_id"), ("REG", "item_title"), ("REG", "category"), ("REG", "photo_url"), ("FK", "found_at_room_id"), ("REG", "date_found"), ("REG", "status")], "#0F766E"))
    svg.append(draw_card(1625, 720, 220, "Lost_Found_Claims", [("PK", "claim_id"), ("FK", "item_id"), ("FK", "claimed_by_user_id"), ("REG", "claim_desc"), ("REG", "claim_date"), ("REG", "verification_status"), ("FK", "handed_over_by")], "#0F766E"))

    # Module 5: Library OPAC (Slate #475569)
    svg.append(draw_frame(2060, 680, 710, 540, "Module 5: Centralized Library OPAC", "Cataloging, copies & circulation lending", "#475569"))
    svg.append(draw_card(2080, 720, 175, "Book_Categories", [("PK", "category_id"), ("REG", "category_name (UQ)")], "#334155"))
    svg.append(draw_card(2275, 720, 215, "Library_Books", [("PK", "book_id"), ("REG", "isbn (UQ)"), ("REG", "title"), ("REG", "author"), ("FK", "category_id"), ("REG", "total_copies"), ("REG", "available_copies"), ("REG", "shelf_location")], "#334155"))
    svg.append(draw_card(2510, 720, 220, "Library_Circulation", [("PK", "issue_id"), ("FK", "book_id"), ("FK", "user_id"), ("REG", "issued_date"), ("REG", "due_date"), ("REG", "returned_date"), ("REG", "fine_amount"), ("REG", "status")], "#334155"))

    # ROW 3 (y: 1240 to 1750)
    # Zone 8: Smart Parking (Module 6) (w: 620, h: 480)
    # Zone 9 & 10: Clubs & Events (Modules 7 & 8) (w: 1050, h: 480)
    # Zone 11 & 12: Grievances & Resources (Modules 10 & 11) (w: 1040, h: 480)

    # Module 6: Smart Parking (Orange #EA580C)
    svg.append(draw_frame(30, 1240, 620, 480, "Module 6: Smart Parking Telemetry", "Bay sensors, EV charging & gate logs", "#EA580C"))
    svg.append(draw_card(50, 1280, 200, "Parking_Slots", [("PK", "slot_id"), ("FK", "block_id"), ("REG", "slot_code (UQ)"), ("REG", "vehicle_type"), ("REG", "is_ev_charging"), ("REG", "is_occupied")], "#C2410C"))
    svg.append(draw_card(270, 1280, 210, "Parking_Logs", [("PK", "log_id"), ("FK", "slot_id"), ("FK", "user_id"), ("REG", "vehicle_reg_number"), ("REG", "entry_time"), ("REG", "exit_time")], "#C2410C"))

    # Modules 7 & 8: Clubs & Events (Fuchsia #C026D3)
    svg.append(draw_frame(670, 1240, 1050, 480, "Modules 7 & 8: Student Clubs & Campus Events", "Societies, rosters, fests calendar & QR digital passes", "#C026D3"))
    svg.append(draw_card(690, 1280, 210, "Student_Clubs", [("PK", "club_id"), ("FK", "school_id"), ("REG", "club_name (UQ)"), ("REG", "club_tagline"), ("FK", "faculty_coordinator_id"), ("REG", "founded_year")], "#A21CAF"))
    svg.append(draw_card(920, 1280, 200, "Club_Memberships", [("PK", "membership_id"), ("FK", "club_id"), ("FK", "student_id"), ("REG", "joined_date"), ("REG", "member_role")], "#A21CAF"))
    svg.append(draw_card(1140, 1280, 220, "Campus_Events", [("PK", "event_id"), ("FK", "club_id"), ("REG", "event_title"), ("REG", "event_type"), ("FK", "venue_room_id"), ("REG", "max_registrations")], "#A21CAF"))
    svg.append(draw_card(1380, 1280, 220, "Event_Registrations", [("PK", "registration_id"), ("FK", "event_id"), ("FK", "user_id"), ("REG", "registered_time"), ("REG", "qr_ticket_hash (UQ)"), ("REG", "has_attended")], "#A21CAF"))

    # Modules 10 & 11: Grievance & Academic Resources (Red #DC2626 / Indigo-Gray #475569)
    svg.append(draw_frame(1740, 1240, 1030, 480, "Modules 10 & 11: Grievances & Academic Resources", "Infrastructure issue tickets, SLA audit & syllabus vault", "#DC2626"))
    svg.append(draw_card(1760, 1280, 215, "Grievances", [("PK", "ticket_id"), ("FK", "student_id"), ("REG", "category"), ("FK", "room_id"), ("REG", "ticket_subject"), ("REG", "priority"), ("REG", "status")], "#B91C1C"))
    svg.append(draw_card(1995, 1280, 215, "Grievance_Audit_Logs", [("PK", "log_id"), ("FK", "ticket_id"), ("FK", "changed_by_user_id"), ("REG", "previous_status"), ("REG", "new_status"), ("REG", "action_time")], "#B91C1C"))
    svg.append(draw_card(2230, 1280, 230, "Academic_Resources", [("PK", "resource_id"), ("FK", "dept_id"), ("FK", "uploaded_by_faculty_id"), ("REG", "resource_type"), ("REG", "course_code"), ("REG", "document_title"), ("REG", "download_count")], "#475569"))

    # Connectors & Cardinality
    conns = [
        # (x1, y1, x2, y2, card, mx, my)
        (240, 165, 260, 165, "1:N", 250, 157),
        (705, 165, 725, 165, "1:N", 715, 157),
        (340, 290, 230, 395, "1:1", 285, 342),
        (430, 290, 520, 395, "1:1", 475, 342),
        (1190, 165, 1210, 165, "1:N", 1200, 157),
        (1425, 165, 1445, 165, "1:N", 1435, 157),
        (2125, 165, 2145, 165, "1:N", 2135, 157),
        (2350, 165, 2370, 165, "1:N", 2360, 157),
        (230, 755, 250, 755, "1:N", 240, 747),
        (950, 755, 970, 755, "1:N", 960, 747),
        (1605, 755, 1625, 755, "1:N", 1615, 747),
        (2255, 755, 2275, 755, "1:N", 2265, 747),
        (2490, 755, 2510, 755, "1:N", 2500, 747),
        (250, 1315, 270, 1315, "1:N", 260, 1307),
        (900, 1315, 920, 1315, "1:N", 910, 1307),
        (1120, 1315, 1140, 1315, "1:N", 1130, 1307),
        (1360, 1315, 1380, 1315, "1:N", 1370, 1307),
        (1975, 1315, 1995, 1315, "1:N", 1985, 1307),
    ]

    for x1, y1, x2, y2, card, mx, my in conns:
        svg.append(f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="conn-line"/>')
        svg.append(f'  <polygon points="{mx},{my-7} {mx+11},{my} {mx},{my+7} {mx-11},{my}" class="rel-diamond"/>')
        svg.append(f'  <text x="{mx}" y="{my+3}" class="rel-txt">{card}</text>')

    # Bottom Legend & Status Bar
    svg.append('''
  <g transform="translate(30, 1740)">
    <rect width="2740" height="170" fill="#FFFFFF" stroke="#CBD5E1" rx="8"/>
    <text x="25" y="30" style="font-family: 'Segoe UI', Arial; font-size: 15px; font-weight: 800; fill: #0F172A;">FIGMA-ENGINEERED ER DIAGRAM NOTATION, CARDINALITY &amp; BCNF NORMALIZATION KEY</text>
    
    <g transform="translate(25, 55)">
      <rect x="0" y="0" width="26" height="16" class="pill-pk"/>
      <text x="13" y="12" class="pill-pk-txt">PK</text>
      <text x="35" y="13" style="font-family: 'Segoe UI', Arial; font-size: 12px; fill: #334155;">Primary Key (Unique &amp; Non-Null)</text>

      <rect x="270" y="0" width="26" height="16" class="pill-fk"/>
      <text x="283" y="12" class="pill-fk-txt">FK</text>
      <text x="305" y="13" style="font-family: 'Segoe UI', Arial; font-size: 12px; fill: #334155;">Foreign Key (Referential Integrity Constraint)</text>

      <rect x="620" y="0" width="40" height="16" class="pill-pkfk"/>
      <text x="640" y="12" class="pill-pkfk-txt">PK,FK</text>
      <text x="670" y="13" style="font-family: 'Segoe UI', Arial; font-size: 12px; fill: #334155;">Entity Subtype Primary Key (Inherits Identity)</text>

      <polygon points="1010,8 1021,1 1032,8 1021,15" class="rel-diamond"/>
      <text x="1045" y="13" style="font-family: 'Segoe UI', Arial; font-size: 12px; fill: #334155;"><strong>1:1, 1:N, M:N</strong> Cardinality (M:N decomposed into associative tables)</text>
    </g>

    <text x="25" y="112" style="font-family: 'Segoe UI', Arial; font-size: 12px; fill: #475569;">
      <strong>Boyce-Codd Normal Form (BCNF) Verification:</strong> All 34 entities across the 12 campus modules satisfy BCNF. Every non-trivial functional dependency determinant is a valid Candidate Key.
    </text>
    <text x="25" y="138" style="font-family: 'Segoe UI', Arial; font-size: 12px; font-weight: bold; fill: #2563EB;">
      CHRIST (Deemed to be University) &bull; Department of Computer Science &bull; Course: BCA381-4 (DBMS Project) &bull; Team 12 (Mayank Raj, Aslesha Sonti, Aadiya Naresh) &bull; Guide: Dr Hemanth K S
    </text>
  </g>
</svg>''')

    svg_str = '\n'.join(svg)
    os.makedirs('images', exist_ok=True)
    with open('images/erd_diagram.svg', 'w') as f:
        f.write(svg_str)
    print("[OK] Saved images/erd_diagram.svg")

    html = f'''<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
@page {{ size: 2800px 1950px; margin: 0; }}
body {{ margin: 0; padding: 0; background: #F8FAFC; }}
</style></head><body>{svg_str}</body></html>'''
    with open('/tmp/erd_render.html', 'w') as f:
        f.write(html)
    
    subprocess.run([
        'libreoffice',
        '-env:UserInstallation=file:///tmp/lo_erd_render',
        '--headless',
        '--convert-to', 'pdf',
        '/tmp/erd_render.html',
        '--outdir', '/tmp'
    ], check=True)

    subprocess.run([
        'pdftoppm',
        '-png',
        '-r', '150',
        '/tmp/erd_render.pdf',
        '/tmp/erd_final'
    ], check=True)

    shutil.move('/tmp/erd_final-1.png', 'images/erd_diagram.png')
    print(f"[OK] Rendered Figma-style images/erd_diagram.png ({os.path.getsize('images/erd_diagram.png')} bytes)")

if __name__ == '__main__':
    create_figma_erd()
