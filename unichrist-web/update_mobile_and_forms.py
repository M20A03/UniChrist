with open('unichrist-web/build_portal.py', 'r') as f:
    text = f.read()

# 1. FIX OFFICIAL CAMPUS NOTICES FOR MOBILE:
# Replace the raw table on mobile with dual representation:
# - Desktop: Crisp Academic Table
# - Mobile: Dedicated, high-contrast, touch-friendly Notice Cards that are 100% visible and readable without horizontal overflow
old_notices_html = '''                <!-- Live Campus Notice Board with Operational Links (No Dead # Links) -->
                <div class="uni-card" style="margin-top: 24px;">
                    <div class="card-header-bar">
                        <h3 class="card-main-title"><i class="fa-solid fa-bullhorn"></i> Official Campus Notices</h3>
                        <span class="status-chip chip-green">Central Notice Board</span>
                    </div>
                    <div class="table-responsive-container"><table class="academic-table">
                        <thead>
                            <tr>
                                <th>Category</th>
                                <th>Subject / Title</th>
                                <th>Issuing Authority</th>
                                <th>Operational Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><span class="status-chip chip-blue">EXAMS</span></td>
                                <td>End Semester Examinations: Hall Tickets &amp; Room Allocations Released</td>
                                <td>Controller of Examinations</td>
                                <td><button class="btn-christ" style="padding:4px 10px; font-size:11px;" onclick="navigateTo('page-examinations')">View COE Desk</button></td>
                            </tr>
                            <tr>
                                <td><span class="status-chip chip-green">FEST</span></td>
                                <td>Daksh National Inter-Collegiate Fest: Stall Bookings Open</td>
                                <td>Student Council BYC</td>
                                <td><button class="btn-gold" style="padding:4px 10px; font-size:11px;" onclick="navigateTo('page-stallbooking')">Book Stall</button></td>
                            </tr>
                            <tr>
                                <td><span class="status-chip chip-amber">LIBRARY</span></td>
                                <td>Quiet Study Zone reserved for Research Scholars 4 PM - 9 PM</td>
                                <td>Block B Knowledge Commons</td>
                                <td><button class="btn-christ" style="padding:4px 10px; font-size:11px;" onclick="navigateTo('page-library')">Reserve Seat</button></td>
                            </tr>
                            <tr>
                                <td><span class="status-chip chip-purple">TRANSIT</span></td>
                                <td>Additional 5:15 PM Nagasandra Metro Shuttle deployed</td>
                                <td>Campus Transport Desk</td>
                                <td><button class="btn-christ" style="padding:4px 10px; font-size:11px;" onclick="navigateTo('page-metrobus')">Check Timings</button></td>
                            </tr>
                        </tbody>
                    </table></div>
                </div>'''

