with open('unichrist-web/build_portal.py', 'r') as f:
    text = f.read()

# Pages to append before </main>
missing_pages_html = """
            <!-- ================= PUBLIC PAGE 5: CAMPUS LIFE OVERVIEW ================= -->
            <section id="page-campuslife" class="page-view">
                <div class="university-hero-billboard">
                    <div class="billboard-tag">CAMPUS EXPERIENCE &amp; CULTURE</div>
                    <h2 class="billboard-title">Vibrant Student Life at Christ University</h2>
                    <p class="billboard-desc">From world-class residential halls and multi-cuisine cafeterias to Olympic-tier sports turfs, 30+ active student societies, and national cultural fests.</p>
                </div>

                <div class="cards-grid-3">
                    <div class="item-tile" onclick="navigateTo('page-hostel')">
                        <div class="feature-heading"><i class="fa-solid fa-bed" style="color:var(--christ-gold-dark);"></i> Hostels &amp; Residences</div>
                        <div class="feature-desc">Jonas Hall (Women) and St. Kuriakose Elias Hall (Men) with biometric security, Wi-Fi, and mess.</div>
                        <div class="tile-footer"><span>Explore Stays</span> <i class="fa-solid fa-chevron-right"></i></div>
                    </div>
                    <div class="item-tile" onclick="navigateTo('page-cafeteria')">
                        <div class="feature-heading"><i class="fa-solid fa-utensils" style="color:var(--christ-gold-dark);"></i> Cafeterias &amp; Food Courts</div>
                        <div class="feature-desc">Central Gourmet Hall &amp; Ivy Hall Express featuring live crowd sensor &amp; pre-order integration.</div>
                        <div class="tile-footer"><span>View Menus</span> <i class="fa-solid fa-chevron-right"></i></div>
                    </div>
                    <div class="item-tile" onclick="navigateTo('page-sportsturf')">
                        <div class="feature-heading"><i class="fa-solid fa-futbol" style="color:var(--christ-gold-dark);"></i> Sports Turf &amp; Courts</div>
                        <div class="feature-desc">FIFA-standard floodlit football turf, 4 BWF wooden badminton courts, and acrylic basketball arena.</div>
                        <div class="tile-footer"><span>Book Slot</span> <i class="fa-solid fa-chevron-right"></i></div>
                    </div>
                    <div class="item-tile" onclick="navigateTo('page-clubs')">
                        <div class="feature-heading"><i class="fa-solid fa-users" style="color:var(--christ-gold-dark);"></i> 30+ Clubs &amp; Societies</div>
                        <div class="feature-desc">ACM Student Chapter, Natya Cultural Team, Toastmasters, Literary Society, and Rotaract.</div>
                        <div class="tile-footer"><span>Join Clubs</span> <i class="fa-solid fa-chevron-right"></i></div>
                    </div>
                    <div class="item-tile" onclick="navigateTo('page-events')">
                        <div class="feature-heading"><i class="fa-solid fa-calendar-days" style="color:var(--christ-gold-dark);"></i> Upcoming 15-Day Events</div>
                        <div class="feature-desc">Daksh National Fest, AI Hackathons, FinTech workshops, and campus acoustic sunset jams.</div>
                        <div class="tile-footer"><span>View Calendar</span> <i class="fa-solid fa-chevron-right"></i></div>
                    </div>
                    <div class="item-tile" onclick="navigateTo('page-medicalcchs')">
                        <div class="feature-heading"><i class="fa-solid fa-hospital" style="color:var(--christ-gold-dark);"></i> Health &amp; CCHS Wellness</div>
                        <div class="feature-desc">24/7 on-campus physician, Sparsh Hospital emergency ambulance tie-up, and confidential counselling.</div>
                        <div class="tile-footer"><span>Book Care</span> <i class="fa-solid fa-chevron-right"></i></div>
                    </div>
                </div>
            </section>

            <!-- ================= PUBLIC PAGE 7: NEWS & MEDIA ================= -->
            <section id="page-news" class="page-view">
                <div class="uni-card">
                    <div class="card-header-bar">
                        <h2 class="card-main-title"><i class="fa-solid fa-newspaper"></i> Christ University News &amp; Media Publications</h2>
                        <span class="status-chip chip-blue">Official Press Releases</span>
                    </div>

                    <div style="display:flex; gap:8px; margin-bottom:16px; overflow-x:auto; padding-bottom:4px;">
                        <button class="status-chip chip-blue" style="cursor:pointer; padding:5px 12px;">All News</button>
                        <button class="status-chip chip-amber" style="cursor:pointer; padding:5px 12px;">Academic &amp; Research</button>
                        <button class="status-chip chip-green" style="cursor:pointer; padding:5px 12px;">Fests &amp; Events</button>
                        <button class="status-chip chip-purple" style="cursor:pointer; padding:5px 12px;">Placements &amp; Careers</button>
                        <button class="status-chip chip-red" style="cursor:pointer; padding:5px 12px;">Press Releases</button>
                    </div>

                    <div class="cards-grid-3">
                        <div class="item-tile">
                            <span class="status-chip chip-blue">24 NOV 2026 • RESEARCH</span>
                            <div class="tile-name">Christ University Department of Computer Science Secures ₹50L DST Grant for AI Edge Computing</div>
                            <div class="tile-sub">Led by Dr. Vinay M, the autonomous sensor research lab at Bangalore Yeshwanthpur Campus initiates research with Sparsh Hospital.</div>
                            <div class="tile-footer"><span>By University News Desk</span> <button class="btn-christ" style="padding:3px 8px; font-size:10.5px;" onclick="showToast('Loading full press release...')">Read Article</button></div>
                        </div>

                        <div class="item-tile">
                            <span class="status-chip chip-green">22 NOV 2026 • PLACEMENTS</span>
                            <div class="tile-name">Over 78% BCA &amp; MCA Scholars Secure Day-1 Pre-Placement Offers from Tier-1 Tech Giants</div>
                            <div class="tile-sub">Amazon, Deloitte, KPMG, and Cisco lead the campus hiring drive with highest international CTC reaching ₹24.5 LPA.</div>
                            <div class="tile-footer"><span>Placement Cell</span> <button class="btn-christ" style="padding:3px 8px; font-size:10.5px;" onclick="navigateTo('page-placements')">View Report</button></div>
                        </div>

                        <div class="item-tile">
                            <span class="status-chip chip-purple">20 NOV 2026 • CAMPUS LIFE</span>
                            <div class="tile-name">Daksh 2026: Bangalore's Premier Inter-Collegiate Management &amp; Tech Conclave Commences at BYC</div>
                            <div class="tile-sub">Over 4,500 delegates from 60 universities across India arrive for three days of rigorous competition and startup pitching.</div>
                            <div class="tile-footer"><span>Student Council</span> <button class="btn-gold" style="padding:3px 8px; font-size:10.5px;" onclick="navigateTo('page-events')">Event Schedule</button></div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- ================= PUBLIC PAGE 8: CONTACT & CAMPUS VISIT ================= -->
            <section id="page-contact" class="page-view">
                <div class="uni-card">
                    <div class="card-header-bar">
                        <h2 class="card-main-title"><i class="fa-solid fa-address-book"></i> Contact Us &amp; Plan Your Campus Visit</h2>
                        <span class="status-chip chip-gold">Bangalore Yeshwanthpur Campus</span>
                    </div>

                    <div class="cards-grid-2" style="margin-bottom:20px;">
                        <div class="item-tile" style="border-left:4px solid var(--christ-navy);">
                            <div class="tile-name">Campus Address &amp; Main Exchange</div>
                            <div class="tile-sub" style="line-height:1.7;">
                                <strong>CHRIST (Deemed to be University)</strong><br>
                                Bangalore Yeshwanthpur Campus (BYC)<br>
                                Hesaraghatta Main Road, Nagasandra Post, Bengaluru - 560073<br>
                                <strong>EPABX:</strong> 080 4012 9100 / 9600<br>
                                <strong>Admissions Office:</strong> 080 4012 9622 / 9623<br>
                                <strong>Email:</strong> byc.office@christuniversity.in / admissions@christuniversity.in
                            </div>
                            <div class="tile-footer">
                                <span>Nearest Metro: Nagasandra (Green Line - 1.2 km)</span>
                                <button class="btn-christ" style="padding:4px 10px; font-size:11px;" onclick="navigateTo('page-metrobus')">Shuttle Route</button>
                            </div>
                        </div>

                        <div class="item-tile" style="border-left:4px solid var(--state-danger);">
                            <div class="tile-name" style="color:var(--state-danger);">24/7 Campus Emergency &amp; Security Desk</div>
                            <div class="tile-sub" style="line-height:1.7;">
                                <strong>Security Control Room (Gate 1):</strong> +91 80 4012 9666<br>
                                <strong>On-Campus Ambulance Hotline:</strong> 080 4012 9100 (Ext. 999)<br>
                                <strong>Anti-Ragging Squad (National Helpline):</strong> 1800-180-5522<br>
                                <strong>Women's Internal Complaints Committee (ICC):</strong> icc.byc@christuniversity.in<br>
                                <strong>CCHS Mental Wellness Confidential Desk:</strong> cchs.byc@christuniversity.in
                            </div>
                            <div class="tile-footer">
                                <span>Zero Tolerance Campus</span>
                                <button class="btn-christ" style="padding:4px 10px; font-size:11px;" onclick="navigateTo('page-grievance')">Lodge Grievance</button>
                            </div>
                        </div>
                    </div>

                    <!-- Campus Visit Booking Form -->
                    <div class="item-tile" style="background:#F8FAFC; border:1px solid var(--border-color); padding:16px;">
                        <h3 style="font-size:14px; font-weight:700; color:var(--christ-navy); margin-bottom:10px;"><i class="fa-solid fa-calendar-check"></i> Book an Official Campus Guided Tour</h3>
                        <div class="cards-grid-3">
                            <div class="form-row">
                                <label class="form-label">Full Name</label>
                                <input type="text" class="form-input" placeholder="Your Name" value="Mayank Raj Gupta" />
                            </div>
                            <div class="form-row">
                                <label class="form-label">Email Address</label>
                                <input type="email" class="form-input" placeholder="name@email.com" value="mayank.gupta@christuniversity.in" />
                            </div>
                            <div class="form-row">
                                <label class="form-label">Preferred Date &amp; Slot</label>
                                <input type="date" class="form-input" value="2026-11-28" />
                            </div>
                        </div>
                        <button class="btn-gold" style="margin-top:10px;" onclick="showToast('Campus Tour booked! Confirmation SMS & Pass dispatched.')">Schedule Guided Tour</button>
                    </div>
                </div>
            </section>

            <!-- ================= SETTINGS: MY PROFILE ================= -->
            <section id="page-profile" class="page-view">
                <div class="uni-card">
                    <div class="card-header-bar">
                        <h2 class="card-main-title"><i class="fa-solid fa-user-circle"></i> Student Academic Profile</h2>
                        <span class="status-chip chip-green">Active KP Account</span>
                    </div>

                    <div class="cards-grid-3" style="margin-bottom:20px;">
                        <div class="item-tile" style="text-align:center;">
                            <svg width="80" height="80" viewBox="0 0 100 100" style="border-radius:50%; background:#F1F5F9; border:3px solid var(--christ-gold); margin:0 auto 10px;">
                                <circle cx="50" cy="38" r="22" fill="#002147"/>
                                <path d="M18 90C18 70 32 58 50 58C68 58 82 70 82 90" fill="#002147"/>
                            </svg>
                            <div style="font-size:15px; font-weight:800; color:var(--christ-navy);">Mayank Raj Gupta</div>
                            <div style="font-size:12px; color:var(--text-muted);">Register No: 2543115</div>
                            <div style="font-size:11.5px; color:var(--christ-gold-dark); font-weight:700; margin-top:4px;">4BCA B • Semester 4</div>
                            <button class="btn-christ" style="margin-top:10px; width:100%; font-size:11px;" onclick="navigateTo('page-idcard')"><i class="fa-solid fa-id-card"></i> View Digital ID</button>
                        </div>

                        <div class="item-tile" style="grid-column:span 2;">
                            <div style="font-size:13px; font-weight:700; color:var(--christ-navy); margin-bottom:12px;">Enrolled Degree &amp; Departmental Information</div>
                            <table class="academic-table" style="font-size:12px;">
                                <tr><td style="font-weight:700; width:35%;">Academic Program:</td><td>Bachelor of Computer Applications (BCA Hons)</td></tr>
                                <tr><td style="font-weight:700;">Department:</td><td>Department of Computer Science (Block B)</td></tr>
                                <tr><td style="font-weight:700;">Head of Department (HOD):</td><td>Dr. Vinay M (Cabin 302, Block B)</td></tr>
                                <tr><td style="font-weight:700;">Academic Mentor:</td><td>Dr. S. K. Roy (Room 402, Block B)</td></tr>
                                <tr><td style="font-weight:700;">Current Aggregate Attendance:</td><td><strong style="color:var(--state-success);">87.5%</strong> (Exam Eligible)</td></tr>
                                <tr><td style="font-weight:700;">Cumulative CGPA:</td><td><strong style="color:var(--christ-navy);">8.64 / 10.00</strong> (First Class Distinction)</td></tr>
                            </table>
                        </div>
                    </div>
                </div>
            </section>

            <!-- ================= SETTINGS: NOTIFICATIONS ================= -->
            <section id="page-notifications" class="page-view">
                <div class="uni-card">
                    <div class="card-header-bar">
                        <h2 class="card-main-title"><i class="fa-solid fa-bell"></i> Notification Centre &amp; Alert Preferences</h2>
                        <button class="btn-christ" style="padding:4px 10px; font-size:11px;" onclick="showToast('All notifications marked as read')">Mark All Read</button>
                    </div>

                    <div style="display:flex; flex-direction:column; gap:10px;">
                        <div class="item-tile" style="border-left:4px solid var(--state-success);">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <span class="status-chip chip-green">ATTENDANCE UPDATE</span>
                                <span style="font-size:10.5px; color:var(--text-muted);">Today, 2:15 PM</span>
                            </div>
                            <div class="tile-name">Yellow Form Approved by HOD Dr. Vinay M</div>
                            <div class="tile-sub">Duty leave claim for National AI Hackathon (Ref: YF-91024) approved. 12 lecture hours credited to your ERP attendance.</div>
                        </div>

                        <div class="item-tile" style="border-left:4px solid var(--state-warning);">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <span class="status-chip chip-amber">CIA DEADLINE</span>
                                <span style="font-size:10.5px; color:var(--text-muted);">Tomorrow, 11:59 PM</span>
                            </div>
                            <div class="tile-name">CS-602 Advanced DBMS Submission Due</div>
                            <div class="tile-sub">Submit your CIA 3 Case Study &amp; ERD report to Moodle. 15% semester weightage.</div>
                        </div>

                        <div class="item-tile" style="border-left:4px solid var(--state-info);">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <span class="status-chip chip-blue">EXAMINATION DESK</span>
                                <span style="font-size:10.5px; color:var(--text-muted);">20 Nov 2026</span>
                            </div>
                            <div class="tile-name">End Semester Examination Hall Tickets Published</div>
                            <div class="tile-sub">COE office has verified attendance and fee clearance. Digital Hall Ticket ready to download.</div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- ================= SETTINGS: PRIVACY & SECURITY ================= -->
            <section id="page-privacy" class="page-view">
                <div class="uni-card">
                    <div class="card-header-bar">
                        <h2 class="card-main-title"><i class="fa-solid fa-lock"></i> Account Privacy, 2FA &amp; Security Log</h2>
                        <span class="status-chip chip-green">256-Bit SSL Encrypted</span>
                    </div>

                    <div class="cards-grid-2">
                        <div class="item-tile">
                            <div class="tile-name">Two-Factor Authentication (2FA)</div>
                            <div class="tile-sub">Protected via Christ University Microsoft Authenticator &amp; Registered Mobile Number (+91 ******2315).</div>
                            <div class="tile-footer"><span>Status: Enabled</span> <button class="btn-christ" style="padding:3px 8px; font-size:10.5px;" onclick="showToast('2FA settings synced')">Configure</button></div>
                        </div>

                        <div class="item-tile">
                            <div class="tile-name">Active Login Sessions</div>
                            <div class="tile-sub">Current: Linux Chrome • Bangalore Yeshwanthpur Wi-Fi (IP: 172.16.42.108)<br>Mobile: UniChrist Android APK • Session Active</div>
                            <div class="tile-footer"><span>2 Active Devices</span> <button class="btn-gold" style="padding:3px 8px; font-size:10.5px;" onclick="showToast('All other sessions revoked successfully')">Revoke Other</button></div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- ================= ADMIN: DASHBOARD & APPROVALS ================= -->
            <section id="page-admin" class="page-view">
                <div class="uni-card">
                    <div class="card-header-bar">
                        <h2 class="card-main-title"><i class="fa-solid fa-user-shield"></i> University Departmental &amp; Admin Console</h2>
                        <span class="status-chip chip-gold">HOD &amp; Authority Oversight</span>
                    </div>

                    <div class="kpi-scan-row" style="margin-bottom:16px;">
                        <div class="kpi-card kpi-blue">
                            <div class="kpi-top-row"><span>Total Students</span><i class="fa-solid fa-users"></i></div>
                            <div class="kpi-value">4,120</div>
                            <div class="kpi-subtitle">BYC Campus Enrolled</div>
                        </div>
                        <div class="kpi-card kpi-emerald">
                            <div class="kpi-top-row"><span>Average Attendance</span><i class="fa-solid fa-chart-pie"></i></div>
                            <div class="kpi-value">88.2%</div>
                            <div class="kpi-subtitle">Campus Compliance</div>
                        </div>
                        <div class="kpi-card kpi-amber">
                            <div class="kpi-top-row"><span>Pending Forms</span><i class="fa-solid fa-clock"></i></div>
                            <div class="kpi-value">3</div>
                            <div class="kpi-subtitle">Awaiting HOD Signature</div>
                        </div>
                        <div class="kpi-card kpi-purple">
                            <div class="kpi-top-row"><span>Active Lab Rooms</span><i class="fa-solid fa-door-open"></i></div>
                            <div class="kpi-value">28 / 32</div>
                            <div class="kpi-subtitle">In Scheduled Session</div>
                        </div>
                    </div>

                    <div class="item-tile">
                        <div class="tile-name" style="margin-bottom:8px;">Fast-Track Administrative Actions</div>
                        <div style="display:flex; gap:10px; flex-wrap:wrap;">
                            <button class="btn-christ" onclick="navigateTo('page-yellowblue')"><i class="fa-solid fa-check-double"></i> Review Yellow Forms</button>
                            <button class="btn-christ" onclick="navigateTo('page-freeroom')"><i class="fa-solid fa-door-open"></i> Manage Classrooms</button>
                            <button class="btn-christ" onclick="navigateTo('page-faculty')"><i class="fa-solid fa-users-gear"></i> Faculty Radar Roster</button>
                            <button class="btn-gold" onclick="navigateTo('page-examinations')"><i class="fa-solid fa-file-invoice"></i> COE Admittance Engine</button>
                        </div>
                    </div>
                </div>
            </section>
"""

# Insert before </main>
insert_target = "</main>"
if insert_target in text:
    text = text.replace(insert_target, missing_pages_html + "\n        " + insert_target)

with open('unichrist-web/build_portal.py', 'w') as f:
    f.write(text)

print("Successfully injected missing pages into build_portal.py!")
