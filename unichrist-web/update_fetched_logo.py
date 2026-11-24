with open('unichrist-web/build_portal.py', 'r') as f:
    text = f.read()

# Replace christ_crest_clean.png with the official downloaded logo: christ_official_logo.png
text = text.replace('/images/christ_crest_clean.png', '/images/christ_official_logo.png')

with open('unichrist-web/build_portal.py', 'w') as f:
    f.write(text)

print("Updated build_portal.py with official downloaded logo!")