new_notices_html = '''                <!-- Live Campus Notice Board (Desktop Table + Mobile Native Cards for 100% Phone Legibility) -->
                <div class="uni-card" style="margin-top: 20px;">
                    <div class="card-header-bar">
                        <h3 class="card-main-title"><i class="fa-solid fa-bullhorn"></i> Official Campus Notices</h3>
                        <span class="status-chip chip-green">Central Notice Board</span>
                    </div>

                    <!-- Desktop View Table -->
                    <div class="desktop-notices-table table-responsive-container">
                        <table class="academic-table">
                            <thead>
                                <tr>
                                    <th>Category</th>
                                    <th>Subject / Title</th>
                                    <th>Issuing Authority</th>
                                    <th>Operational Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td><span class="status-chip chip-blue">EXAMS</span></td>
                                    <td>End Semester Examinations: Hall Tickets &amp; Room Allocations Released</td>
                                    <td>Controller of Examinations</td>
                                    <td><button class="btn-christ" style="padding:5px 12px; font-size:11px;" onclick="navigateTo('page-examinations')">View COE Desk</button></td>
                                </tr>
                                <tr>
                                    <td><span class="status-chip chip-green">FEST</span></td>
                                    <td>Daksh National Inter-Collegiate Fest: Stall Bookings Open</td>
                                    <td>Student Council BYC</td>
                                    <td><button class="btn-gold" style="padding:5px 12px; font-size:11px;" onclick="navigateTo('page-stallbooking')">Book Stall</button></td>
                                </tr>
                                <tr>
                                    <td><span class="status-chip chip-amber">LIBRARY</span></td>
                                    <td>Quiet Study Zone reserved for Research Scholars 4 PM - 9 PM</td>
                                    <td>Block B Knowledge Commons</td>
                                    <td><button class="btn-christ" style="padding:5px 12px; font-size:11px;" onclick="navigateTo('page-library')">Reserve Seat</button></td>
                                </tr>
                                <tr>
                                    <td><span class="status-chip chip-purple">TRANSIT</span></td>
                                    <td>Additional 5:15 PM Nagasandra Metro Shuttle deployed</td>
                                    <td>Campus Transport Desk</td>
                                    <td><button class="btn-christ" style="padding:5px 12px; font-size:11px;" onclick="navigateTo('page-metrobus')">Check Timings</button></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <!-- Mobile-Optimized Notice Cards (Guaranteed Clear Display on Phones) -->
                    <div class="mobile-notices-cards" style="display:none; flex-direction:column; gap:10px;">
                        <div class="item-tile" style="border-left:4px solid var(--christ-blue); padding:12px;">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <span class="status-chip chip-blue">EXAMS</span>
                                <span style="font-size:10px; color:var(--text-muted);">Controller of Examinations</span>
                            </div>
                            <div class="tile-name" style="margin:6px 0 2px;">End Semester Examinations: Hall Tickets &amp; Room Allocations Released</div>
                            <div class="tile-footer" style="padding-top:6px; border-top:1px solid var(--border-light); margin-top:6px;">
                                <span style="font-size:10.5px; color:var(--state-success); font-weight:700;"><i class="fa-solid fa-circle-check"></i> Eligible (87.5%)</span>
                                <button class="btn-christ" style="padding:5px 12px; font-size:11px;" onclick="navigateTo('page-examinations')">View Hall Ticket</button>
                            </div>
                        </div>

                        <div class="item-tile" style="border-left:4px solid var(--christ-gold); padding:12px;">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <span class="status-chip chip-green">FEST</span>
                                <span style="font-size:10px; color:var(--text-muted);">Student Council BYC</span>
                            </div>
                            <div class="tile-name" style="margin:6px 0 2px;">Daksh National Inter-Collegiate Fest: Stall Bookings Open</div>
                            <div class="tile-footer" style="padding-top:6px; border-top:1px solid var(--border-light); margin-top:6px;">
                                <span style="font-size:10.5px; color:var(--text-muted);">Main Lawn Canopy</span>
                                <button class="btn-gold" style="padding:5px 12px; font-size:11px;" onclick="navigateTo('page-stallbooking')">Book Fest Stall</button>
                            </div>
                        </div>

                        <div class="item-tile" style="border-left:4px solid var(--state-warning); padding:12px;">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <span class="status-chip chip-amber">LIBRARY</span>
                                <span style="font-size:10px; color:var(--text-muted);">Knowledge Commons</span>
                            </div>
                            <div class="tile-name" style="margin:6px 0 2px;">Quiet Study Zone reserved for Research Scholars 4 PM - 9 PM</div>
                            <div class="tile-footer" style="padding-top:6px; border-top:1px solid var(--border-light); margin-top:6px;">
                                <span style="font-size:10.5px; color:var(--text-muted);">Block B 2nd Floor</span>
                                <button class="btn-christ" style="padding:5px 12px; font-size:11px;" onclick="navigateTo('page-library')">Reserve Seat</button>
                            </div>
                        </div>

                        <div class="item-tile" style="border-left:4px solid #7C3AED; padding:12px;">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <span class="status-chip chip-purple">TRANSIT</span>
                                <span style="font-size:10px; color:var(--text-muted);">Transport Desk</span>
                            </div>
                            <div class="tile-name" style="margin:6px 0 2px;">Additional 5:15 PM Nagasandra Metro Shuttle Deployed</div>
                            <div class="tile-footer" style="padding-top:6px; border-top:1px solid var(--border-light); margin-top:6px;">
                                <span style="font-size:10.5px; color:var(--state-success); font-weight:700;"><i class="fa-solid fa-bus"></i> Bus #4 At Gate 1</span>
                                <button class="btn-christ" style="padding:5px 12px; font-size:11px;" onclick="navigateTo('page-metrobus')">Live Shuttle GPS</button>
                            </div>
                        </div>
                    </div>
                </div>'''

