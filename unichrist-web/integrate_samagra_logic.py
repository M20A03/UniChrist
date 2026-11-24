with open('unichrist-web/build_portal.py', 'r') as f:
    text = f.read()

# 1. Update Attendance Calculator UI with Samagra Blue & Yellow Form Fields & Target Slider
old_att_html = '''                    <div class="cards-grid-2">
                        <div class="meter-card">
                            <div class="form-row">
                                <label class="form-label">Total Classes Conducted</label>
                                <input type="number" id="att-total" class="form-input" value="60" oninput="calculateAttendance()" />
                            </div>
                            <div class="form-row">
                                <label class="form-label">Total Classes Attended</label>
                                <input type="number" id="att-attended" class="form-input" value="48" oninput="calculateAttendance()" />
                            </div>
                            <div class="form-row">
                                <label class="form-label">Target Mandatory Threshold</label>
                                <input type="text" class="form-input" value="85% (Official Christ Standard)" disabled />
                            </div>
                        </div>

                        <div class="meter-card" style="justify-content: center; align-items: center; text-align: center;">
                            <div style="font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Current Standing</div>
                            <div id="att-percent-display" style="font-size: 44px; font-weight: 800; color: var(--christ-emerald); line-height: 1.1; margin: 8px 0;">80.0%</div>
                            <div class="meter-bar-outer" style="width: 80%; margin: 8px 0 14px;">
                                <div id="att-bar" class="meter-bar-fill" style="width: 80%; background: var(--christ-emerald);"></div>
                            </div>
                            <div id="att-recommendation" style="font-size: 12.5px; color: var(--text-heading); max-width: 320px; line-height: 1.5;">
                                Recalculating attendance metrics...
                            </div>
                            <button class="btn-christ" style="margin-top:14px;" onclick="exportAttendanceReport()"><i class="fa-solid fa-file-arrow-down"></i> Export Attendance Report (PDF)</button>
                        </div>
                    </div>'''

new_att_html = '''                    <!-- Samagra Official Attendance Engine with Blue & Yellow Form Duty Leaves -->
                    <div class="cards-grid-2">
                        <div class="meter-card">
                            <div style="font-size:12px; font-weight:700; color:var(--christ-navy); margin-bottom:10px; border-bottom:1px solid var(--border-light); padding-bottom:6px;">
                                <i class="fa-solid fa-calculator"></i> Attendance &amp; Form Input Parameters (Samagra Engine)
                            </div>
                            <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
                                <div class="form-row">
                                    <label class="form-label">Total Conducted</label>
                                    <input type="number" id="att-total" class="form-input" value="60" oninput="calculateAttendance()" />
                                </div>
                                <div class="form-row">
                                    <label class="form-label">Physically Attended</label>
                                    <input type="number" id="att-attended" class="form-input" value="48" oninput="calculateAttendance()" />
                                </div>
                            </div>
                            <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-top:4px;">
                                <div class="form-row">
                                    <label class="form-label" title="Duty leave for fests, sports & hackathons"><i class="fa-solid fa-file-invoice" style="color:var(--christ-blue);"></i> Blue Form (Hours)</label>
                                    <input type="number" id="att-blue-hours" class="form-input" value="4" oninput="calculateAttendance()" />
                                </div>
                                <div class="form-row">
                                    <label class="form-label" title="Official medical leave claim"><i class="fa-solid fa-file-medical" style="color:var(--christ-gold-dark);"></i> Yellow Form (Hours)</label>
                                    <input type="number" id="att-yellow-hours" class="form-input" value="2" oninput="calculateAttendance()" />
                                </div>
                            </div>
                            <div class="form-row" style="margin-top:4px;">
                                <div style="display:flex; justify-content:space-between;">
                                    <label class="form-label">Target Compliance Threshold</label>
                                    <span id="target-threshold-label" style="font-size:12px; font-weight:800; color:var(--christ-navy);">85%</span>
                                </div>
                                <input type="range" id="att-target-slider" min="70" max="95" value="85" class="form-range" style="width:100%; accent-color:var(--christ-navy);" oninput="updateTargetThreshold(this.value)" />
                            </div>
                        </div>

                        <div class="meter-card" style="justify-content: center; align-items: center; text-align: center;">
                            <div style="font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Official Evaluation Standing</div>
                            <div id="att-percent-display" style="font-size: 42px; font-weight: 800; color: var(--state-success); line-height: 1.1; margin: 6px 0;">90.0%</div>
                            <div id="att-breakdown-sub" style="font-size:11.5px; color:var(--text-muted); font-weight:600; margin-bottom:8px;">Raw: 80.0% • Effective: 90.0% (with Approved Claims)</div>
                            
                            <div class="meter-bar-outer" style="width: 85%; margin: 4px 0 12px;">
                                <div id="att-bar" class="meter-bar-fill" style="width: 90%; background: var(--state-success);"></div>
                            </div>
                            <div id="att-recommendation" style="font-size: 12.5px; color: var(--text-heading); max-width: 360px; line-height: 1.5;">
                                Recalculating attendance metrics...
                            </div>
                            <div style="display:flex; gap:8px; margin-top:14px;">
                                <button class="btn-christ" style="font-size:11.5px;" onclick="exportAttendanceReport()"><i class="fa-solid fa-file-arrow-down"></i> Export PDF Report</button>
                                <button class="btn-gold" style="font-size:11.5px;" onclick="navigateTo('page-yellowblue')"><i class="fa-solid fa-file-circle-plus"></i> Claim Duty Form</button>
                            </div>
                        </div>
                    </div>'''

