# CHRIST (Deemed to be University)
### Department of Computer Science — Bangalore Yeshwanthpur Campus
### DBMS PROJECT (BCA381-4) — ASSESSMENT-1 SUBMISSION
## PROJECT SYNOPSIS & SOFTWARE REQUIREMENT SPECIFICATION (SRS)

---

### Project Process Flow | Initial Review and Guide Discussion
* **Course / Class:** 4BCA-B | Course Code: BCA381-4 (DBMS Project)
* **Project Title:** **UniChrist: Integrated Campus Life & Location Services Portal**
* **Team Members:**
  1. **Mayank Raj Gupta** (Register No: 2543115) — *Database design, table schema, SQL scripts & backend logic*
  2. **Sonti Sri Lakshmi Aslesha** (Register No: 2543140) — *Schema Normalization (1NF to BCNF), constraints, views & queries*
  3. **Aadiya Naresh** (Register No: 2543163) — *System analysis, UI flow, test cases & documentation*
* **Project Guide Name:** **Dr Hemanth K S** (Associate Professor, Department of Computer Science)
* **Academic Year:** 2025 – 2029 (Semester IV)
* **Date of Submission:** November 2026

---

# Section 1: Team Details & Project Metadata

| S.No | Student Name | Register Number | Role in Project |
| :---: | :--- | :---: | :--- |
| **1** | **Mayank Raj Gupta** | **2543115** | **Team Lead**: Database design, table schema, SQL scripts and backend logic |
| **2** | **Sonti Sri Lakshmi Aslesha** | **2543140** | **Schema Normalization**: (1NF to BCNF), constraints, views and queries |
| **3** | **Aadiya Naresh** | **2543163** | **System Analyst**: UI flow, test cases and documentation |

* **Course Code & Title:** BCA381-4 — DBMS Project
* **Class:** 4BCA-B
* **Project Guide:** Dr Hemanth K S (Associate Professor, Department of Computer Science)
* **Academic Year:** 2025 – 2029

---

# Section 2: Chosen Application Domain & Problem Statement

* **Chosen Domain:** Smart Campus Management & Schedule-Based Location Services System
* **Why we chose this project:** As students at the Bangalore Yeshwanthpur campus, our team experiences everyday friction because different campus facilities run on separate, unlinked methods. Some use paper books, some use independent counters, and some rely on word of mouth. Specifically:
  1. **Finding Teachers:** Students spend 15 to 25 minutes walking across Block A and Block B staff rooms trying to find a teacher during free hours, only to realize the teacher is currently taking a lecture in a classroom, conducting a practical lab, or attending a meeting. Live sensor/biometric tracking across campus is difficult to implement and maintain.
  2. **Cafeteria Lines:** During our 20-minute morning and lunch breaks, students crowd food counters just to place an order, leaving hardly any time to eat.
  3. **Scattered Services:** The bookstore, uniform desk, campus health room, lost & found counter, and parking spots all keep separate logbooks with no live lookup.
  4. **Maintenance Complaints:** When Wi-Fi drops in lab workstations or classroom projectors malfunction, complaints written in physical logbooks get delayed or forgotten with no status update.
  5. **Finding Rooms:** New students and visitors frequently get confused trying to find specific labs, seminar halls, and faculty cabins across floors.
* **Proposed Solution (Guide-Approved Approach):** Based on feedback from our guide Dr Hemanth K S, tracking teachers with physical biometric hardware scanners everywhere is technically difficult and impractical. Instead, UniChrist integrates the official university faculty timetable into the database. When a student searches for a teacher, the system automatically checks the current day and time against the teacher's schedule. If the teacher has a class or lab, the app displays their active room number (e.g. 'In Class: DBMS Lab, Block B Lab 201'). If the teacher has a free hour, the app directs the student to their designated staff room/cabin (e.g. 'Free / Consultation — Staff Room 304').

---

# Section 3: Business & Application Objectives

