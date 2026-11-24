import os
import re

# Read base portal
with open('unichrist-web/build_portal.py', 'r') as f:
    portal_code = f.read()

# 1. Enhance Top Utility Bar with Language Toggle & Accessibility Controls
old_topbar = '''    <!-- 1. Topmost Official University Bar -->
    <div class="university-topbar">
        <div class="topbar-content">
            <div class="accreditation-pill">
                <span class="naac-badge">NAAC A+ GRADE</span>
                <span>UGC Recognised • Autonomy Since 2004 • NIRF Top Tier Multi-Campus University</span>
            </div>
            
            <!-- Live Role Switcher (Student vs HOD Dr. Vinay M) -->
            <div style="display:flex; align-items:center; gap:12px;">
                <div class="role-switcher-box">
                    <span style="font-size:10px; color:#CBD5E1; padding-left:6px; font-weight:700;">ROLE:</span>
                    <button class="role-pill active" id="role-btn-student" onclick="setPortalRole('student')">
                        <i class="fa-solid fa-user-graduate"></i> Student (Mayank)
                    </button>
                    <button class="role-pill" id="role-btn-hod" onclick="setPortalRole('hod')">
                        <i class="fa-solid fa-user-tie"></i> HOD (Dr. Vinay M)
                    </button>
                </div>

                <div class="campus-switcher">
                    <span class="campus-item active" onclick="switchCampus('BYC (Yeshwanthpur)')">BYC Campus</span>
                    <span class="campus-item" onclick="switchCampus('Bangalore Central')">Central</span>
                    <span class="campus-item" onclick="switchCampus('Kengeri')">Kengeri</span>
                </div>
            </div>
        </div>
    </div>'''

new_topbar = '''    <!-- 1. Topmost Official University Bar (With Accessibility, Quick Links & Role Switcher) -->
    <div class="university-topbar">
        <div class="topbar-content">
            <div class="accreditation-pill">
                <span class="naac-badge">NAAC A+ GRADE</span>
                <span>CHRIST (Deemed to be University) | UGC Recognised | Estd. 1969</span>
            </div>
            
            <!-- Quick Utility Links, Accessibility & Role Switcher -->
            <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
                <!-- Accessibility Controls (Font size & Contrast) -->
                <div class="accessibility-ctrls" style="display:flex; align-items:center; gap:4px; font-size:10px; background:rgba(255,255,255,0.08); padding:2px 6px; border-radius:3px;">
                    <span style="color:#94A3B8; font-weight:600;">Text:</span>
                    <button class="access-btn" onclick="adjustFontSize(-1)" title="Decrease Font">A-</button>
                    <button class="access-btn" onclick="adjustFontSize(0)" title="Default Font">A</button>
                    <button class="access-btn" onclick="adjustFontSize(1)" title="Increase Font">A+</button>
                    <button class="access-btn" onclick="toggleContrast()" title="Toggle High Contrast"><i class="fa-solid fa-circle-half-stroke"></i></button>
                </div>

                <!-- Language Toggle -->
                <button class="lang-pill" id="lang-toggle-btn" onclick="toggleLanguage()" style="background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.2); color:#CBD5E1; font-size:10.5px; padding:2px 7px; border-radius:3px; cursor:pointer;">
                    <i class="fa-solid fa-language"></i> <span id="lang-label">हिंदी</span>
                </button>

                <!-- Role Switcher -->
                <div class="role-switcher-box">
                    <span style="font-size:10px; color:#CBD5E1; padding-left:4px; font-weight:700;">ROLE:</span>
                    <button class="role-pill active" id="role-btn-student" onclick="setPortalRole('student')">
                        <i class="fa-solid fa-user-graduate"></i> Student (Mayank)
                    </button>
                    <button class="role-pill" id="role-btn-hod" onclick="setPortalRole('hod')">
                        <i class="fa-solid fa-user-tie"></i> HOD (Dr. Vinay M)
                    </button>
                    <button class="role-pill" id="role-btn-admin" onclick="setPortalRole('admin')">
                        <i class="fa-solid fa-shield-halved"></i> Admin
                    </button>
                </div>

                <div class="campus-switcher">
                    <span class="campus-item active" onclick="switchCampus('BYC (Yeshwanthpur)')">BYC</span>
                    <span class="campus-item" onclick="switchCampus('Bangalore Central')">Central</span>
                    <span class="campus-item" onclick="switchCampus('Kengeri')">Kengeri</span>
                    <span class="campus-item" onclick="navigateTo('page-login')"><i class="fa-solid fa-arrow-right-to-bracket"></i> Login</span>
                </div>
            </div>
        </div>
    </div>'''

portal_code = portal_code.replace(old_topbar, new_topbar)

# 2. Main Navigation Bar with Institutional Mega-Menu Dropdowns
old_header_actions = '''            <div class="quick-nav-actions">
                <button class="btn-header-action idcard-btn" onclick="navigateTo('page-idcard')">
                    <i class="fa-solid fa-id-card"></i> Digital ID
                </button>
                <button class="btn-header-action emergency-btn" onclick="navigateTo('page-security')">
                    <i class="fa-solid fa-phone-volume"></i> Emergency
                </button>
                <button class="btn-header-action portal-login-btn" onclick="navigateTo('page-login')">
                    <i class="fa-solid fa-user-shield"></i> KP ERP Login
                </button>
            </div>'''

