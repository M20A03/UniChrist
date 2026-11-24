with open('unichrist-web/build_portal.py', 'r') as f:
    text = f.read()

# 1. Update the Search Box & Category Headers in Sidebar:
# Add a top global view toggle (List / Grid) plus small grid toggle icon on each sub-heading
old_sidebar_header = '''        <aside class="sidebar-card">
            <div class="sidebar-search-box">
                <i class="fa-solid fa-magnifying-glass sidebar-search-icon"></i>
                <input type="text" id="dir-filter-input" class="sidebar-search-input" placeholder="Search 38 portals..." onkeyup="filterDirectory()" />
            </div>

            <!-- Category A: Academics & Classroom Tools -->
            <div class="sidebar-category-title"><i class="fa-solid fa-graduation-cap"></i> Academics &amp; Tools</div>
            <ul class="directory-list">'''

new_sidebar_header = '''        <aside class="sidebar-card">
            <div class="sidebar-search-box" style="display:flex; gap:6px; align-items:center;">
                <div style="position:relative; flex:1;">
                    <i class="fa-solid fa-magnifying-glass sidebar-search-icon"></i>
                    <input type="text" id="dir-filter-input" class="sidebar-search-input" placeholder="Search 38 portals..." onkeyup="filterDirectory()" />
                </div>
                <!-- Global View Mode Switcher Button -->
                <button id="global-sidebar-toggle" class="sidebar-view-btn" onclick="toggleAllSidebarViews()" title="Toggle Grid / List View for all categories">
                    <i class="fa-solid fa-table-cells-large"></i>
                </button>
            </div>

            <!-- Category A: Academics & Classroom Tools -->
            <div class="sidebar-category-title">
                <span><i class="fa-solid fa-graduation-cap"></i> Academics &amp; Tools</span>
                <button class="cat-grid-toggle-btn" onclick="toggleCategoryGrid('cat-list-academics', this)" title="Toggle Grid View">
                    <i class="fa-solid fa-grip"></i>
                </button>
            </div>
            <ul class="directory-list" id="cat-list-academics">'''

text = text.replace(old_sidebar_header, new_sidebar_header)

# Replace Category B header
old_cat_b = '''            <!-- Category B: Campus Logistics & BYC Essentials -->
            <div class="sidebar-category-title"><i class="fa-solid fa-map-pin"></i> BYC Campus &amp; Logistics</div>
            <ul class="directory-list">'''

new_cat_b = '''            <!-- Category B: Campus Logistics & BYC Essentials -->
            <div class="sidebar-category-title">
                <span><i class="fa-solid fa-map-pin"></i> BYC Campus &amp; Logistics</span>
                <button class="cat-grid-toggle-btn" onclick="toggleCategoryGrid('cat-list-logistics', this)" title="Toggle Grid View">
                    <i class="fa-solid fa-grip"></i>
                </button>
            </div>
            <ul class="directory-list" id="cat-list-logistics">'''

text = text.replace(old_cat_b, new_cat_b)

# Replace Category C header
old_cat_c = '''            <!-- Category C: Research, Clubs & Professional -->
            <div class="sidebar-category-title"><i class="fa-solid fa-briefcase"></i> Research, Careers &amp; Events</div>
            <ul class="directory-list">'''

new_cat_c = '''            <!-- Category C: Research, Clubs & Professional -->
            <div class="sidebar-category-title">
                <span><i class="fa-solid fa-briefcase"></i> Research, Careers &amp; Events</span>
                <button class="cat-grid-toggle-btn" onclick="toggleCategoryGrid('cat-list-research', this)" title="Toggle Grid View">
                    <i class="fa-solid fa-grip"></i>
                </button>
            </div>
            <ul class="directory-list" id="cat-list-research">'''

text = text.replace(old_cat_c, new_cat_c)

# Replace Category D header
old_cat_d = '''            <!-- Category D: Wellness, Admin & Support -->
            <div class="sidebar-category-title"><i class="fa-solid fa-hand-holding-heart"></i> Wellness, Admin &amp; Support</div>
            <ul class="directory-list">'''

new_cat_d = '''            <!-- Category D: Wellness, Admin & Support -->
            <div class="sidebar-category-title">
                <span><i class="fa-solid fa-hand-holding-heart"></i> Wellness, Admin &amp; Support</span>
                <button class="cat-grid-toggle-btn" onclick="toggleCategoryGrid('cat-list-wellness', this)" title="Toggle Grid View">
                    <i class="fa-solid fa-grip"></i>
                </button>
            </div>
            <ul class="directory-list" id="cat-list-wellness">'''

text = text.replace(old_cat_d, new_cat_d)

# 2. Add JavaScript Functions to toggle category grid views:
sidebar_js = """
        // Sidebar Grid / List View Toggle Logic
        let isGlobalGrid = false;
        function toggleCategoryGrid(listId, btn) {
            const list = document.getElementById(listId);
            if (!list) return;
            const isGrid = list.classList.toggle('grid-mode');
            if (btn) {
                btn.classList.toggle('active', isGrid);
                btn.innerHTML = isGrid ? '<i class="fa-solid fa-list"></i>' : '<i class="fa-solid fa-grip"></i>';
                btn.title = isGrid ? 'Switch to List View' : 'Switch to Grid View';
            }
        }

        function toggleAllSidebarViews() {
            isGlobalGrid = !isGlobalGrid;
            const catLists = ['cat-list-academics', 'cat-list-logistics', 'cat-list-research', 'cat-list-wellness'];
            const toggleBtns = document.querySelectorAll('.cat-grid-toggle-btn');
            
            catLists.forEach(id => {
                const el = document.getElementById(id);
                if (el) el.classList.toggle('grid-mode', isGlobalGrid);
            });

            toggleBtns.forEach(b => {
                b.classList.toggle('active', isGlobalGrid);
                b.innerHTML = isGlobalGrid ? '<i class="fa-solid fa-list"></i>' : '<i class="fa-solid fa-grip"></i>';
            });

            const globalBtn = document.getElementById('global-sidebar-toggle');
            if (globalBtn) {
                globalBtn.classList.toggle('active', isGlobalGrid);
                globalBtn.innerHTML = isGlobalGrid ? '<i class="fa-solid fa-list"></i>' : '<i class="fa-solid fa-table-cells-large"></i>';
            }
            showToast(isGlobalGrid ? "Sidebar switched to Compact Grid View" : "Sidebar switched to List View");
        }
"""

if "function filterDirectory()" in text:
    text = text.replace("function filterDirectory()", sidebar_js + "\n        function filterDirectory()")

with open('unichrist-web/build_portal.py', 'w') as f:
    f.write(text)

print("Added sidebar grid view buttons and script successfully!")