Our project aims to achieve the following 6 practical objectives:
1. **Centralized Database:** Design and build a clean relational database normalized up to BCNF that brings 12 essential campus services together without duplicate records.
2. **Automated Timetable-Based Location Engine:** Build an intelligent schedule-matching database engine that checks the faculty timetable against the current clock: showing the classroom/lab during lecture hours, or the staff room during free hours.
3. **Online Cafeteria Pre-Ordering:** Allow students to view the live canteen menu, place food orders ahead of time, get a digital token number, and automatically reduce available kitchen stock.
4. **Campus Utility Tracking:** Digitize the health room visit logs, lost-and-found claims, and block-wise vehicle parking slot counts.
5. **Trackable Grievance Ticketing:** Build a complaint portal where student issues follow a clear status lifecycle (`Pending` -> `Assigned` -> `In-Progress` -> `Resolved`) with timestamps.
6. **Multi-Floor Room Directory:** Provide a simple floor-by-floor campus map where users click a block and floor number to find any classroom, lab, or seminar hall.

---

# Section 4: Detailed Module Breakdown (All 12 Modules)

| Module No. | Campus Service | Main Database Tables | What This Module Does |
| :---: | :--- | :--- | :--- |
| **1** | Cafeteria Ordering | `Cafeteria_Vendors`, `Items`, `Orders`, `Order_Items` | Menu browsing, pre-ordering, token generation, kitchen queue, live stock update. |
| **2** | Bookstore & Store | `Store_Categories`, `Store_Inventory`, `Store_Orders` | Checks textbook & uniform stock, allows booking, creates digital receipt. |
| **3** | Medical Room | `Medical_Visits`, `Medical_Prescriptions` | Logs student check-ins, duty doctor hours, first-aid alerts, medicine records. |
| **4** | Lost & Found | `Lost_Found_Items`, `Lost_Found_Claims` | Uploads photos of found items, collects claims, logs security handovers. |
| **5** | Library OPAC | `Book_Categories`, `Library_Books`, `Circulation` | Book searches, issue/return dates, reading desk bookings, overdue fine calculation. |
| **6** | Smart Parking | `Parking_Slots`, `Parking_Logs` | Shows free 2-wheeler, 4-wheeler, and EV charging slots; logs security gate entry. |
| **7** | Campus Events | `Campus_Events`, `Event_Registrations` | Central calendar for college fests and workshops, student signups, digital passes. |
| **8** | College Clubs | `Student_Clubs`, `Club_Memberships` | Lists clubs under Sciences, Commerce, Arts & Management; manages member lists. |
| **9** | Teacher Schedule & Location | `Faculty_Timetables`, `Faculties`, `Campus_Rooms` | Fetches period schedule: shows current class room; if free, shows staff room. |
| **10** | Grievance Portal | `Grievances`, `Grievance_Audit_Logs` | Students log Wi-Fi, lab, or classroom issues; tracks fix status with staff notes. |
| **11** | Study Resources | `Academic_Resources` | Searchable repository for syllabus copies, past exam question papers (PYQs), lab manuals. |
| **12** | Campus Map | `Campus_Blocks`, `Campus_Rooms` | Interactive directory: pick block and floor to see all classrooms, labs & halls. |

---

# Section 5: Existing System vs. Proposed UniChrist System

| Campus Service | How It Is Done Right Now | Problems with Current Method | How UniChrist Fixes It |
| :--- | :--- | :--- | :--- |
| **Finding Faculty** | Walking to staff rooms, asking classmates or peons | Wasted time, teachers often in another class or meeting | Checks faculty timetable: shows active classroom during lectures, or staff room if free. |
| **Canteen Orders** | Standing in long queues, paying at counter, paper slips | Crowded counters, 20-min breaks wasted, food items run out | Pre-order on phone, get token number, collect food when ready. |
| **Lost & Found** | Paper book kept at the main security guard post | Students don't know items were found; items sit unclaimed | Students browse photos of found items online and verify ownership. |
| **Complaints** | Handwritten register in maintenance office or verbal complaints | Complaints get lost, no record of who is fixing it or when | Digital ticket with timestamp; shows Pending, In-Progress or Resolved. |
| **Campus Directions** | Looking at wall signboards or asking security guards | Hard to locate specific computer labs and seminar halls across floors | Clean map interface: select Block -> Floor to see exact room numbers. |