text = text.replace(old_att_html, new_att_html)

# 2. Update Marks & SGPA Calculator UI with Samagra 4.0 Scale & Target Goal Selector
old_marks_html = '''                    <div class="cards-grid-2">
                        <div class="meter-card">
                            <div class="form-row">
                                <label class="form-label">CIA 1 Score (out of 20)</label>
                                <input type="number" id="cia1" class="form-input" value="18" oninput="calculateGPA()" />
                            </div>
                            <div class="form-row">
                                <label class="form-label">CIA 2 / Mid-Sem Score (out of 50)</label>
                                <input type="number" id="cia2" class="form-input" value="42" oninput="calculateGPA()" />
                            </div>
                            <div class="form-row">
                                <label class="form-label">CIA 3 Assessment Score (out of 20)</label>
                                <input type="number" id="cia3" class="form-input" value="19" oninput="calculateGPA()" />
                            </div>
                            <div class="form-row">
                                <label class="form-label">Expected End-Sem (ESE) Theory Score (out of 100)</label>
                                <input type="number" id="ese-expected" class="form-input" value="82" oninput="calculateGPA()" />
                            </div>
                        </div>

                        <div class="meter-card" style="justify-content: center; align-items: center; text-align: center;">
                            <div style="font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Predicted Academic SGPA</div>
                            <div id="gpa-score-display" style="font-size: 44px; font-weight: 800; color: var(--christ-navy); line-height: 1.1; margin: 8px 0;">8.54</div>
                            <span id="grade-badge" class="status-chip chip-green" style="font-size: 12px; padding: 4px 12px; margin-bottom: 12px;">GRADE: A+ (Excellent)</span>
                            <div id="gpa-breakdown" style="font-size: 12px; color: var(--text-muted); max-width: 320px; line-height: 1.6;">
                                Total Computed Marks: <strong>85.4 / 100</strong><br>
                                CIA Contribution: 44.4 / 50 • ESE Contribution: 41.0 / 50
                            </div>
                        </div>
                    </div>'''

