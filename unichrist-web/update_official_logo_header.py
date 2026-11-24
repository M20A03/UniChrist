with open('unichrist-web/build_portal.py', 'r') as f:
    text = f.read()

# Replace the brand-seal-lockup:
# Use the official Christ circular crest image directly, with high quality rendering.
# In the subtitle, display full text on desktop and a short clean "Bangalore Yeshwanthpur Campus (BYC)" on mobile (dropping "(Deemed to be University)" on phone so it doesn't take up space).

old_brand_lockup = '''            <div class="brand-seal-lockup" onclick="navigateTo('page-home')">
                <!-- Official Christ University Crest & Emblem -->
                <img src="/images/christ_logo.png" alt="CHRIST (Deemed to be University)" class="official-christ-logo-img" onerror="this.style.display='none'; document.getElementById('fallback-crest').style.display='block';" />
                <svg id="fallback-crest" style="display:none;" class="crest-svg-icon" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="50" cy="50" r="48" fill="#002147" stroke="#C5A059" stroke-width="4"/>
                    <circle cx="50" cy="50" r="42" fill="none" stroke="#C5A059" stroke-width="1.5" stroke-dasharray="3 2"/>
                    <path d="M50 18L58 34H42L50 18Z" fill="#C5A059"/>
                    <rect x="36" y="38" width="28" height="24" rx="2" fill="#FFFFFF" stroke="#C5A059" stroke-width="2"/>
                    <path d="M40 44H60M40 50H60M40 56H52" stroke="#002147" stroke-width="2" stroke-linecap="round"/>
                    <path d="M30 68C40 76 60 76 70 68" stroke="#C5A059" stroke-width="3" stroke-linecap="round"/>
                    <text x="50" y="86" text-anchor="middle" fill="#C5A059" font-family="'Cinzel', serif" font-size="8" font-weight="bold" letter-spacing="1">ESTD. 1969</text>
                </svg>

                <div class="university-names">
                    <span class="motto-banner">Excellence and Service • Estd. 1969</span>
                    <h1 class="christ-title">CHRIST</h1>
                    <span class="portal-subtitle" id="active-campus-label">(Deemed to be University) • Bangalore Yeshwanthpur Campus</span>
                </div>
            </div>'''

new_brand_lockup = '''            <div class="brand-seal-lockup" onclick="navigateTo('page-home')">
                <!-- Official Christ University Crest Emblem -->
                <img src="/images/christ_crest_clean.png" alt="CHRIST (Deemed to be University)" class="official-christ-crest-img" />

                <div class="university-names">
                    <span class="motto-banner">Excellence and Service • Estd. 1969</span>
                    <h1 class="christ-title">CHRIST</h1>
                    <span class="portal-subtitle desktop-only-sub" id="active-campus-label">(Deemed to be University) • Bangalore Yeshwanthpur Campus</span>
                    <span class="portal-subtitle mobile-only-sub">Bangalore Yeshwanthpur Campus (BYC)</span>
                </div>
            </div>'''

text = text.replace(old_brand_lockup, new_brand_lockup)

with open('unichrist-web/build_portal.py', 'w') as f:
    f.write(text)

print("Updated header with official christ_crest_clean.png and responsive subtitle!")