new_header_actions = '''            <div class="header-nav-menus" style="display:flex; align-items:center; gap:12px;">
                <!-- Main Header Nav Links / Dropdowns -->
                <div class="nav-dropdown-item">
                    <span class="nav-link" onclick="navigateTo('page-about')">About ▾</span>
                    <div class="nav-dropdown-menu">
                        <a href="#" onclick="navigateTo('page-about'); return false;"><i class="fa-solid fa-landmark"></i> History (1969)</a>
                        <a href="#" onclick="navigateTo('page-about'); return false;"><i class="fa-solid fa-eye"></i> Vision &amp; Mission</a>
                        <a href="#" onclick="navigateTo('page-leadership'); return false;"><i class="fa-solid fa-user-tie"></i> University Leadership</a>
                        <a href="#" onclick="navigateTo('page-about'); return false;"><i class="fa-solid fa-certificate"></i> Accreditation &amp; NIRF</a>
                        <a href="#" onclick="navigateTo('page-map'); return false;"><i class="fa-solid fa-compass"></i> Campus Tour (BYC)</a>
                    </div>
                </div>

                <div class="nav-dropdown-item">
                    <span class="nav-link" onclick="navigateTo('page-admissions')">Admissions ▾</span>
                    <div class="nav-dropdown-menu">
                        <a href="#" onclick="navigateTo('page-admissions'); return false;"><i class="fa-solid fa-graduation-cap"></i> Undergraduate (UG)</a>
                        <a href="#" onclick="navigateTo('page-admissions'); return false;"><i class="fa-solid fa-user-graduate"></i> Postgraduate (PG)</a>
                        <a href="#" onclick="navigateTo('page-research'); return false;"><i class="fa-solid fa-microscope"></i> Doctoral (PhD)</a>
                        <a href="#" onclick="navigateTo('page-feedues'); return false;"><i class="fa-solid fa-receipt"></i> Fee Structure 2026</a>
                        <a href="#" onclick="navigateTo('page-admissionsdesk'); return false;"><i class="fa-solid fa-file-signature"></i> Apply Online</a>
                    </div>
                </div>

                <div class="nav-dropdown-item">
                    <span class="nav-link" onclick="navigateTo('page-academics')">Academics ▾</span>
                    <div class="nav-dropdown-menu">
                        <a href="#" onclick="navigateTo('page-schools'); return false;"><i class="fa-solid fa-university"></i> 8 Academic Schools</a>
                        <a href="#" onclick="navigateTo('page-faculty'); return false;"><i class="fa-solid fa-users"></i> Faculty Directory &amp; Radar</a>
                        <a href="#" onclick="navigateTo('page-examinations'); return false;"><i class="fa-solid fa-clipboard-check"></i> Controller of Exams (COE)</a>
                        <a href="#" onclick="navigateTo('page-library'); return false;"><i class="fa-solid fa-book-bookmark"></i> Central Library OPAC</a>
                        <a href="#" onclick="navigateTo('page-research'); return false;"><i class="fa-solid fa-atom"></i> Research &amp; Innovation</a>
                    </div>
                </div>

                <div class="nav-dropdown-item">
                    <span class="nav-link" onclick="navigateTo('page-campuslife')">Campus Life ▾</span>
                    <div class="nav-dropdown-menu">
                        <a href="#" onclick="navigateTo('page-hostel'); return false;"><i class="fa-solid fa-bed"></i> Hostels &amp; Residences</a>
                        <a href="#" onclick="navigateTo('page-cafeteria'); return false;"><i class="fa-solid fa-utensils"></i> Cafeterias &amp; Menus</a>
                        <a href="#" onclick="navigateTo('page-sportsturf'); return false;"><i class="fa-solid fa-futbol"></i> Sports Turf &amp; Courts</a>
                        <a href="#" onclick="navigateTo('page-clubs'); return false;"><i class="fa-solid fa-users-viewfinder"></i> Student Clubs (ACM, Natya)</a>
                        <a href="#" onclick="navigateTo('page-events'); return false;"><i class="fa-solid fa-calendar-days"></i> Upcoming 15-Day Events</a>
                    </div>
                </div>

                <div class="nav-dropdown-item">
                    <span class="nav-link" onclick="navigateTo('page-placements')">Placements ▾</span>
                    <div class="nav-dropdown-menu">
                        <a href="#" onclick="navigateTo('page-placements'); return false;"><i class="fa-solid fa-chart-line"></i> Placement Stats 2026</a>
                        <a href="#" onclick="navigateTo('page-placements'); return false;"><i class="fa-solid fa-briefcase"></i> Top Recruiters (500+)</a>
                        <a href="#" onclick="navigateTo('page-placements'); return false;"><i class="fa-solid fa-building"></i> Placement Cell Desk</a>
                    </div>
                </div>

                <div class="nav-dropdown-item">
                    <span class="nav-link" onclick="navigateTo('page-news')">News</span>
                </div>

                <div class="nav-dropdown-item">
                    <span class="nav-link" onclick="navigateTo('page-contact')">Contact</span>
                </div>

                <button class="btn-header-action btn-gold" style="padding:6px 14px; font-weight:800; border-radius:3px;" onclick="navigateTo('page-admissionsdesk')">
                    Apply Now
                </button>

                <button class="btn-header-action idcard-btn" onclick="navigateTo('page-idcard')" title="Digital Student ID">
                    <i class="fa-solid fa-id-card"></i> ID
                </button>
            </div>'''

portal_code = portal_code.replace(old_header_actions, new_header_actions)

with open('unichrist-web/build_portal.py', 'w') as f:
    f.write(portal_code)

print("Updated topbar and header mega-menus successfully!")