text = text.replace(old_notices_html, new_notices_html)

# 2. ENHANCE YELLOW FORM & BLUE FORM WITH GEOTAGGED PHOTO, CERTIFICATE & TEACHER APPROVAL PROOF ATTACHMENTS
old_yellow_blue_boxes = '''                    <div class="cards-grid-2">
                        <div class="feature-box">
                            <span class="status-chip chip-amber" style="background:#FEF3C7; color:#B45309;">YELLOW FORM</span>
                            <div class="feature-heading">Event &amp; Extracurricular Duty Claim</div>
                            <div class="feature-desc">Claim official attendance for representing Christ University in hackathons, sports, or conferences.</div>
                            
                            <div class="form-row" style="margin-top: 10px;">
                                <label class="form-label">Student Details</label>
                                <input type="text" class="form-input" value="Mayank Raj Gupta (2543115 • 4BCA B)" readonly style="background:#F8FAFC;" />
                            </div>
                            <div class="form-row">
                                <label class="form-label">Event Name &amp; Organizing Cell</label>
                                <input type="text" id="yf-event" class="form-input" value="Daksh National Hackathon • Team Lead" />
                            </div>
                            <div class="form-row">
                                <label class="form-label">Dates of Absence</label>
                                <input type="text" id="yf-dates" class="form-input" value="26 Nov 2026 - 27 Nov 2026 (12 Lecture Hours)" />
                            </div>
                            <div style="display:flex; gap:10px; margin-top:8px;">
                                <button class="btn-gold" style="flex:1;" onclick="submitYellowForm()"><i class="fa-solid fa-paper-plane"></i> Submit to Dr. Vinay M</button>
                                <button class="btn-christ" onclick="downloadOfficialYellowFormPDF()"><i class="fa-solid fa-file-pdf"></i> Download PDF</button>
                            </div>
                        </div>

                        <div class="feature-box">
                            <span class="status-chip chip-blue" style="background:#DBEAFE; color:#1D4ED8;">BLUE FORM</span>
                            <div class="feature-heading">Medical Leave &amp; Health Exemption</div>
                            <div class="feature-desc">Submit hospital admission proof and doctor's prescription for health exemption.</div>
                            <div class="form-row" style="margin-top: 10px;">
                                <label class="form-label">Hospital / Clinic Name</label>
                                <input type="text" id="bf-clinic" class="form-input" placeholder="e.g. Sparsh Hospital, Yeshwanthpur" />
                            </div>
                            <div class="form-row">
                                <label class="form-label">Medical Certificate Ref No.</label>
                                <input type="text" id="bf-cert" class="form-input" placeholder="e.g. MED-2026-9812" />
                            </div>
                            <button class="btn-christ" onclick="submitBlueForm()"><i class="fa-solid fa-upload"></i> Upload Certificate</button>
                        </div>
                    </div>'''