---

# Section 6: Feasibility Study

| Feasibility Area | What We Examined | Our Findings & Project Reality |
| :--- | :--- | :--- |
| **Technical** | Database software, programming tools, hardware requirements | **FEASIBLE:** Timetable lookup is much more reliable and feasible than expensive biometric hardware. The database queries `Faculty_Timetables` with current day and time to return the room in milliseconds. Built with PostgreSQL / SQL Server and .NET. |
| **Operational** | Ease of use for students, teachers, cafeteria staff and security | **FEASIBLE:** All students and teachers already carry smartphones. The screens are simple and easy to understand. Each user type (student, teacher, canteen vendor, security guard) only sees options relevant to them. |
| **Economic** | Development costs, software licenses, operational expenses | **FEASIBLE:** By using the database timetable engine instead of installing physical RFID/biometric readers at every door, hardware costs are eliminated. We use free, open-source DBMS tools available in university labs. |
| **Behavioural** | Teacher privacy, student willingness, campus regulations | **FEASIBLE:** Uses only official university timetable data already published by departments. Zero privacy concerns because it reflects public academic schedules, not personal physical tracking. |

---

# Section 7: Software Requirement Specifications — Functional Requirements

| Req ID | Priority | Module | System Action & What It Does |
| :---: | :---: | :--- | :--- |
| **FR-01** | High | Login & Roles | Verify university user credentials and grant access according to role (Student, Faculty, Vendor, Medical, Admin). |
| **FR-02** | High | Timetable Storage | Store weekly period schedules for all faculty members (day of week, start time, end time, room ID, subject code, class section). |
| **FR-03** | High | Teacher Location | Fetch current time and match with teacher timetable: if in class, show classroom/lab; if free, show designated staff room. |
| **FR-04** | High | Canteen Order | Allow students to view food items, place an order, get an order token, and automatically reduce item stock. |
| **FR-05** | Medium | College Store | Keep count of textbooks, uniform items, and stationery; let students reserve available items online. |
| **FR-06** | High | Health Room | Log student medical visits, record symptoms and first-aid given, and send emergency alerts if needed. |
| **FR-07** | Medium | Lost & Found | Let users post pictures and descriptions of found items; allow students to submit verification claims. |
| **FR-08** | High | Library Search | Search books by title or author, track borrowed books, calculate overdue fines, and book reading room desks. |
| **FR-09** | Medium | Parking Slots | Show counts of available 2-wheeler, 4-wheeler, and EV charging parking spots across campus blocks. |
| **FR-10** | Medium | Events Calendar | Display upcoming fests and guest lectures, register students, and generate digital entry passes. |
| **FR-11** | Medium | Clubs Module | Show club details under Sciences, Commerce, Arts, and Business; handle student member signups. |
| **FR-12** | High | Grievance Ticket | Allow students to lodge maintenance or Wi-Fi complaints and see status move from Pending to Resolved. |
| **FR-13** | Medium | Study Material | Provide downloadable PDF syllabus copies, past exam question papers (PYQs), and practical lab manuals. |
| **FR-14** | High | Campus Map | Display an interactive directory where clicking a block and floor reveals all classrooms, labs, and halls. |
| **FR-15** | Medium | Admin Reports | Generate summary reports for daily canteen sales, active maintenance complaints, and library book returns. |
| **FR-16** | High | Notifications | Send alert notifications when food is ready for pickup, a complaint is updated, or a borrowed book is due. |

---

# Section 8: Non-Functional Requirements

