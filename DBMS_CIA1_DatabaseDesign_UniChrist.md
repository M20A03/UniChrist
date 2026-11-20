# CHRIST (Deemed to be University)
### Department of Computer Science — Bangalore Yeshwanthpur Campus
### Course: BCA381-4 (DBMS Project) | Class: 4BCA-B | Academic Year: 2025–2029 (Semester IV)
## CIA-1 SUBMISSION: DATABASE DESIGN (ERD, NORMALIZATION, SCHEMA & DATA POPULATION)

---

### Assignment Metadata & Team Details
* **Course Code & Title:** BCA381-4 — Database Management Systems Project
* **Assignment Title:** DBMS Project – CIA 1: Database Design (Component 2: 10 Marks)
* **Project Title:** **UniChrist: Integrated Campus Life & Location Services Portal**
* **Project Guide:** **Dr Hemanth K S** (Associate Professor, Department of Computer Science)
* **Due Date / Submission Date:** 20 November 2026
* **Evaluation Weightage:** 10 Marks (ERD: 2M, Normalization: 3M, Relational Schema: 2M, Database Creation & Population: 3M)

| S.No | Student Name | Register Number | Role in Project | Email ID |
| :---: | :--- | :---: | :--- | :--- |
| **1** | **Mayank Raj Gupta** | **2543115** | **Team Lead**: Full database design, table schema, SQL scripts and backend logic | `mayank.raj@christuniversity.in` |
| **2** | **Sonti Sri Lakshmi Aslesha** | **2543140** | **Schema Normalization**: 1NF to BCNF, constraints, views and queries | `aslesha.sonti@christuniversity.in` |
| **3** | **Aadiya Naresh** | **2543163** | **System Analyst**: ER modeling, sample data population & benchmark proofs | `aadiya.naresh@christuniversity.in` |

---

# Section 1: Team Details & Evaluation Rubrics
* **Evaluation Component 1: Entity Relationship Diagram (ERD)** — 2 Marks (Entities, attributes, keys, relationships & cardinality)
* **Evaluation Component 2: Database Normalization** — 3 Marks (UNF to BCNF with functional dependencies)
* **Evaluation Component 3: Relational Database Schema** — 2 Marks (Tables, keys, data types and constraints)
* **Evaluation Component 4: Database Creation and Data Population** — 3 Marks (SQL implementation and sample records)
* **Total:** 10 Marks

---

# Section 2: Executive Summary & Project Domain Rationale
In strict alignment with the Project Synopsis and Software Requirements Specification (SRS) approved by project guide **Dr Hemanth K S**, the **UniChrist** system models an integrated academic and facilities management platform. Instead of deploying expensive physical hardware trackers across campus buildings, the system implements an intelligent **Automated Faculty Schedule & Location Engine**. By checking university faculty weekly timetables against current clock periods, the database dynamically resolves active room locations (e.g., *DBMS Lab 201* during lectures) or designated cabins (e.g., *Staff Room 101* during consultation hours).

The schema incorporates all **12 operational campus modules** across **34 relational tables**:
1. Core Demographics & Authentication (RBAC)
2. Smart Cafeteria Pre-Ordering
3. University Bookstore & Uniforms
4. Health & Medical Room
5. Campus Lost & Found Vault
6. Centralized Library OPAC
7. Smart Parking & EV Telemetry
8. Campus Events & Digital Passes
9. Student Clubs & Societies
10. Teacher Schedule & Location Engine
11. Grievance Redressal Portal
12. Academic Study Resources Repository
13. Spatial Campus Directory

---

# Section 3: Entity Relationship Diagram (ERD) — [2 Marks]
* **Entities:** 34 relational entities defined across the 12 modules.
* **Attributes:** Formally classified into Key, Simple/Atomic, Composite, Multi-Valued, and Derived attributes.
* **Cardinality & Participation:** 1:1, 1:N, M:N relationships with total participation on dependent child entities.
* **ER Diagram:** Rendered and embedded as a high-resolution diagram in `images/erd_diagram.png` and `images/erd_diagram.svg`.

---

# Section 4: Database Normalization (UNF to BCNF) — [3 Marks]
* **Relational Anomalies:** Detailed explanations for Insertion, Deletion, and Update anomalies.
* **Functional Dependencies:** Catalog of 20 formal functional dependencies spanning all 12 modules.
* **Normalization Demonstration:**
  * **UNF to 1NF:** Eliminating repeating groups; ensuring atomic attributes.
  * **1NF to 2NF:** Eliminating partial dependencies on composite candidate keys.
  * **2NF to 3NF:** Eliminating transitive dependencies (`room_id -> block_id -> block_name`).
  * **3NF to BCNF:** Ensuring every determinant is a superkey (rigorous proof of Timetable Candidate Keys).
* **Final Normalized Relations:** 34 relations in BCNF notation.

---

# Section 5: Relational Database Schema & Data Dictionary — [2 Marks]
* **Mapping Rules:** Formal transformation from conceptual ERD to concrete relations.
* **Data Dictionary:** Detailed specifications for all 34 tables (column names, data types, nullability, constraints, PK/FK relationships).
* **Integrity Constraints:** Entity, referential (`CASCADE`, `RESTRICT`, `SET NULL`), domain `CHECK`, and unique constraints.

---

# Section 6: Database Creation & Data Population — [3 Marks]
* **SQL Implementation:** Complete SQL schema and sample data scripts in `UniChrist_Database_Schema_and_Data.sql`.
* **Execution Proofs:** Live terminal outputs demonstrating table creation, constraints validation, foreign key cascades, and complex operational queries across the 12 modules.

---

# Section 7: Student Declaration & Guide Endorsement
* **Student Team:** Mayank Raj Gupta (2543115), Sonti Sri Lakshmi Aslesha (2543140), Aadiya Naresh (2543163)
* **Faculty Guide:** Dr Hemanth K S (Associate Professor, Department of Computer Science)
