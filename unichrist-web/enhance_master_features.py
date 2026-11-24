with open('unichrist-web/build_portal.py', 'r') as f:
    text = f.read()

# 1. Add "Why Christ?" Stats Strip on Homepage
stats_strip_html = """
                <!-- "Why Christ?" Animated Institutional Stats Strip -->
                <div style="background:var(--christ-navy); border-radius:var(--radius-sm); padding:16px 20px; color:#FFFFFF; margin-bottom:18px; border-bottom:3px solid var(--christ-gold);">
                    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(160px, 1fr)); gap:16px; text-align:center;">
                        <div>
                            <div style="font-size:22px; font-weight:800; color:var(--christ-gold);">Estd. 1969</div>
                            <div style="font-size:11px; color:#CBD5E1;">57+ Years of Heritage</div>
                        </div>
                        <div>
                            <div style="font-size:22px; font-weight:800; color:var(--christ-gold);">NAAC A+</div>
                            <div style="font-size:11px; color:#CBD5E1;">Highest National Grade</div>
                        </div>
                        <div>
                            <div style="font-size:22px; font-weight:800; color:var(--christ-gold);">30,000+</div>
                            <div style="font-size:11px; color:#CBD5E1;">Students Enrolled</div>
                        </div>
                        <div>
                            <div style="font-size:22px; font-weight:800; color:var(--christ-gold);">6 Campuses</div>
                            <div style="font-size:11px; color:#CBD5E1;">Multi-State Presence</div>
                        </div>
                        <div>
                            <div style="font-size:22px; font-weight:800; color:var(--christ-gold);">95%+</div>
                            <div style="font-size:11px; color:#CBD5E1;">Placement Record</div>
                        </div>
                    </div>
                </div>
"""

# Place stats strip right after the 3-second KPI scan row on homepage
target_kpi_end = '<!-- 3. Campus Billboard Announcement -->'
if target_kpi_end in text:
    text = text.replace(target_kpi_end, stats_strip_html + "\n                " + target_kpi_end)

# 2. Add Accessibility and Language Toggle JS functions
js_additions = """
        // Accessibility Functions: Font Resizer & High-Contrast Mode
        let currentFontSize = 13;
        function adjustFontSize(delta) {
            if (delta === 0) currentFontSize = 13;
            else currentFontSize = Math.min(Math.max(currentFontSize + delta, 11), 17);
            document.documentElement.style.fontSize = currentFontSize + "px";
            showToast("Font size adjusted to " + currentFontSize + "px");
        }

        let isHighContrast = false;
        function toggleContrast() {
            isHighContrast = !isHighContrast;
            document.body.classList.toggle('high-contrast-mode', isHighContrast);
            showToast(isHighContrast ? "High Contrast Mode Active" : "Standard Palette Restored");
        }

        let currentLang = "en";
        function toggleLanguage() {
            currentLang = currentLang === "en" ? "hi" : "en";
            document.getElementById('lang-label').innerText = currentLang === "en" ? "हिंदी" : "English";
            showToast(currentLang === "en" ? "Switched to English Interface" : "इंटरफ़ेस हिंदी में स्विच किया गया");
        }
"""

if "function navigateTo(" in text:
    text = text.replace("function navigateTo(", js_additions + "\n        function navigateTo(")

with open('unichrist-web/build_portal.py', 'w') as f:
    f.write(text)

print("Stats strip and accessibility scripts integrated successfully!")