| Req ID | Quality Factor | How Our Database & Application Handles It |
| :---: | :--- | :--- |
| **NFR-01** | Response Time | Search queries for teacher schedule lookup, canteen menus, and library books must respond in under 500 milliseconds. We use B-Tree indexes on `faculty_id` and `day_of_week`. |
| **NFR-02** | Security | Student and faculty passwords are encrypted using Bcrypt. SQL injection is prevented by using parameterized queries and stored procedures. |
| **NFR-03** | Data Consistency | All orders and book borrowing transactions follow strict ACID rules. We use database row locks (`SELECT FOR UPDATE`) to stop double-booking. |
| **NFR-04** | Ease of Use | Interface works smoothly on mobile phones and laptops. Any core task can be completed in three clicks or taps. |
| **NFR-05** | Availability | The database is available throughout campus hours (7:30 AM to 7:30 PM) with regular daily database backup copies. |
| **NFR-06** | Clean Schema | All database tables are normalized up to BCNF to ensure there is no repetitive data or accidental deletion of records. |

---

# Section 9: Software Development Model & Guide Discussion

* **Development Model Chosen:** **Agile / Iterative Model**
* **Why this model fits:** Because we are building 12 modules, doing everything in one giant step is risky. The Agile iterative approach lets our team build, test, and normalize the database tables in two-week cycles (Sprints):
  * **Sprint 1 (Weeks 1-2):** User accounts, role access, campus blocks, rooms, and teacher schedule timetable engine.
  * **Sprint 2 (Weeks 3-4):** Canteen menu, pre-ordering, bookstore inventory, and medical room visit logs.
  * **Sprint 3 (Weeks 5-6):** Library OPAC, parking slot counters, lost & found, and student clubs/events.
  * **Sprint 4 (Weeks 7-8):** Grievance redressal ticketing, academic resources, and campus floor map directory.
  * **Sprint 5 (Weeks 9-10):** Stored procedures, triggers, views, load testing, and final project documentation.

### Guide Discussion Notes (Meeting with Dr Hemanth K S)
| No. | Guide Advice & Suggestion | How We Are Implementing It in Our Project |
| :---: | :--- | :--- |
| **1** | Feasibility of Teacher Tracking | Dr Hemanth K S advised that continuous live hardware/biometric tracking across campus is difficult to implement. He instructed us to fetch the teacher's schedule from the database: if they have a class, show the classroom/lab; if free, show their designated staff room. |
| **2** | Normalize all tables up to BCNF | Split user and faculty records properly; use junction tables for student club memberships and fest signups. |
| **3** | Prevent food stock overselling | Use database transaction row locks in stored procedure `sp_PlaceCafeteriaOrder` so stock never goes below zero. |
| **4** | Lock grievance status transitions | Use a database trigger to enforce that complaints move in order: Pending -> In-Progress -> Resolved. |

---

# Section 10: Student Declaration & Guide Verification

*We confirm that the information provided in this document is based on our project discussion and preliminary analysis. We have explained the proposed project to our guide and discussed the scope and requirements.*

### Team Members Confirmation:
* **Member 1:** Mayank Raj Gupta (Register No: 2543115) — Signature: _______________________
* **Member 2:** Sonti Sri Lakshmi Aslesha (Register No: 2543140) — Signature: _______________________
* **Member 3:** Aadiya Naresh (Register No: 2543163) — Signature: _______________________
* **Date of Submission:** ___________________________

### Project Guide Verification & Remarks:
* **Project Guide Name:** **Dr Hemanth K S**
* **Department:** Department of Computer Science, CHRIST (Deemed to be University)
* **Guide's Signature:** ___________________________ &nbsp;&nbsp;&nbsp;&nbsp; **Date:** ___________________________
* **Guide's Decision:** `[ ] Approved as submitted` &nbsp;&nbsp;&nbsp;&nbsp; `[ ] Approved with minor modifications` &nbsp;&nbsp;&nbsp;&nbsp; `[ ] Needs revision`

### Guide's Detailed Feedback & Suggestions:
____________________________________________________________________________________________________  
____________________________________________________________________________________________________  
____________________________________________________________________________________________________  
____________________________________________________________________________________________________  
____________________________________________________________________________________________________  