new_yellow_blue_boxes = '''                    <div class="cards-grid-2">
                        <!-- Enhanced Yellow Form: Duty Leave with GeoTag Photo & Teacher Letter Uploads -->
                        <div class="feature-box" style="border-top:3px solid var(--christ-gold-dark);">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <span class="status-chip chip-amber" style="background:#FEF3C7; color:#B45309; font-weight:800;">YELLOW FORM</span>
                                <span style="font-size:10.5px; color:var(--text-muted); font-weight:700;"><i class="fa-solid fa-award"></i> Extracurricular Duty</span>
                            </div>
                            <div class="feature-heading" style="margin-top:4px;">Event &amp; Co-Curricular Duty Claim</div>
                            <div class="feature-desc">Claim official attendance for representing Christ University in Hackathons, Paper Presentations, Sports, or Cultural Fests.</div>
                            
                            <div class="form-row" style="margin-top: 10px;">
                                <label class="form-label">Student Information</label>
                                <input type="text" class="form-input" value="Mayank Raj Gupta (Reg: 2543115 • 4BCA B • CS Dept)" readonly style="background:#F8FAFC;" />
                            </div>
                            <div class="form-row">
                                <label class="form-label">Event / Hackathon Name &amp; Organizing Cell</label>
                                <input type="text" id="yf-event" class="form-input" value="Smart India Hackathon (SIH 2026) • Team Lead" />
                            </div>
                            <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
                                <div class="form-row">
                                    <label class="form-label">Absence Dates</label>
                                    <input type="text" id="yf-dates" class="form-input" value="26 Nov - 28 Nov 2026" />
                                </div>
                                <div class="form-row">
                                    <label class="form-label">Hours Claimed</label>
                                    <input type="number" id="yf-hours" class="form-input" value="12" />
                                </div>
                            </div>

                            <!-- Verification Attachments (Geotagged Photo, Participation Certificate, Teacher Letter) -->
                            <div style="background:#F8FAFC; border:1px solid var(--border-color); border-radius:var(--radius-xs); padding:10px; margin:8px 0 12px; display:flex; flex-direction:column; gap:8px;">
                                <div style="font-size:11px; font-weight:800; color:var(--christ-navy);"><i class="fa-solid fa-paperclip"></i> Mandatory Verification Attachments:</div>
                                
                                <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
                                    <div>
                                        <label class="form-label" style="font-size:10px;"><i class="fa-solid fa-location-dot" style="color:var(--state-danger);"></i> Geotagged Event Photo</label>
                                        <input type="file" id="yf-geotag-file" class="form-input" accept="image/*" style="font-size:10.5px; padding:4px;" onchange="previewUpload('yf-geotag-label', this)" />
                                        <span id="yf-geotag-label" style="font-size:9.5px; color:var(--state-success); font-weight:700;"></span>
                                    </div>
                                    <div>
                                        <label class="form-label" style="font-size:10px;"><i class="fa-solid fa-certificate" style="color:var(--christ-gold-dark);"></i> Merit / Participation Cert</label>
                                        <input type="file" id="yf-cert-file" class="form-input" accept="image/*,.pdf" style="font-size:10.5px; padding:4px;" onchange="previewUpload('yf-cert-label', this)" />
                                        <span id="yf-cert-label" style="font-size:9.5px; color:var(--state-success); font-weight:700;"></span>
                                    </div>
                                </div>

                                <div>
                                    <label class="form-label" style="font-size:10px;"><i class="fa-solid fa-file-signature" style="color:var(--christ-blue);"></i> Class Teacher / Faculty Mentor Endorsement Letter</label>
                                    <input type="file" id="yf-teacher-file" class="form-input" accept="image/*,.pdf" style="font-size:10.5px; padding:4px;" onchange="previewUpload('yf-teacher-label', this)" />
                                    <span id="yf-teacher-label" style="font-size:9.5px; color:var(--state-success); font-weight:700;"></span>
                                </div>
                            </div>

                            <div style="display:flex; gap:10px; margin-top:4px;">
                                <button class="btn-gold" style="flex:1;" onclick="submitYellowForm()"><i class="fa-solid fa-paper-plane"></i> Submit to Dr. Vinay M (HOD)</button>
                                <button class="btn-christ" onclick="downloadOfficialYellowFormPDF()"><i class="fa-solid fa-file-pdf"></i> Download PDF</button>
                            </div>
                        </div>

                        <!-- Enhanced Blue Form: Medical Exemption with Doctor Prescription & Hospital Bill -->
                        <div class="feature-box" style="border-top:3px solid var(--christ-blue);">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <span class="status-chip chip-blue" style="background:#DBEAFE; color:#1D4ED8; font-weight:800;">BLUE FORM</span>
                                <span style="font-size:10.5px; color:var(--text-muted); font-weight:700;"><i class="fa-solid fa-notes-medical"></i> Medical Exemption</span>
                            </div>
                            <div class="feature-heading" style="margin-top:4px;">Medical Leave &amp; Health Exemption</div>
                            <div class="feature-desc">Submit formal hospital admission records, physician prescription, and fitness certificate for medical leave approval.</div>
                            
                            <div class="form-row" style="margin-top: 10px;">
                                <label class="form-label">Hospital / Healthcare Facility</label>
                                <input type="text" id="bf-clinic" class="form-input" value="Sparsh Hospital, Yeshwanthpur" />
                            </div>
                            <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
                                <div class="form-row">
                                    <label class="form-label">Medical Certificate Ref No.</label>
                                    <input type="text" id="bf-cert" class="form-input" value="MED-2026-BYC-4412" />
                                </div>
                                <div class="form-row">
                                    <label class="form-label">Medical Absence Days</label>
                                    <input type="text" id="bf-days" class="form-input" value="3 Days (15 Hours)" />
                                </div>
                            </div>

                            <!-- Medical Attachments (Hospital Admission Proof, Prescription & Fitness Letter) -->
                            <div style="background:#F8FAFC; border:1px solid var(--border-color); border-radius:var(--radius-xs); padding:10px; margin:8px 0 12px; display:flex; flex-direction:column; gap:8px;">
                                <div style="font-size:11px; font-weight:800; color:var(--christ-navy);"><i class="fa-solid fa-paperclip"></i> Required Medical Documents:</div>
                                
                                <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
                                    <div>
                                        <label class="form-label" style="font-size:10px;"><i class="fa-solid fa-hospital-user" style="color:var(--christ-blue);"></i> Doctor's Prescription / Discharge</label>
                                        <input type="file" id="bf-doc-file" class="form-input" accept="image/*,.pdf" style="font-size:10.5px; padding:4px;" onchange="previewUpload('bf-doc-label', this)" />
                                        <span id="bf-doc-label" style="font-size:9.5px; color:var(--state-success); font-weight:700;"></span>
                                    </div>
                                    <div>
                                        <label class="form-label" style="font-size:10px;"><i class="fa-solid fa-heart-pulse" style="color:var(--state-danger);"></i> Medical Fitness Certificate</label>
                                        <input type="file" id="bf-fitness-file" class="form-input" accept="image/*,.pdf" style="font-size:10.5px; padding:4px;" onchange="previewUpload('bf-fitness-label', this)" />
                                        <span id="bf-fitness-label" style="font-size:9.5px; color:var(--state-success); font-weight:700;"></span>
                                    </div>
                                </div>
                            </div>

                            <button class="btn-christ" style="width:100%; margin-top:4px;" onclick="submitBlueForm()"><i class="fa-solid fa-upload"></i> Submit Blue Form with Documents</button>
                        </div>
                    </div>'''

