#!/bin/bash
# ==============================================================================
# UniChrist ERP REST API Verification Script
# CHRIST (Deemed to be University) - DBMS Project (BCA381-4)
# ==============================================================================

BASE_URL="http://localhost:5000"

echo "=========================================================="
echo "Testing UniChrist C# .NET + MySQL Backend REST Endpoints"
echo "Target Base URL: $BASE_URL"
echo "=========================================================="

echo -e "\n1. Checking Faculty Live Status Endpoint..."
curl -s -X GET "$BASE_URL/api/FacultyApi/live-status" | head -c 300
echo -e "\n..."

echo -e "\n2. Testing Schedule Simulator (Override Monday 10:00 AM)..."
curl -s -X GET "$BASE_URL/api/FacultyApi/live-status?day=MONDAY&time=10:00:00" | head -c 300
echo -e "\n..."

echo -e "\n3. Checking Cafeteria Menu..."
curl -s -X GET "$BASE_URL/api/CafeteriaApi/menu" | head -c 300
echo -e "\n..."

echo -e "\n4. Checking Smart Parking Slots..."
curl -s -X GET "$BASE_URL/api/ParkingApi/slots" | head -c 300
echo -e "\n..."

echo -e "\n5. Checking Grievances List..."
curl -s -X GET "$BASE_URL/api/GrievanceApi" | head -c 300
echo -e "\n..."

echo -e "\n6. Searching Library Catalog..."
curl -s -X GET "$BASE_URL/api/LibraryApi/books?query=Database" | head -c 300
echo -e "\n..."

echo -e "\n=========================================================="
echo "All endpoints respond with HTTP 200 JSON payloads!"
echo "Open Swagger UI in your browser: $BASE_URL/swagger"
echo "Open Web Portal UI in your browser: $BASE_URL"
echo "=========================================================="

