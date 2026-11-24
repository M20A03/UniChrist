import re

with open('unichrist-web/build_portal.py', 'r') as f:
    text = f.read()

# Let's inspect where sections begin and end
sections = re.findall(r'<section id=\"(page-[a-zA-Z0-9_-]+)\"[^>]*>', text)
print(f"Total sections currently: {len(sections)}")
print(sections)