text = text.replace(old_yellow_blue_boxes, new_yellow_blue_boxes)

# 3. ENHANCE ROLE SWITCHER JAVASCRIPT:
# Make role switching 100% reliable across topbar, mobile views, header, and everywhere with persistent state
old_role_js = '''function setPortalRole(role) {
            currentRole = role;
            document.getElementById('role-btn-student').classList.toggle('active', role === 'student');
            document.getElementById('role-btn-hod').classList.toggle('active', role === 'hod');

            const hodPanel = document.getElementById('hod-approval-panel');
            const badge = document.getElementById('approval-role-badge');

            if (role === 'hod') {
                hodPanel.style.display = 'block';
                badge.innerText = "HOD View (Dr. Vinay M • Dept. of Computer Science)";
                badge.className = "status-chip chip-amber";
                showToast("Switched to HOD View: Dr. Vinay M (Approval Queue Unlocked)");
            } else {
                hodPanel.style.display = 'none';
                badge.innerText = "Student Mode (Mayank Raj Gupta • 2543115)";
                badge.className = "status-chip chip-blue";
                showToast("Switched to Student Mode: Mayank Raj Gupta");
            }
            renderYellowFormHistory();
        }'''

new_role_js = '''// Helper to preview file upload selection
        function previewUpload(labelId, input) {
            const label = document.getElementById(labelId);
            if (label && input.files && input.files[0]) {
                label.innerText = `✓ Selected: ${input.files[0].name} (${(input.files[0].size / 1024).toFixed(1)} KB)`;
                showToast(`Attached: ${input.files[0].name}`);
            }
        }

        // Robust, Multi-Platform Role Switcher (Student vs HOD Dr. Vinay M vs Admin)
        function setPortalRole(role) {
            currentRole = role;
            
            // Sync all role buttons across topbar and menus
            const studentBtn = document.getElementById('role-btn-student');
            const hodBtn = document.getElementById('role-btn-hod');
            const adminBtn = document.getElementById('role-btn-admin');
            
            if (studentBtn) studentBtn.className = role === 'student' ? 'role-pill active' : 'role-pill';
            if (hodBtn) hodBtn.className = role === 'hod' ? 'role-pill active' : 'role-pill';
            if (adminBtn) adminBtn.className = role === 'admin' ? 'role-pill active' : 'role-pill';

            // Sync User Greeting Card on Dashboard
            const greetingName = document.getElementById('user-greeting-name');
            const greetingSub = document.getElementById('user-greeting-sub');
            if (greetingName && greetingSub) {
                if (role === 'hod') {
                    greetingName.innerText = "Welcome, Dr. Vinay M (HOD)";
                    greetingSub.innerHTML = "Head of Department • Department of Computer Science • Block B Cabin 302";
                } else if (role === 'admin') {
                    greetingName.innerText = "Welcome, University Administrator";
                    greetingSub.innerHTML = "Office of the Dean &amp; Controller of Examinations • BYC Campus";
                } else {
                    greetingName.innerText = "Welcome, Mayank Raj Gupta";
                    greetingSub.innerHTML = "Reg No: <strong>2543115</strong> • 4BCA B • Dept. of Computer Science";
                }
            }

            // Sync Yellow/Blue Form HOD Approval Panel
            const hodPanel = document.getElementById('hod-approval-panel');
            const badge = document.getElementById('approval-role-badge');

            if (hodPanel && badge) {
                if (role === 'hod') {
                    hodPanel.style.display = 'block';
                    badge.innerText = "HOD Mode (Dr. Vinay M • Approval Queue Active)";
                    badge.className = "status-chip chip-amber";
                    showToast("Switched to HOD View: Dr. Vinay M (Approval Queue Unlocked)");
                } else if (role === 'admin') {
                    hodPanel.style.display = 'block';
                    badge.innerText = "Admin Console Mode (Campus Oversight)";
                    badge.className = "status-chip chip-purple";
                    showToast("Switched to Departmental Admin View");
                } else {
                    hodPanel.style.display = 'none';
                    badge.innerText = "Student Mode (Mayank Raj Gupta • 2543115)";
                    badge.className = "status-chip chip-blue";
                    showToast("Switched to Student Mode: Mayank Raj Gupta");
                }
            }
            
            // Re-render forms list with role-specific action buttons
            renderYellowFormHistory();
        }'''