new_marks_html = '''                    <!-- Samagra Official 4.0 Scale & Target ESE Predictor -->
                    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:14px; background:#F8FAFC; border:1px solid var(--border-color); padding:10px 14px; border-radius:var(--radius-xs);">
                        <div style="display:flex; align-items:center; gap:8px;">
                            <span style="font-size:12px; font-weight:700; color:var(--christ-navy);">Grading System Scale:</span>
                            <button id="scale-btn-4" class="btn-christ" style="padding:4px 10px; font-size:11px;" onclick="switchScaleMode('4.0')">Official 4.0 Scale</button>
                            <button id="scale-btn-10" class="btn-gold" style="padding:4px 10px; font-size:11px; opacity:0.8;" onclick="switchScaleMode('10.0')">10.0 Point Scale</button>
                        </div>
                        <div style="display:flex; align-items:center; gap:8px;">
                            <span style="font-size:12px; font-weight:700; color:var(--christ-navy);">Target Goal:</span>
                            <select id="target-goal-select" class="form-select" style="padding:4px 8px; font-size:11.5px; font-weight:700;" onchange="calculateGPA()">
                                <option value="O" selected>Grade O (80%+ / 4.0 Point)</option>
                                <option value="DISTINCTION">First Class Distinction (75%+)</option>
                                <option value="A+">Grade A+ (70%+ / 3.6 Point)</option>
                                <option value="A">Grade A (60%+ / 3.2 Point)</option>
                                <option value="B+">Grade B+ (55%+ / 2.8 Point)</option>
                                <option value="PASS">Pass Class (40%+ / 1.6 Point)</option>
                            </select>
                        </div>
                    </div>

                    <div class="cards-grid-2">
                        <div class="meter-card">
                            <div style="font-size:12px; font-weight:700; color:var(--christ-navy); margin-bottom:10px; border-bottom:1px solid var(--border-light); padding-bottom:6px;">
                                <i class="fa-solid fa-list-check"></i> Internal Assessment (CIA) Component Marks
                            </div>
                            <div class="form-row">
                                <label class="form-label">CIA 1 Assessment (Scored out of 20)</label>
                                <input type="number" id="cia1" class="form-input" value="18" oninput="calculateGPA()" />
                            </div>
                            <div class="form-row">
                                <label class="form-label">Mid-Sem Exam / CIA 2 (Scored out of 50)</label>
                                <input type="number" id="cia2" class="form-input" value="42" oninput="calculateGPA()" />
                            </div>
                            <div class="form-row">
                                <label class="form-label">CIA 3 Assessment / Project (Scored out of 20)</label>
                                <input type="number" id="cia3" class="form-input" value="19" oninput="calculateGPA()" />
                            </div>
                            <div class="form-row">
                                <label class="form-label">Attendance Component (Scored out of 5)</label>
                                <input type="number" id="cia-att" class="form-input" value="5" oninput="calculateGPA()" />
                            </div>
                            <div class="form-row">
                                <label class="form-label">Expected ESE Question Paper Marks (out of 100)</label>
                                <input type="number" id="ese-expected" class="form-input" value="82" oninput="calculateGPA()" />
                            </div>
                        </div>

                        <div class="meter-card" style="justify-content: center; align-items: center; text-align: center;">
                            <div style="font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Official Christ Academic SGPA</div>
                            <div id="gpa-score-display" style="font-size: 42px; font-weight: 800; color: var(--christ-navy); line-height: 1.1; margin: 6px 0;">3.82 / 4.0</div>
                            <span id="grade-badge" class="status-chip chip-green" style="font-size: 12px; padding: 4px 12px; margin-bottom: 10px;">GRADE: O (Outstanding)</span>
                            <div id="result-division-badge" class="status-chip chip-blue" style="margin-bottom:10px; font-size:11px;">First Class with Distinction</div>
                            
                            <div id="gpa-breakdown" style="font-size: 11.5px; color: var(--text-muted); max-width: 340px; line-height: 1.6; text-align:left; background:#F8FAFC; border:1px solid var(--border-color); padding:10px 12px; border-radius:var(--radius-xs);">
                                Total Scaled Course Marks: <strong>85.4 / 100</strong><br>
                                CIA Contribution: 44.4 / 50 • ESE Contribution: 41.0 / 50<br>
                                Required ESE Exam Score for Target: <strong id="ese-target-needed">40 / 100</strong>
                            </div>
                            <button class="btn-christ" style="margin-top:12px; font-size:11.5px;" onclick="copyAcademicSummary()"><i class="fa-solid fa-copy"></i> Copy Academic Report</button>
                        </div>
                    </div>'''

