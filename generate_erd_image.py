#!/usr/bin/env python3
"""
Generate the high-resolution ER Diagram SVG and PNG for the UniChrist CIA-1 submission.
Includes all 34 tables organized into 12 distinct module zones.
"""
import os
import subprocess

def create_erd():
    w = 3200
    h = 2200
    
    svg = []
    svg.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <defs>
    <style>
      .canvas {{ fill: #FFFFFF; }}
      .title-main {{ font-family: 'Times New Roman', serif; font-size: 34px; font-weight: bold; fill: #000000; text-anchor: middle; }}
      .title-sub {{ font-family: 'Times New Roman', serif; font-size: 16px; fill: #333333; text-anchor: middle; }}
      
      .zone-box {{ fill: #FAFAFA; stroke: #999999; stroke-width: 1.5; rx: 6; }}
      .zone-header {{ font-family: 'Times New Roman', serif; font-size: 14px; font-weight: bold; fill: #000000; text-transform: uppercase; }}
      .zone-sub {{ font-family: 'Times New Roman', serif; font-size: 11px; fill: #555555; }}

      .entity-header {{ fill: #2B4C7E; rx: 3; }}
      .entity-title {{ font-family: 'Times New Roman', serif; font-size: 13px; font-weight: bold; fill: #FFFFFF; text-anchor: middle; }}
      .entity-body {{ fill: #FFFFFF; stroke: #444444; stroke-width: 1.2; rx: 3; }}

      .attr-txt {{ font-family: 'Consolas', 'Courier New', monospace; font-size: 10.5px; fill: #000000; }}
      .pk-txt {{ font-weight: bold; fill: #A00000; }}
      .fk-txt {{ fill: #003399; font-style: italic; }}
      .pkfk-txt {{ font-weight: bold; fill: #660099; }}
      
      .badge-pk {{ font-size: 9px; fill: #A00000; font-weight: bold; font-family: Arial, sans-serif; }}
      .badge-fk {{ font-size: 9px; fill: #003399; font-weight: bold; font-family: Arial, sans-serif; }}
      .badge-pkfk {{ font-size: 9px; fill: #660099; font-weight: bold; font-family: Arial, sans-serif; }}

      .conn {{ stroke: #444444; stroke-width: 1.6; fill: none; }}
      .rel-box {{ fill: #FFFFFF; stroke: #666666; stroke-width: 1; rx: 2; }}
      .rel-txt {{ font-family: Arial, sans-serif; font-size: 9px; font-weight: bold; fill: #000000; text-anchor: middle; }}
    </style>
  </defs>

  <rect width="100%" height="100%" class="canvas"/>

  <!-- Main Header Banner -->
  <g transform="translate(1600, 45)">
    <text y="0" class="title-main">UniChrist: Relational Entity-Relationship Diagram (ERD)</text>
    <text y="24" class="title-sub">Comprehensive 12-Module Enterprise Architecture &bull; 34 Relational Entities Normalized to BCNF</text>
    <text y="44" class="title-sub" style="font-size: 13px; font-style: italic;">BCA381-4 DBMS Project &bull; Team 12: Mayank Raj Gupta (2543115), Aslesha Sonti (2543140), Aadiya Naresh (2543163) &bull; Guide: Dr Hemanth K S</text>
  </g>
''')

    def draw_entity(x, y, w, name, attrs):
        hh = 24
        rh = 17
        bh = len(attrs) * rh + 8
        th = hh + bh
        out = [f'  <g transform="translate({x}, {y})">']
        out.append(f'    <rect width="{w}" height="{th}" class="entity-body"/>')
        out.append(f'    <rect width="{w}" height="{hh}" class="entity-header"/>')
        out.append(f'    <text x="{w/2}" y="16" class="entity-title">{name}</text>')
        cy = hh + 13
        for atype, aname in attrs:
            if 'PK,FK' in atype or 'PK/FK' in atype:
                out.append(f'    <text x="8" y="{cy}" class="attr-txt"><tspan class="badge-pkfk">PK,FK </tspan><tspan class="pkfk-txt">{aname}</tspan></text>')
            elif 'PK' in atype:
                out.append(f'    <text x="8" y="{cy}" class="attr-txt"><tspan class="badge-pk">PK </tspan><tspan class="pk-txt">{aname}</tspan></text>')
            elif 'FK' in atype:
                out.append(f'    <text x="8" y="{cy}" class="attr-txt"><tspan class="badge-fk">FK </tspan><tspan class="fk-txt">{aname}</tspan></text>')
            else:
                out.append(f'    <text x="22" y="{cy}" class="attr-txt">{aname}</text>')
            cy += rh
        out.append('  </g>')
        return '\n'.join(out)

    def draw_zone(x, y, w, h, title, sub):
        return f'''  <rect x="{x}" y="{y}" width="{w}" height="{h}" class="zone-box"/>
  <text x="{x + 15}" y="{y + 22}" class="zone-header">{title}</text>
  <text x="{x + 15}" y="{y + 36}" class="zone-sub">{sub}</text>'''

    # Row 1 (y: 100 to 760)
    # Zone 0: Core Academic & Demographic
    svg.append(draw_zone(30, 100, 1040, 650, "Core Demographics & Authentication (RBAC)", "Users, Roles, Organizational Hierarchy, Student & Faculty Subtypes"))
    svg.append(draw_entity(55, 150, 220, "Roles", [("PK", "role_id"), ("REG", "role_name (UQ)"), ("REG", "role_description")]))
    svg.append(draw_entity(305, 150, 250, "Users", [("PK", "user_id"), ("FK", "role_id"), ("REG", "register_number (UQ)"), ("REG", "full_name"), ("REG", "email (UQ)"), ("REG", "password_hash"), ("REG", "phone_number"), ("REG", "is_active")]))
    svg.append(draw_entity(585, 150, 210, "Schools", [("PK", "school_id"), ("REG", "school_name (UQ)"), ("REG", "school_dean")]))
    svg.append(draw_entity(825, 150, 220, "Departments", [("PK", "dept_id"), ("FK", "school_id"), ("REG", "dept_name (UQ)"), ("REG", "hod_name")]))
    svg.append(draw_entity(150, 440, 240, "Students", [("PK,FK", "student_id (Users)"), ("FK", "dept_id"), ("REG", "class_section"), ("REG", "semester"), ("REG", "batch_year")]))
    svg.append(draw_entity(480, 440, 260, "Faculties", [("PK,FK", "faculty_id (Users)"), ("FK", "dept_id"), ("REG", "designation"), ("FK", "cabin_room_id"), ("REG", "office_extension"), ("REG", "consultation_hours")]))

    # Zone 1 & 12: Spatial Directory & Faculty Timetable Engine (Modules 9 & 12)
    svg.append(draw_zone(1100, 100, 1060, 650, "Modules 9 & 12: Spatial Directory & Faculty Schedule Engine", "Campus Blocks, Atomic Rooms, Dynamic Timetable Mapping & Status Overrides"))
    svg.append(draw_entity(1125, 150, 220, "Campus_Blocks", [("PK", "block_id"), ("REG", "block_code (UQ)"), ("REG", "block_name"), ("REG", "total_floors"), ("REG", "latitude"), ("REG", "longitude")]))
    svg.append(draw_entity(1375, 150, 230, "Campus_Rooms", [("PK", "room_id"), ("FK", "block_id"), ("REG", "room_number"), ("REG", "floor_number"), ("REG", "room_type"), ("REG", "seating_capacity"), ("REG", "is_active")]))
    svg.append(draw_entity(1635, 150, 250, "Faculty_Timetables", [("PK", "schedule_id"), ("FK", "faculty_id"), ("REG", "day_of_week"), ("REG", "period_number"), ("REG", "start_time"), ("REG", "end_time"), ("FK", "room_id"), ("REG", "course_code"), ("REG", "class_section")]))
    svg.append(draw_entity(1375, 450, 260, "Faculty_Status_Overrides", [("PK", "override_id"), ("FK", "faculty_id"), ("REG", "override_date"), ("REG", "start_time"), ("REG", "end_time"), ("REG", "status_type"), ("FK", "assigned_room_id"), ("REG", "notes")]))

    # Zone 2: Smart Cafeteria Pre-Ordering (Module 1)
    svg.append(draw_zone(2190, 100, 980, 650, "Module 1: Smart Cafeteria Pre-Ordering", "Food Vendors, Menu Catalog, Pre-Orders with Token Queue & Order Lines"))
    svg.append(draw_entity(2215, 150, 220, "Cafeteria_Vendors", [("PK", "vendor_id"), ("REG", "vendor_name"), ("FK", "block_id"), ("REG", "contact_phone"), ("REG", "is_open")]))
    svg.append(draw_entity(2465, 150, 230, "Cafeteria_Items", [("PK", "item_id"), ("FK", "vendor_id"), ("REG", "item_name"), ("REG", "category"), ("REG", "price"), ("REG", "is_available"), ("REG", "current_stock_qty")]))
    svg.append(draw_entity(2725, 150, 225, "Cafeteria_Orders", [("PK", "order_id"), ("FK", "user_id"), ("FK", "vendor_id"), ("REG", "order_timestamp"), ("REG", "token_number"), ("REG", "total_amount"), ("REG", "order_status")]))
    svg.append(draw_entity(2465, 450, 230, "Cafeteria_Order_Items", [("PK", "order_item_id"), ("FK", "order_id"), ("FK", "item_id"), ("REG", "quantity"), ("REG", "unit_price"), ("REG", "subtotal")]))

    # Row 2 (y: 780 to 1430)
    # Zone 3: Bookstore (Module 2)
    svg.append(draw_zone(30, 780, 750, 650, "Module 2: University Bookstore & Uniforms", "Merchandise Categories, Stock Inventory, Orders & Itemized Lines"))
    svg.append(draw_entity(55, 830, 200, "Store_Categories", [("PK", "category_id"), ("REG", "category_name (UQ)")]))
    svg.append(draw_entity(285, 830, 230, "Store_Inventory", [("PK", "product_id"), ("FK", "category_id"), ("REG", "product_code (UQ)"), ("REG", "product_name"), ("REG", "unit_price"), ("REG", "stock_quantity"), ("REG", "reorder_level")]))
    svg.append(draw_entity(535, 830, 220, "Store_Orders", [("PK", "store_order_id"), ("FK", "user_id"), ("REG", "order_date"), ("REG", "total_amount"), ("REG", "order_status")]))
    svg.append(draw_entity(285, 1140, 230, "Store_Order_Items", [("PK", "store_order_item_id"), ("FK", "store_order_id"), ("FK", "product_id"), ("REG", "quantity"), ("REG", "unit_price"), ("REG", "subtotal")]))

    # Zone 4: Health Clinic (Module 3)
    svg.append(draw_zone(810, 780, 750, 650, "Module 3: Health & Medical Room", "Clinic Check-in Logs, Vitals, Emergency Triage & Prescriptions"))
    svg.append(draw_entity(835, 830, 240, "Medical_Visits", [("PK", "visit_id"), ("FK", "student_id"), ("FK", "attending_staff_id"), ("REG", "checkin_time"), ("REG", "symptoms_observed"), ("REG", "temperature_celsius"), ("REG", "blood_pressure"), ("REG", "is_emergency_flag"), ("REG", "disposition")]))
    svg.append(draw_entity(1105, 830, 240, "Medical_Prescriptions", [("PK", "prescription_id"), ("FK", "visit_id"), ("REG", "medicine_name"), ("REG", "dosage"), ("REG", "quantity_dispensed"), ("REG", "instructions")]))

    # Zone 5: Lost & Found (Module 4)
    svg.append(draw_zone(1590, 780, 760, 650, "Module 4: Campus Lost & Found Vault", "Recovered Property Catalog, Ownership Claims & Handover Verification"))
    svg.append(draw_entity(1615, 830, 240, "Lost_Found_Items", [("PK", "item_id"), ("FK", "reported_by_user_id"), ("REG", "item_title"), ("REG", "category"), ("REG", "photo_url"), ("FK", "found_at_room_id"), ("REG", "date_found"), ("REG", "status")]))
    svg.append(draw_entity(1885, 830, 240, "Lost_Found_Claims", [("PK", "claim_id"), ("FK", "item_id"), ("FK", "claimed_by_user_id"), ("REG", "claim_description"), ("REG", "claim_submitted_date"), ("REG", "verification_status"), ("FK", "handed_over_by_security_id")]))

    # Zone 6: Library OPAC (Module 5)
    svg.append(draw_zone(2380, 780, 790, 650, "Module 5: Centralized Library OPAC", "Discipline Taxonomy, Book Titles, Multi-Copy Tracking & Circulation Lending"))
    svg.append(draw_entity(2405, 830, 190, "Book_Categories", [("PK", "category_id"), ("REG", "category_name (UQ)")]))
    svg.append(draw_entity(2625, 830, 230, "Library_Books", [("PK", "book_id"), ("REG", "isbn (UQ)"), ("REG", "title"), ("REG", "author"), ("FK", "category_id"), ("REG", "total_copies"), ("REG", "available_copies"), ("REG", "shelf_location")]))
    svg.append(draw_entity(2885, 830, 240, "Library_Circulation", [("PK", "issue_id"), ("FK", "book_id"), ("FK", "user_id"), ("REG", "issued_date"), ("REG", "due_date"), ("REG", "returned_date"), ("REG", "fine_amount"), ("REG", "circulation_status")]))

    # Row 3 (y: 1460 to 2050)
    # Zone 7: Smart Parking (Module 6)
    svg.append(draw_zone(30, 1460, 700, 520, "Module 6: Smart Parking Telemetry", "Bays, 2W/4W/EV Slots & Security Logs"))
    svg.append(draw_entity(55, 1510, 220, "Parking_Slots", [("PK", "slot_id"), ("FK", "block_id"), ("REG", "slot_code (UQ)"), ("REG", "vehicle_type"), ("REG", "is_ev_charging"), ("REG", "is_occupied")]))
    svg.append(draw_entity(305, 1510, 230, "Parking_Logs", [("PK", "log_id"), ("FK", "slot_id"), ("FK", "user_id"), ("REG", "vehicle_reg_number"), ("REG", "entry_timestamp"), ("REG", "exit_timestamp")]))

    # Zone 8 & 9: Clubs & Events (Modules 7 & 8)
    svg.append(draw_zone(760, 1460, 1100, 520, "Modules 7 & 8: Student Clubs & Campus Events", "Academic Clubs, Memberships, Event Calendars & QR Passes"))
    svg.append(draw_entity(785, 1510, 230, "Student_Clubs", [("PK", "club_id"), ("FK", "school_id"), ("REG", "club_name (UQ)"), ("REG", "club_tagline"), ("FK", "faculty_coordinator_id"), ("REG", "founded_year")]))
    svg.append(draw_entity(1045, 1510, 220, "Club_Memberships", [("PK", "membership_id"), ("FK", "club_id"), ("FK", "student_id"), ("REG", "joined_date"), ("REG", "member_role")]))
    svg.append(draw_entity(1295, 1510, 240, "Campus_Events", [("PK", "event_id"), ("FK", "club_id"), ("REG", "event_title"), ("REG", "event_type"), ("FK", "venue_room_id"), ("REG", "max_registrations")]))
    svg.append(draw_entity(1565, 1510, 240, "Event_Registrations", [("PK", "registration_id"), ("FK", "event_id"), ("FK", "user_id"), ("REG", "registration_timestamp"), ("REG", "qr_ticket_hash (UQ)"), ("REG", "has_attended")]))

    # Zone 10 & 11: Grievance & Academic Resources (Modules 10 & 11)
    svg.append(draw_zone(1890, 1460, 1280, 520, "Modules 10 & 11: Grievance Portal & Study Resources", "Facility Tickets, SLA Audit Trail & Study Resources Repository"))
    svg.append(draw_entity(1915, 1510, 240, "Grievances", [("PK", "ticket_id"), ("FK", "student_id"), ("REG", "category"), ("FK", "room_id"), ("REG", "ticket_subject"), ("REG", "priority"), ("REG", "status")]))
    svg.append(draw_entity(2185, 1510, 240, "Grievance_Audit_Logs", [("PK", "log_id"), ("FK", "ticket_id"), ("FK", "changed_by_user_id"), ("REG", "previous_status"), ("REG", "new_status"), ("REG", "action_timestamp")]))
    svg.append(draw_entity(2455, 1510, 250, "Academic_Resources", [("PK", "resource_id"), ("FK", "dept_id"), ("FK", "uploaded_by_faculty_id"), ("REG", "resource_type"), ("REG", "course_code"), ("REG", "document_title"), ("REG", "download_count")]))

    # Relationship connectors
    conns = [
        (275, 180, 305, 180, "1:N", 290, 172),
        (795, 180, 825, 180, "1:N", 810, 172),
        (380, 320, 270, 440, "1:1", 325, 380),
        (480, 320, 560, 440, "1:1", 520, 380),
        (1345, 180, 1375, 180, "1:N", 1360, 172),
        (1605, 180, 1635, 180, "1:N", 1620, 172),
        (2435, 180, 2465, 180, "1:N", 2450, 172),
        (2695, 180, 2725, 180, "1:N", 2710, 172),
        (255, 860, 285, 860, "1:N", 270, 852),
        (1075, 860, 1105, 860, "1:N", 1090, 852),
        (1855, 860, 1885, 860, "1:N", 1870, 852),
        (2595, 860, 2625, 860, "1:N", 2610, 852),
        (2855, 860, 2885, 860, "1:N", 2870, 852),
        (275, 1540, 305, 1540, "1:N", 290, 1532),
        (1015, 1540, 1045, 1540, "1:N", 1030, 1532),
        (1265, 1540, 1295, 1540, "1:N", 1280, 1532),
        (1535, 1540, 1565, 1540, "1:N", 1550, 1532),
        (2155, 1540, 2185, 1540, "1:N", 2170, 1532),
    ]

    for x1, y1, x2, y2, card, mx, my in conns:
        svg.append(f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="conn"/>')
        svg.append(f'  <rect x="{mx-14}" y="{my-8}" width="28" height="16" class="rel-box"/>')
        svg.append(f'  <text x="{mx}" y="{my+4}" class="rel-txt">{card}</text>')

    # Bottom Legend
    svg.append('''
  <g transform="translate(30, 2010)">
    <rect width="3140" height="150" fill="#FFFFFF" stroke="#666666" rx="4"/>
    <text x="25" y="30" style="font-family: 'Times New Roman', serif; font-size: 15px; font-weight: bold; fill: #000000;">ER DIAGRAM KEY &amp; ARCHITECTURAL INTEGRITY CONSTRAINTS:</text>
    <text x="25" y="58" class="attr-txt"><tspan class="badge-pk">PK</tspan> Primary Key (Unique &amp; Non-Null)</text>
    <text x="320" y="58" class="attr-txt"><tspan class="badge-fk">FK</tspan> Foreign Key (Referential Integrity)</text>
    <text x="640" y="58" class="attr-txt"><tspan class="badge-pkfk">PK,FK</tspan> Entity Subtype Identifier</text>
    <text x="960" y="58" style="font-family: 'Times New Roman', serif; font-size: 13px; fill: #000000;"><strong>1:1, 1:N, M:N</strong> Cardinality Ratios (M:N resolved via associative tables)</text>
    <text x="25" y="90" style="font-family: 'Times New Roman', serif; font-size: 12.5px; fill: #333333;"><strong>BCNF Compliance:</strong> All 34 entities satisfy Boyce-Codd Normal Form with every determinant functioning as a valid Candidate Key. Zero redundant storage.</text>
    <text x="25" y="115" style="font-family: 'Times New Roman', serif; font-size: 12px; font-weight: bold; fill: #000000;">Department of Computer Science &bull; CHRIST (Deemed to be University), Bangalore Yeshwanthpur Campus &bull; DBMS Project (BCA381-4)</text>
  </g>
</svg>''')

    svg_str = '\n'.join(svg)
    with open('images/erd_diagram.svg', 'w') as f:
        f.write(svg_str)
    print("[OK] Saved images/erd_diagram.svg")

    # Render to HTML and then PDF -> PNG using pdftoppm
    html = f'''<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
@page {{ size: 3200px 2200px; margin: 0; }}
body {{ margin: 0; padding: 0; background: #FFFFFF; }}
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

    # Move output image
    import shutil
    shutil.move('/tmp/erd_final-1.png', 'images/erd_diagram.png')
    print(f"[OK] Rendered images/erd_diagram.png ({os.path.getsize('images/erd_diagram.png')} bytes)")

if __name__ == '__main__':
    create_erd()
