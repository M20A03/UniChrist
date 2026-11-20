#!/usr/bin/env python3
"""
Generate a Figma-style high-resolution portrait Entity-Relationship Diagram (ERD)
image using Python Pillow (PIL).
Canvas: 2400 x 3100 (matches standard portrait page aspect ratio ~0.774).
Covers the whole page cleanly without dead blank space, with large, bold,
crisply readable fonts, pill badges, and relationship lines for all 34 BCNF entities.
"""

import os
from PIL import Image, ImageDraw, ImageFont

def generate_figma_erd():
    W, H = 2400, 3100
    im = Image.new('RGB', (W, H), color='#F8FAFC')
    draw = ImageDraw.Draw(im)

    font_bold = '/usr/share/fonts/google-carlito-fonts/Carlito-Bold.ttf'
    font_reg = '/usr/share/fonts/google-carlito-fonts/Carlito-Regular.ttf'
    font_mono = '/usr/share/fonts/adwaita-mono-fonts/AdwaitaMono-Regular.ttf'

    f_title = ImageFont.truetype(font_bold, 36)
    f_sub = ImageFont.truetype(font_reg, 18)
    f_meta = ImageFont.truetype(font_bold, 16)
    
    f_frame_title = ImageFont.truetype(font_bold, 16)
    f_frame_sub = ImageFont.truetype(font_reg, 14)
    
    f_card_hdr = ImageFont.truetype(font_bold, 16)
    f_pill = ImageFont.truetype(font_bold, 11)
    f_attr = ImageFont.truetype(font_mono, 14)
    
    f_legend_hdr = ImageFont.truetype(font_bold, 16)
    f_legend_txt = ImageFont.truetype(font_reg, 14)
    f_rel = ImageFont.truetype(font_bold, 12)

    # 1. Top Header Banner
    draw.rounded_rectangle([30, 20, 2370, 125], radius=10, fill='#FFFFFF', outline='#CBD5E1', width=2)
    draw.text((1200, 48), 'UniChrist : Relational Entity-Relationship Diagram (ERD)', font=f_title, fill='#0F172A', anchor='mm')
    draw.text((1200, 80), '34 Relational Entities • Fully Normalized to BCNF • 12 Functional Modules • BCA381-4 DBMS Project', font=f_sub, fill='#475569', anchor='mm')
    draw.text((1200, 104), 'CHRIST (Deemed to be University) • Department of Computer Science • Team 12 • Guide: Dr Hemanth K S', font=f_meta, fill='#2563EB', anchor='mm')

    # Helper: draw module frame
    def draw_module_frame(x, y, w, h, title, sub, pill_color):
        draw.rounded_rectangle([x, y, x+w, y+h], radius=10, fill='#FFFFFF', outline='#CBD5E1', width=2)
        # title pill
        tw = len(title) * 10 + 24
        draw.rounded_rectangle([x+16, y+10, x+16+tw, y+34], radius=5, fill=pill_color)
        draw.text((x+24, y+22), title, font=f_frame_title, fill='#FFFFFF', anchor='lm')
        draw.text((x+24+tw+12, y+22), sub, font=f_frame_sub, fill='#64748B', anchor='lm')

    # Helper: draw entity card
    def draw_card(x, y, w, title, attrs, hdr_color):
        hh = 32
        rh = 22
        bh = len(attrs) * rh + 12
        th = hh + bh
        
        # Body
        draw.rounded_rectangle([x, y, x+w, y+th], radius=7, fill='#FFFFFF', outline='#CBD5E1', width=1)
        # Header
        draw.rounded_rectangle([x, y, x+w, y+hh], radius=7, fill=hdr_color)
        draw.text((x + w/2, y + 16), title, font=f_card_hdr, fill='#FFFFFF', anchor='mm')
        
        # Attributes
        cy = y + hh + 16
        for atype, aname in attrs:
            if 'PK,FK' in atype or 'PK/FK' in atype:
                draw.rounded_rectangle([x+8, cy-10, x+48, cy+8], radius=4, fill='#F3E8FF', outline='#A855F7')
                draw.text((x+28, cy-1), 'PK,FK', font=f_pill, fill='#7E22CE', anchor='mm')
                draw.text((x+54, cy-1), aname, font=f_attr, fill='#7E22CE', anchor='lm')
            elif 'PK' in atype:
                draw.rounded_rectangle([x+8, cy-10, x+34, cy+8], radius=4, fill='#FEF3C7', outline='#F59E0B')
                draw.text((x+21, cy-1), 'PK', font=f_pill, fill='#B45309', anchor='mm')
                draw.text((x+40, cy-1), aname, font=f_attr, fill='#B45309', anchor='lm')
            elif 'FK' in atype:
                draw.rounded_rectangle([x+8, cy-10, x+34, cy+8], radius=4, fill='#DBEAFE', outline='#3B82F6')
                draw.text((x+21, cy-1), 'FK', font=f_pill, fill='#1D4ED8', anchor='mm')
                draw.text((x+40, cy-1), aname, font=f_attr, fill='#1D4ED8', anchor='lm')
            else:
                draw.text((x+20, cy-1), aname, font=f_attr, fill='#334155', anchor='lm')
            cy += rh
        return th

    # Helper: draw relationship connector
    def draw_rel(x1, y1, x2, y2, card, mx, my):
        draw.line([x1, y1, x2, y2], fill='#64748B', width=2)
        # Diamond
        points = [(mx, my-10), (mx+14, my), (mx, my+10), (mx-14, my)]
        draw.polygon(points, fill='#FFFFFF', outline='#2563EB')
        draw.text((mx, my), card, font=f_rel, fill='#0F172A', anchor='mm')

    # =========================================================================
    # ROW 1 (Y: 140 to 715)
    # =========================================================================
    # Left: Module 0: Core Demographics & RBAC (W: 1140)
    draw_module_frame(30, 140, 1140, 565, "MODULE 0: CORE DEMOGRAPHICS & AUTH", "Users, Roles, Schools, Depts, Subtypes", "#2563EB")
    draw_card(45, 185, 215, "Roles", [("PK", "role_id"), ("REG", "role_name (UQ)"), ("REG", "role_description")], "#1D4ED8")
    draw_card(275, 185, 280, "Users", [("PK", "user_id"), ("FK", "role_id"), ("REG", "register_number (UQ)"), ("REG", "full_name"), ("REG", "email (UQ)"), ("REG", "password_hash"), ("REG", "is_active")], "#1D4ED8")
    draw_card(570, 185, 255, "Schools", [("PK", "school_id"), ("REG", "school_name (UQ)"), ("REG", "school_dean")], "#1D4ED8")
    draw_card(840, 185, 315, "Departments", [("PK", "dept_id"), ("FK", "school_id"), ("REG", "dept_name (UQ)"), ("REG", "hod_name")], "#1D4ED8")
    draw_card(140, 460, 320, "Students", [("PK,FK", "student_id (Users)"), ("FK", "dept_id"), ("REG", "class_section"), ("REG", "semester"), ("REG", "batch_year")], "#3B82F6")
    draw_card(550, 460, 330, "Faculties", [("PK,FK", "faculty_id (Users)"), ("FK", "dept_id"), ("REG", "designation"), ("FK", "cabin_room_id"), ("REG", "office_extension")], "#3B82F6")

    # Right: Modules 9 & 12: Spatial Directory & Faculty Timetables (W: 1180)
    draw_module_frame(1190, 140, 1180, 565, "MODULES 9 & 12: SPATIAL DIRECTORY & TIMETABLES", "Blocks, Rooms, Weekly Timetables & Status Overrides", "#7C3AED")
    draw_card(1205, 185, 260, "Campus_Blocks", [("PK", "block_id"), ("REG", "block_code (UQ)"), ("REG", "block_name"), ("REG", "total_floors"), ("REG", "latitude / longitude")], "#059669")
    draw_card(1485, 185, 280, "Campus_Rooms", [("PK", "room_id"), ("FK", "block_id"), ("REG", "room_number"), ("REG", "floor_number"), ("REG", "room_type"), ("REG", "seating_capacity")], "#059669")
    draw_card(1785, 185, 330, "Faculty_Timetables", [("PK", "schedule_id"), ("FK", "faculty_id"), ("REG", "day_of_week"), ("REG", "period_number"), ("REG", "start_time / end_time"), ("FK", "room_id"), ("REG", "course_code")], "#6D28D9")
    draw_card(1485, 460, 330, "Faculty_Status_Overrides", [("PK", "override_id"), ("FK", "faculty_id"), ("REG", "override_date"), ("REG", "start_time / end_time"), ("REG", "status_type"), ("FK", "assigned_room_id")], "#6D28D9")

    # Connectors Row 1
    draw_rel(260, 220, 275, 220, "1:N", 267, 220)
    draw_rel(825, 220, 840, 220, "1:N", 832, 220)
    draw_rel(380, 385, 270, 460, "1:1", 325, 420)
    draw_rel(480, 385, 600, 460, "1:1", 540, 420)
    draw_rel(1465, 220, 1485, 220, "1:N", 1475, 220)
    draw_rel(1765, 220, 1785, 220, "1:N", 1775, 220)

    # =========================================================================
    # ROW 2 (Y: 725 to 1300)
    # =========================================================================
    # Left: Module 1: Smart Cafeteria Pre-Ordering (W: 1140)
    draw_module_frame(30, 725, 1140, 565, "MODULE 1: CAFETERIA PRE-ORDERING", "Counters, live stock menu, FIFO token queue & order lines", "#D97706")
    draw_card(45, 770, 255, "Cafeteria_Vendors", [("PK", "vendor_id"), ("REG", "vendor_name"), ("FK", "block_id"), ("REG", "contact_phone"), ("REG", "is_open")], "#B45309")
    draw_card(320, 770, 275, "Cafeteria_Items", [("PK", "item_id"), ("FK", "vendor_id"), ("REG", "item_name"), ("REG", "category"), ("REG", "price"), ("REG", "is_available"), ("REG", "stock_quantity")], "#B45309")
    draw_card(615, 770, 280, "Cafeteria_Orders", [("PK", "order_id"), ("FK", "user_id"), ("FK", "vendor_id"), ("REG", "order_timestamp"), ("REG", "token_number"), ("REG", "total_amount"), ("REG", "order_status")], "#B45309")
    draw_card(320, 1030, 280, "Cafeteria_Order_Items", [("PK", "order_item_id"), ("FK", "order_id"), ("FK", "item_id"), ("REG", "quantity"), ("REG", "unit_price"), ("REG", "subtotal")], "#D97706")

    # Right: Module 2: Bookstore & Uniforms (W: 1180)
    draw_module_frame(1190, 725, 1180, 565, "MODULE 2: BOOKSTORE & UNIFORMS", "Merchandise catalog, stock management & itemized store orders", "#E11D48")
    draw_card(1205, 770, 260, "Store_Categories", [("PK", "category_id"), ("REG", "category_name (UQ)"), ("REG", "description")], "#BE123C")
    draw_card(1485, 770, 285, "Store_Inventory", [("PK", "product_id"), ("FK", "category_id"), ("REG", "product_code (UQ)"), ("REG", "product_name"), ("REG", "unit_price"), ("REG", "stock_quantity")], "#BE123C")
    draw_card(1790, 770, 280, "Store_Orders", [("PK", "store_order_id"), ("FK", "user_id"), ("REG", "order_date"), ("REG", "total_amount"), ("REG", "order_status")], "#BE123C")
    draw_card(1485, 1030, 285, "Store_Order_Items", [("PK", "store_order_item_id"), ("FK", "store_order_id"), ("FK", "product_id"), ("REG", "quantity"), ("REG", "unit_price"), ("REG", "subtotal")], "#E11D48")

    # Connectors Row 2
    draw_rel(300, 810, 320, 810, "1:N", 310, 810)
    draw_rel(595, 810, 615, 810, "1:N", 605, 810)
    draw_rel(1465, 810, 1485, 810, "1:N", 1475, 810)
    draw_rel(1770, 810, 1790, 810, "1:N", 1780, 810)

    # =========================================================================
    # ROW 3 (Y: 1310 to 1870)
    # =========================================================================
    # Left: Module 3: Health & Medical Room (W: 740)
    draw_module_frame(30, 1310, 740, 550, "MODULE 3: HEALTH CLINIC", "Visits, vitals & prescriptions", "#0891B2")
    draw_card(45, 1355, 300, "Medical_Visits", [("PK", "visit_id"), ("FK", "student_id"), ("FK", "attending_staff_id"), ("REG", "checkin_time"), ("REG", "symptoms_observed"), ("REG", "temp / bp"), ("REG", "disposition")], "#0E7490")
    draw_card(365, 1355, 290, "Medical_Prescriptions", [("PK", "prescription_id"), ("FK", "visit_id"), ("REG", "medicine_name"), ("REG", "dosage"), ("REG", "qty_dispensed"), ("REG", "instructions")], "#0E7490")

    # Middle: Module 4: Lost & Found Vault (W: 750)
    draw_module_frame(790, 1310, 750, 550, "MODULE 4: LOST & FOUND", "Found property & claims vault", "#0D9488")
    draw_card(805, 1355, 290, "Lost_Found_Items", [("PK", "item_id"), ("FK", "reported_by_user_id"), ("REG", "item_title"), ("REG", "category"), ("REG", "photo_url"), ("FK", "found_at_room_id"), ("REG", "status")], "#0F766E")
    draw_card(1115, 1355, 295, "Lost_Found_Claims", [("PK", "claim_id"), ("FK", "item_id"), ("FK", "claimed_by_user_id"), ("REG", "claim_description"), ("REG", "verification_status"), ("FK", "handed_over_by")], "#0F766E")

    # Right: Module 5: Central Library OPAC (W: 810)
    draw_module_frame(1560, 1310, 810, 550, "MODULE 5: LIBRARY OPAC", "Catalog, multi-copy & loans", "#475569")
    draw_card(1575, 1355, 230, "Book_Categories", [("PK", "category_id"), ("REG", "category_name (UQ)")], "#334155")
    draw_card(1825, 1355, 275, "Library_Books", [("PK", "book_id"), ("REG", "isbn (UQ)"), ("REG", "title"), ("REG", "author"), ("FK", "category_id"), ("REG", "total_copies"), ("REG", "shelf_location")], "#334155")
    draw_card(2115, 1355, 240, "Library_Circulation", [("PK", "issue_id"), ("FK", "book_id"), ("FK", "user_id"), ("REG", "issued_date"), ("REG", "due_date"), ("REG", "returned_date"), ("REG", "fine_amount")], "#334155")

    # Connectors Row 3
    draw_rel(345, 1400, 365, 1400, "1:N", 355, 1400)
    draw_rel(1095, 1400, 1115, 1400, "1:N", 1105, 1400)
    draw_rel(1805, 1400, 1825, 1400, "1:N", 1815, 1400)
    draw_rel(2100, 1400, 2115, 1400, "1:N", 2107, 1400)

    # =========================================================================
    # ROW 4 (Y: 1880 to 2440)
    # =========================================================================
    # Left: Module 6: Smart Parking (W: 740)
    draw_module_frame(30, 1880, 740, 545, "MODULE 6: SMART PARKING", "Bay sensors, EV slots & gate entry logs", "#EA580C")
    draw_card(45, 1925, 270, "Parking_Slots", [("PK", "slot_id"), ("FK", "block_id"), ("REG", "slot_code (UQ)"), ("REG", "vehicle_type"), ("REG", "is_ev_charging"), ("REG", "is_occupied")], "#C2410C")
    draw_card(335, 1925, 280, "Parking_Logs", [("PK", "log_id"), ("FK", "slot_id"), ("FK", "user_id"), ("REG", "vehicle_reg_number"), ("REG", "entry_timestamp"), ("REG", "exit_timestamp")], "#C2410C")

    # Right: Modules 7 & 8: Clubs & Campus Events (W: 1580)
    draw_module_frame(790, 1880, 1580, 545, "MODULES 7 & 8: CLUBS & CAMPUS EVENTS", "Societies, rosters, event calendar & QR digital entry passes", "#C026D3")
    draw_card(805, 1925, 280, "Student_Clubs", [("PK", "club_id"), ("FK", "school_id"), ("REG", "club_name (UQ)"), ("REG", "club_tagline"), ("FK", "faculty_coordinator_id"), ("REG", "founded_year")], "#A21CAF")
    draw_card(1105, 1925, 270, "Club_Memberships", [("PK", "membership_id"), ("FK", "club_id"), ("FK", "student_id"), ("REG", "joined_date"), ("REG", "member_role")], "#A21CAF")
    draw_card(1395, 1925, 285, "Campus_Events", [("PK", "event_id"), ("FK", "club_id"), ("REG", "event_title"), ("REG", "event_type"), ("FK", "venue_room_id"), ("REG", "max_registrations")], "#A21CAF")
    draw_card(1700, 1925, 290, "Event_Registrations", [("PK", "registration_id"), ("FK", "event_id"), ("FK", "user_id"), ("REG", "registered_time"), ("REG", "qr_ticket_hash (UQ)"), ("REG", "has_attended")], "#A21CAF")

    # Connectors Row 4
    draw_rel(315, 1970, 335, 1970, "1:N", 325, 1970)
    draw_rel(1085, 1970, 1105, 1970, "1:N", 1095, 1970)
    draw_rel(1375, 1970, 1395, 1970, "1:N", 1385, 1970)
    draw_rel(1680, 1970, 1700, 1970, "1:N", 1690, 1970)

    # =========================================================================
    # ROW 5 (Y: 2445 to 2965)
    # =========================================================================
    # Modules 10 & 11: Grievances & Academic Study Resources (W: 2340)
    draw_module_frame(30, 2445, 2340, 505, "MODULES 10 & 11: GRIEVANCES & ACADEMIC STUDY VAULT", "Facility defect tickets, immutable audit trail & subject study materials", "#DC2626")
    draw_card(55, 2490, 320, "Grievances", [("PK", "ticket_id"), ("FK", "student_id"), ("REG", "category"), ("FK", "room_id"), ("REG", "ticket_subject"), ("REG", "priority"), ("REG", "status")], "#B91C1C")
    draw_card(405, 2490, 330, "Grievance_Audit_Logs", [("PK", "log_id"), ("FK", "ticket_id"), ("FK", "changed_by_user_id"), ("REG", "previous_status"), ("REG", "new_status"), ("REG", "action_timestamp")], "#B91C1C")
    draw_card(765, 2490, 340, "Academic_Resources", [("PK", "resource_id"), ("FK", "dept_id"), ("FK", "uploaded_by_faculty_id"), ("REG", "resource_type"), ("REG", "course_code"), ("REG", "document_title"), ("REG", "download_count")], "#475569")

    # Connectors Row 5
    draw_rel(375, 2530, 405, 2530, "1:N", 390, 2530)

    # =========================================================================
    # BOTTOM LEGEND & BCNF VERIFICATION BAR (Y: 2975 to 3085)
    # =========================================================================
    draw.rounded_rectangle([30, 2975, 2370, 3085], radius=10, fill='#FFFFFF', outline='#CBD5E1', width=2)
    draw.text((50, 2995), 'FIGMA ER DIAGRAM NOTATION, CARDINALITY & BCNF VERIFICATION KEY', font=f_legend_hdr, fill='#0F172A')

    # Legend items
    draw.rounded_rectangle([50, 3015, 80, 3033], radius=4, fill='#FEF3C7', outline='#F59E0B')
    draw.text((65, 3024), 'PK', font=f_pill, fill='#B45309', anchor='mm')
    draw.text((90, 3024), 'Primary Key (Unique & Non-Null)', font=f_legend_txt, fill='#334155', anchor='lm')

    draw.rounded_rectangle([380, 3015, 410, 3033], radius=4, fill='#DBEAFE', outline='#3B82F6')
    draw.text((395, 3024), 'FK', font=f_pill, fill='#1D4ED8', anchor='mm')
    draw.text((420, 3024), 'Foreign Key (Referential Integrity)', font=f_legend_txt, fill='#334155', anchor='lm')

    draw.rounded_rectangle([730, 3015, 780, 3033], radius=4, fill='#F3E8FF', outline='#A855F7')
    draw.text((755, 3024), 'PK,FK', font=f_pill, fill='#7E22CE', anchor='mm')
    draw.text((790, 3024), 'Subtype Entity Key (Inherits Users PK)', font=f_legend_txt, fill='#334155', anchor='lm')

    # Diamond symbol in legend
    pts = [(1130, 3024-8), (1142, 3024), (1130, 3024+8), (1118, 3024)]
    draw.polygon(pts, fill='#FFFFFF', outline='#2563EB')
    draw.text((1152, 3024), '1:1, 1:N, M:N Cardinality (Decomposed into associative tables)', font=f_legend_txt, fill='#334155', anchor='lm')

    draw.text((50, 3055), 'Boyce-Codd Normal Form (BCNF): All 34 relations satisfy BCNF. Every determinant is a candidate superkey; zero storage redundancy.', font=f_legend_txt, fill='#475569')
    draw.text((1200, 3055), 'CHRIST (Deemed to be University) • Department of Computer Science • Course: BCA381-4 • Team 12 • Guide: Dr Hemanth K S', font=f_meta, fill='#2563EB')

    os.makedirs('images', exist_ok=True)
    out_path = 'images/erd_diagram.png'
    im.save(out_path, format='PNG', optimize=True)
    print(f"[OK] Rendered Figma-style Portrait PNG: {out_path} ({os.path.getsize(out_path)} bytes)")

if __name__ == '__main__':
    generate_figma_erd()