text = text.replace(old_marks_html, new_marks_html)

# 3. Inject Full Samagra Logic Functions in Script
samagra_js_code = """
        // ==========================================================================
        // SAMAGRA REPOSITORY OFFICIAL CALCULATION ENGINES
        // Christ University 4.0 Point Scale & Attendance Duty Leave Rules
        // ==========================================================================
        let activeScaleMode = "4.0"; // '4.0' or '10.0'

        const SAMAGRA_4_SCALE = {
            O: { point: 4.0, label: '80% & Above', grade: 'O', desc: 'Outstanding' },
            'A+': { point: 3.6, label: '70% – 79.99%', grade: 'A+', desc: 'Excellent' },
            A: { point: 3.2, label: '60% – 69.99%', grade: 'A', desc: 'Very Good' },
            'B+': { point: 2.8, label: '55% – 59.99%', grade: 'B+', desc: 'Good' },
            B: { point: 2.4, label: '50% – 54.99%', grade: 'B', desc: 'Above Average' },
            C: { point: 2.0, label: '45% – 49.99%', grade: 'C', desc: 'Average' },
            P: { point: 1.6, label: '40% – 44.99%', grade: 'P', desc: 'Pass' },
            F: { point: 0.0, label: 'Less than 40%', grade: 'F', desc: 'Fail / Reappear' }
        };

        const SAMAGRA_10_SCALE = {
            O: { point: 10.0, label: '90–100%', grade: 'O', desc: 'Outstanding' },
            'A+': { point: 9.0, label: '80–89%', grade: 'A+', desc: 'Excellent' },
            A: { point: 8.0, label: '70–79%', grade: 'A', desc: 'Very Good' },
            'B+': { point: 7.0, label: '60–69%', grade: 'B+', desc: 'Good' },
            B: { point: 6.0, label: '55–59%', grade: 'B', desc: 'Above Average' },
            C: { point: 5.0, label: '50–54%', grade: 'C', desc: 'Average' },
            P: { point: 4.0, label: '40–49%', grade: 'P', desc: 'Pass' },
            F: { point: 0.0, label: '<40%', grade: 'F', desc: 'Fail' }
        };

        function switchScaleMode(mode) {
            activeScaleMode = mode;
            const btn4 = document.getElementById('scale-btn-4');
            const btn10 = document.getElementById('scale-btn-10');
            if (btn4 && btn10) {
                if (mode === '4.0') {
                    btn4.className = 'btn-christ';
                    btn10.className = 'btn-gold';
                    btn10.style.opacity = '0.8';
                    btn4.style.opacity = '1.0';
                } else {
                    btn10.className = 'btn-christ';
                    btn4.className = 'btn-gold';
                    btn4.style.opacity = '0.8';
                    btn10.style.opacity = '1.0';
                }
            }
            calculateGPA();
        }

        function updateTargetThreshold(val) {
            document.getElementById('target-threshold-label').innerText = val + "%";
            calculateAttendance();
        }

        // 1. Samagra Attendance Calculation Engine
        function calculateAttendance() {
            const conducted = Math.max(1, parseInt(document.getElementById('att-total').value) || 60);
            const attended = Math.max(0, parseInt(document.getElementById('att-attended').value) || 48);
            const blueClaims = Math.max(0, parseInt(document.getElementById('att-blue-hours')?.value) || 0);
            const yellowClaims = Math.max(0, parseInt(document.getElementById('att-yellow-hours')?.value) || 0);
            const targetSlider = document.getElementById('att-target-slider');
            const target = targetSlider ? parseInt(targetSlider.value) : 85;

            const totalEffectiveAttended = attended + blueClaims + yellowClaims;
            const currentRawPercentage = Math.min(100, (attended / conducted) * 100).toFixed(1);
            const currentAdjustedPercentage = Math.min(100, (totalEffectiveAttended / conducted) * 100).toFixed(1);

            const disp = document.getElementById('att-percent-display');
            const bar = document.getElementById('att-bar');
            const sub = document.getElementById('att-breakdown-sub');
            const rec = document.getElementById('att-recommendation');

            if (!disp) return;

            disp.innerText = currentAdjustedPercentage + "%";
            bar.style.width = Math.min(parseFloat(currentAdjustedPercentage), 100) + "%";
            sub.innerText = `Raw: ${currentRawPercentage}% • Effective: ${currentAdjustedPercentage}% (with Duty Claims)`;

            if (parseFloat(currentAdjustedPercentage) >= target) {
                bar.style.background = "var(--state-success)";
                disp.style.color = "var(--state-success)";
                // Max absences permitted while staying at or above target
                const maxCanMiss = Math.max(0, Math.floor((totalEffectiveAttended * 100) / target - conducted));
                rec.innerHTML = `<span style="color:var(--state-success); font-weight:700;">Compliant!</span> You hold a permissible absence margin of <strong>${maxCanMiss} lecture hours</strong> while remaining at or above ${target}%.`;
            } else {
                bar.style.background = "var(--state-danger)";
                disp.style.color = "var(--state-danger)";
                // Consecutive lectures needed without absence
                const needed = Math.ceil((target * conducted - 100 * totalEffectiveAttended) / (100 - target));
                rec.innerHTML = `<span style="color:var(--state-danger); font-weight:700;">Shortage Alert!</span> You must attend the next <strong>${needed} consecutive lectures</strong> with zero absences to hit ${target}%.`;
            }
        }

        // 2. Samagra Marks & SGPA Calculator Engine
        function calculateGPA() {
            const c1 = parseFloat(document.getElementById('cia1')?.value) || 0; // out of 20 -> scaled to 10
            const c2 = parseFloat(document.getElementById('cia2')?.value) || 0; // out of 50 -> scaled to 25
            const c3 = parseFloat(document.getElementById('cia3')?.value) || 0; // out of 20 -> scaled to 10
            const att = parseFloat(document.getElementById('cia-att')?.value) || 0; // out of 5 -> scaled to 5
            const esePaper = parseFloat(document.getElementById('ese-expected')?.value) || 0; // out of 100 -> scaled to 50
            const targetGoal = document.getElementById('target-goal-select')?.value || 'O';

            // Exact Samagra weightage conversions
            const cia1Scaled = (c1 / 20) * 10;
            const midSemScaled = (c2 / 50) * 25;
            const cia3Scaled = (c3 / 20) * 10;
            const attScaled = Math.min(att, 5);
            const totalCIA = Math.min(cia1Scaled + midSemScaled + cia3Scaled + attScaled, 50);

            const eseContribution = (esePaper / 100) * 50;
            const totalCourseMarks = Math.min(totalCIA + eseContribution, 100);

            // Grade assignment based on Samagra CHRIST scale
            let grade = "F";
            let gradePoint = 0.0;
            let resultClass = "Fail (Reappear required)";
            let resultBadgeClass = "chip-red";

            if (totalCourseMarks >= 80) {
                grade = "O";
                gradePoint = activeScaleMode === "4.0" ? 4.0 : 10.0;
                resultClass = "First Class with Distinction";
                resultBadgeClass = "chip-green";
            } else if (totalCourseMarks >= 70) {
                grade = "A+";
                gradePoint = activeScaleMode === "4.0" ? 3.6 : 9.0;
                resultClass = "First Class with Distinction";
                resultBadgeClass = "chip-green";
            } else if (totalCourseMarks >= 60) {
                grade = "A";
                gradePoint = activeScaleMode === "4.0" ? 3.2 : 8.0;
                resultClass = "First Class";
                resultBadgeClass = "chip-blue";
            } else if (totalCourseMarks >= 55) {
                grade = "B+";
                gradePoint = activeScaleMode === "4.0" ? 2.8 : 7.0;
                resultClass = "Second Class";
                resultBadgeClass = "chip-amber";
            } else if (totalCourseMarks >= 50) {
                grade = "B";
                gradePoint = activeScaleMode === "4.0" ? 2.4 : 6.0;
                resultClass = "Second Class";
                resultBadgeClass = "chip-amber";
            } else if (totalCourseMarks >= 45) {
                grade = "C";
                gradePoint = activeScaleMode === "4.0" ? 2.0 : 5.0;
                resultClass = "Pass Class";
                resultBadgeClass = "chip-blue";
            } else if (totalCourseMarks >= 40) {
                grade = "P";
                gradePoint = activeScaleMode === "4.0" ? 1.6 : 4.0;
                resultClass = "Pass Class";
                resultBadgeClass = "chip-blue";
            } else {
                grade = "F";
                gradePoint = 0.0;
                resultClass = "Fail / Reappear";
                resultBadgeClass = "chip-red";
            }

            // Target ESE Requirement Calculation (Samagra Formula)
            const TARGET_PCT = {
                O: 80,
                DISTINCTION: 75,
                'A+': 70,
                A: 60,
                'B+': 55,
                PASS: 40
            };
            const targetPct = TARGET_PCT[targetGoal] || 80;
            const requiredTotal = targetPct; // Course total max is 100
            const neededEseContribution = Math.max(0, requiredTotal - totalCIA);
            const neededEsePaperMarks = (neededEseContribution / 50) * 100;
            const effectiveNeededPaper = Math.max(40, Math.ceil(neededEsePaperMarks)); // 40% mandatory ESE rule

            const scoreDisp = document.getElementById('gpa-score-display');
            const gradeBadge = document.getElementById('grade-badge');
            const divisionBadge = document.getElementById('result-division-badge');
            const breakdown = document.getElementById('gpa-breakdown');

            if (scoreDisp) {
                scoreDisp.innerText = `${gradePoint.toFixed(2)} / ${activeScaleMode === '4.0' ? '4.0' : '10.0'}`;
                gradeBadge.innerText = `GRADE: ${grade} (${SAMAGRA_4_SCALE[grade]?.desc || ''})`;
                divisionBadge.innerText = resultClass;
                divisionBadge.className = `status-chip ${resultBadgeClass}`;
                
                breakdown.innerHTML = `
                    Total Scaled Course Marks: <strong>${totalCourseMarks.toFixed(1)} / 100</strong><br>
                    CIA Scaled: ${totalCIA.toFixed(1)} / 50 (CIA1: ${cia1Scaled.toFixed(1)}, Mid-Sem: ${midSemScaled.toFixed(1)}, CIA3: ${cia3Scaled.toFixed(1)}, Att: ${attScaled})<br>
                    ESE Contribution: ${eseContribution.toFixed(1)} / 50<br>
                    Required ESE Exam Score for ${targetGoal}: <strong>${Math.min(effectiveNeededPaper, 100)} / 100 Marks</strong> (40% min rule applies)
                `;
            }
        }

        function copyAcademicSummary() {
            const summary = `CHRIST (Deemed to be University) Academic Marks Summary\\n` +
                `Calculated Academic Performance: ${document.getElementById('gpa-score-display')?.innerText || ''}\\n` +
                `Status: ${document.getElementById('grade-badge')?.innerText || ''}\\n` +
                `Class: ${document.getElementById('result-division-badge')?.innerText || ''}\\n` +
                `Computed via Samagra Engine: https://unichrist-portal.vercel.app`;
            if (navigator.clipboard) {
                navigator.clipboard.writeText(summary).then(() => showToast('Academic Summary copied to clipboard!'));
            } else {
                showToast('Report copied!');
            }
        }
"""

# Replace existing calculateAttendance and calculateGPA with Samagra implementations
old_att_fn_start = text.find('function calculateAttendance() {')
old_login_fn_start = text.find('function handleLogin() {')

if old_att_fn_start != -1 and old_login_fn_start != -1:
    text = text[:old_att_fn_start] + samagra_js_code + "\n        " + text[old_login_fn_start:]

with open('unichrist-web/build_portal.py', 'w') as f:
    f.write(text)

print("Samagra calculation engines successfully integrated into build_portal.py!")