### Suggested Assessment Rubric (For Faculty Use — Max 10 Marks)
| Assessment Criterion | Max Marks | Marks Awarded |
| :--- | :---: | :---: |
| Problem statement, business objectives and comprehensive project scope | 2.0 | |
| Existing-system analysis, preliminary investigation and identification of need | 2.0 | |
| Feasibility study (Technical, Operational, Economic, Behavioural) | 2.0 | |
| Functional and Non-functional requirements / SRS completeness & clarity | 2.0 | |
| Guide discussion, technical explanation, completeness and signed verification | 2.0 | |
| **TOTAL ASSESSMENT-1 MARKS** | **10.0** | |

---

# Section 11: Relational Database Architecture Blueprint (Appendix)

| Table Name | Primary Key | Foreign Keys | Key Fields & Constraints |
| :--- | :--- | :--- | :--- |
| **Users** | `user_id` (PK) | `role_id` -> Roles | `register_number` (UQ), `full_name`, `email` (UQ), `password_hash`, `is_active` |
| **Faculties** | `faculty_id` (PK) | `user_id`, `dept_id`, `staff_room_id` | `designation`, `office_extension`, `consultation_hours`, `default_cabin` |
| **Faculty_Timetables** | `schedule_id` (PK) | `faculty_id`, `room_id` | `day_of_week`, `period_no`, `start_time`, `end_time`, `subject_code`, `section` |
| **Faculty_Status_Overrides** | `override_id` (PK) | `faculty_id` | `override_date`, `start_time`, `end_time`, `status` (MEETING, ON_LEAVE), `notes` |
| **Campus_Blocks** | `block_id` (PK) | None | `block_code` (UQ), `block_name`, `total_floors`, `latitude`, `longitude` |
| **Campus_Rooms** | `room_id` (PK) | `block_id` -> Campus_Blocks | `room_number`, `floor_number`, `room_type`, `seating_capacity` (UQ block, room) |
| **Cafeteria_Items** | `item_id` (PK) | `vendor_id` -> Vendors | `item_name`, `category`, `price`, `is_available`, `current_stock_qty` |
| **Cafeteria_Orders** | `order_id` (PK) | `user_id`, `vendor_id` | `order_timestamp`, `token_number`, `total_amount`, `order_status` |
| **Store_Inventory** | `product_id` (PK) | `category_id` -> Store_Categories | `product_code` (UQ), `product_name`, `unit_price`, `stock_quantity` |
| **Medical_Visits** | `visit_id` (PK) | `student_id`, `attending_staff_id` | `checkin_time`, `symptoms_observed`, `is_emergency_flag`, `disposition` |
| **Lost_Found_Items** | `item_id` (PK) | `reported_by_user_id`, `room_id` | `item_title`, `category`, `photo_url`, `date_found`, `status` |
| **Library_Books** | `book_id` (PK) | `category_id` -> Book_Categories | `isbn` (UQ), `title`, `author`, `edition`, `total_copies`, `available_copies` |
| **Library_Circulation** | `issue_id` (PK) | `book_id`, `user_id` | `issued_date`, `due_date`, `returned_date`, `fine_amount`, `circulation_status` |
| **Parking_Slots** | `slot_id` (PK) | `block_id` -> Campus_Blocks | `slot_code` (UQ), `vehicle_type`, `is_ev_charging`, `is_occupied` |
| **Campus_Events** | `event_id` (PK) | `club_id`, `venue_room_id` | `event_title`, `event_type`, `start_time`, `end_time`, `max_registrations` |
| **Student_Clubs** | `club_id` (PK) | `school_id`, `faculty_coordinator_id` | `club_name` (UQ), `club_tagline`, `founded_year` |
| **Grievances** | `ticket_id` (PK) | `student_id`, `room_id`, `assigned_to` | `category`, `ticket_subject`, `description`, `priority`, `status` |
| **Academic_Resources** | `resource_id` (PK) | `dept_id`, `uploaded_by_faculty` | `resource_type`, `course_code`, `document_title`, `file_url` |
