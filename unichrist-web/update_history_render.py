with open('unichrist-web/build_portal.py', 'r') as f:
    text = f.read()

target = '<div class="tile-sub"><i class="fa-regular fa-calendar"></i> Absence Period: ${c.dates} • Hours: ${c.hours} Hrs Claimed</div>'
replacement = '''<div class="tile-sub"><i class="fa-regular fa-calendar"></i> Absence Period: ${c.dates} • Hours: ${c.hours} Hrs Claimed</div>
                    <div style="font-size:10.5px; color:var(--christ-navy); background:#F8FAFC; border:1px solid var(--border-light); padding:4px 8px; border-radius:3px; margin:6px 0; display:flex; gap:10px; flex-wrap:wrap;">
                        <span><i class="fa-solid fa-location-dot" style="color:var(--state-danger);"></i> Geotag: <strong>Verified</strong></span>
                        <span><i class="fa-solid fa-certificate" style="color:var(--christ-gold-dark);"></i> Cert: <strong>Attached</strong></span>
                        <span><i class="fa-solid fa-file-signature" style="color:var(--christ-blue);"></i> Teacher Letter: <strong>Endorsed</strong></span>
                    </div>'''

if target in text:
    text = text.replace(target, replacement)

with open('unichrist-web/build_portal.py', 'w') as f:
    f.write(text)

print("Updated renderYellowFormHistory successfully!")