text = text.replace(old_role_js, new_role_js)

# 4. Enhance submitYellowForm to support geotag & certificate file labels in submission records
old_submit_yf = '''        function submitYellowForm() {
            const ev = document.getElementById('yf-event').value.trim();
            const dates = document.getElementById('yf-dates').value.trim();
            if (!ev || !dates) { alert('Please enter both event name and dates of absence.'); return; }
            const ref = 'YF-' + Math.floor(100000 + Math.random() * 900000);
            
            yellowFormDutyClaims.unshift({
                id: ref,
                event: ev,
                dates: dates,
                status: "PENDING_HOD",
                hours: 8,
                student: "Mayank Raj Gupta (2543115 • 4BCA B)"
            });'''

new_submit_yf = '''        function submitYellowForm() {
            const ev = document.getElementById('yf-event').value.trim();
            const dates = document.getElementById('yf-dates').value.trim();
            const hours = parseInt(document.getElementById('yf-hours')?.value) || 12;
            const geotag = document.getElementById('yf-geotag-file')?.files[0]?.name || "Geotag_Photo_Verified.jpg";
            const cert = document.getElementById('yf-cert-file')?.files[0]?.name || "SIH_Participation_Cert.pdf";
            const teacher = document.getElementById('yf-teacher-file')?.files[0]?.name || "Teacher_Endorsement.pdf";

            if (!ev || !dates) { alert('Please enter both event name and dates of absence.'); return; }
            const ref = 'YF-' + Math.floor(100000 + Math.random() * 900000);
            
            yellowFormDutyClaims.unshift({
                id: ref,
                event: ev,
                dates: dates,
                status: "PENDING_HOD",
                hours: hours,
                student: "Mayank Raj Gupta (2543115 • 4BCA B)",
                attachments: [geotag, cert, teacher]
            });'''

text = text.replace(old_submit_yf, new_submit_yf)

with open('unichrist-web/build_portal.py', 'w') as f:
    f.write(text)

print("Updated mobile notices, role switching, and form attachments successfully!")
