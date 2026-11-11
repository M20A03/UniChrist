# UniChrist Backend Server (C# • ASP.NET Core • MySQL)

### Course: BCA381-4 (DBMS Project) — CHRIST (Deemed to be University)
**Project Title:** UniChrist — Integrated Smart Campus ERP & Location-Aware Services  
**Guide:** Dr Hemanth K S  
**Team Members:** Mayank Raj Gupta (Lead - 2543115), Sonti Sri Lakshmi Aslesha (2543140), Aadiya Naresh (2543163)

---

## 🛠️ Technology Stack
* **Language:** C# 12 / .NET 8.0
* **Framework:** ASP.NET Core (MVC + Web API)
* **ORM:** Entity Framework Core 8.0 with `Pomelo.EntityFrameworkCore.MySql`
* **Database:** MySQL 8.0+ / MariaDB
* **API Documentation:** OpenAPI / Swagger UI
* **Frontend:** Responsive HTML5 / CSS3 / JavaScript (with Christ University Blue & Gold theme)

---

## 🚀 Quick Start Guide

### Step 1: Setup MySQL Database
1. Open **MySQL Workbench**, **phpMyAdmin**, or **MySQL Terminal**.
2. Run the script located at:
   ```bash
   UniChristBackend/Database/UniChrist_MySQL_Schema.sql
   ```
   Or run directly from the command line:
   ```bash
   mysql -u root -p < UniChristBackend/Database/UniChrist_MySQL_Schema.sql
   ```
   This creates the database `unichrist_db` and seeds all initial data (users, faculty schedules, rooms, cafeteria items, parking slots).

### Step 2: Configure Connection String
Open `appsettings.json` and adjust your MySQL credentials:
```json
"ConnectionStrings": {
  "DefaultConnection": "Server=localhost;Port=3306;Database=unichrist_db;User=root;Password=your_password;CharSet=utf8mb4;"
}
```

### Step 3: Run the Backend Server
From the `UniChristBackend` directory, execute:
```bash
dotnet restore
dotnet run
```
Or open the solution in **Visual Studio 2022 / Rider / VS Code** and press **F5 (Start Debugging)**.

---

## 🌐 URLs & Endpoints
* **Web Portal Interface:** [http://localhost:5000](http://localhost:5000)
* **Interactive Swagger REST API:** [http://localhost:5000/swagger](http://localhost:5000/swagger)

---

## 📡 Key REST API Endpoints

| Category | Endpoint | Method | Description |
| :--- | :--- | :---: | :--- |
| **Faculty Locator** | `/api/FacultyApi/live-status` | `GET` | Live schedule-based teacher location (checks current period vs. timetable) |
| **Faculty Override** | `/api/FacultyApi/simulate-override` | `POST` | Simulate meeting, leave, or consultation room override |
| **Cafeteria Menu** | `/api/CafeteriaApi/menu` | `GET` | Active food stalls and menu items with live stock counts |
| **Order Placement** | `/api/CafeteriaApi/order` | `POST` | Pre-orders food items and generates order token number |
| **Grievance Portal**| `/api/GrievanceApi` | `GET/POST`| Fetch tickets or lodge a new campus infrastructure complaint |
| **Smart Parking**   | `/api/ParkingApi/slots` | `GET` | Real-time vacancy status of Block A & B slots |
| **Parking Toggle**  | `/api/ParkingApi/toggle` | `POST` | Toggle parking occupancy status (simulating sensor) |
| **Library OPAC**    | `/api/LibraryApi/books` | `GET` | Centralized book search by title, author, or ISBN |
| **Authentication**  | `/api/AuthApi/login` | `POST` | Login with student/faculty register number |

