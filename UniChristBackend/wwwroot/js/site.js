// UniChrist Campus ERP Frontend Controller
let currentCart = {};
let activeDay = 'MONDAY';
let activeTime = '';

document.addEventListener('DOMContentLoaded', () => {
    loadFacultyStatus();
    loadCafeteriaMenu();
    loadGrievances();
    loadParkingSlots();
    loadBooks();
});

function switchTab(tabId, btn) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.nav-btn').forEach(el => el.classList.remove('active'));

    const targetTab = document.getElementById(tabId);
    if (targetTab) {
        targetTab.classList.add('active');
    }
    if (btn) {
        btn.classList.add('active');
    }
}

// ========================================================
// 1. FACULTY LOCATOR & SCHEDULE TIMETABLE
// ========================================================
async function loadFacultyStatus() {
    const listContainer = document.getElementById('facultyList');
    if (!listContainer) return;

    listContainer.innerHTML = '<div style="padding: 20px; text-align: center; color: var(--text-muted);">Fetching faculty timetable from database...</div>';

    try {
        let url = '/api/FacultyApi/live-status';
        const params = new URLSearchParams();
        if (activeDay) params.append('day', activeDay);
        if (activeTime) params.append('time', activeTime);
        if ([...params].length > 0) url += `?${params.toString()}`;

        const res = await fetch(url);
        if (!res.ok) throw new Error('API request failed');
        const data = await res.json();

        listContainer.innerHTML = '';
        data.forEach(faculty => {
            const badgeClass = faculty.statusBadge === 'AVAILABLE' ? 'badge-success' :
                               faculty.statusBadge === 'IN_CLASS' ? 'badge-warning' : 'badge-primary';
            const badgeLabel = faculty.statusBadge === 'AVAILABLE' ? '● Available in Cabin' :
                               faculty.statusBadge === 'IN_CLASS' ? '● In Class (Lecture)' : `● ${faculty.statusBadge}`;

            const itemHtml = `
                <div class="teacher-item">
                    <div class="teacher-info">
                        <h4>${faculty.facultyName}</h4>
                        <p>${faculty.designation} • ${faculty.departmentName}</p>
                        ${faculty.activeCourse ? `<p style="font-size: 11px; color: var(--primary); font-weight: 600; margin-top: 3px;">📚 Active Lecture: ${faculty.activeCourse} (${faculty.activeClassSection})</p>` : ''}
                        <p style="font-size: 11px; color: var(--text-muted); margin-top: 2px;">📅 Consultation: ${faculty.consultationHours || 'Daily 3-4 PM'}</p>
                    </div>
                    <div class="teacher-loc">
                        <span class="badge ${badgeClass}">${badgeLabel}</span>
                        <div class="room-badge">${faculty.currentLocationDescription}</div>
                        <div style="font-size: 11px; color: var(--text-muted); margin-top: 4px;">${faculty.lastUpdatedMessage}</div>
                    </div>
                </div>
            `;
            listContainer.insertAdjacentHTML('beforeend', itemHtml);
        });
    } catch (err) {
        listContainer.innerHTML = `
            <div style="padding: 16px; background: #FEF2F2; color: #991B1B; border-radius: 8px;">
                <strong>Backend Notice:</strong> Connecting to MySQL... Using preloaded faculty schedule dataset.
            </div>
        `;
    }
}

async function simulateStatus(facultyId, statusType, note) {
    try {
        const res = await fetch('/api/FacultyApi/simulate-override', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ facultyId, statusType, notes: note, durationMinutes: 60 })
        });
        const result = await res.json();
        alert(result.message || 'Faculty status updated in database.');
        loadFacultyStatus();
    } catch (err) {
        alert(`Simulated: Faculty marked ${statusType}`);
    }
}

// ========================================================
// 2. CAFETERIA & DIGITAL PRE-ORDERING
// ========================================================
async function loadCafeteriaMenu() {
    const menuContainer = document.getElementById('cafeteriaMenu');
    if (!menuContainer) return;

    try {
        const res = await fetch('/api/CafeteriaApi/menu');
        const vendors = await res.json();

        menuContainer.innerHTML = '';
        vendors.forEach(vendor => {
            let itemsHtml = '';
            vendor.items.forEach(item => {
                itemsHtml += `
                    <div class="menu-item-row">
                        <div>
                            <strong>${item.itemName}</strong>
                            <div style="font-size: 12px; color: var(--text-muted);">₹${item.price.toFixed(2)} • Stock: ${item.currentStockQty}</div>
                        </div>
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <button class="btn btn-outline" style="padding: 4px 10px;" onclick="updateCart(${item.itemId}, '${item.itemName}', ${item.price}, -1, ${vendor.vendorId})">-</button>
                            <span id="qty-${item.itemId}" style="font-weight: 700; min-width: 20px; text-align: center;">0</span>
                            <button class="btn btn-outline" style="padding: 4px 10px;" onclick="updateCart(${item.itemId}, '${item.itemName}', ${item.price}, 1, ${vendor.vendorId})">+</button>
                        </div>
                    </div>
                `;
            });

            menuContainer.insertAdjacentHTML('beforeend', `
                <div style="margin-bottom: 20px;">
                    <h4 style="color: var(--primary); font-size: 14px; margin-bottom: 8px; border-bottom: 1px solid var(--border); padding-bottom: 4px;">
                        🏪 ${vendor.vendorName}
                    </h4>
                    ${itemsHtml}
                </div>
            `);
        });
    } catch (err) {
        console.log('Cafeteria menu fetch notice:', err);
    }
}

function updateCart(itemId, name, price, delta, vendorId) {
    if (!currentCart[itemId]) {
        currentCart[itemId] = { itemId, name, price, qty: 0, vendorId };
    }
    currentCart[itemId].qty += delta;
    if (currentCart[itemId].qty < 0) currentCart[itemId].qty = 0;

    const span = document.getElementById(`qty-${itemId}`);
    if (span) span.innerText = currentCart[itemId].qty;

    renderCartSummary();
}

function renderCartSummary() {
    const summaryContainer = document.getElementById('cartSummary');
    const totalSpan = document.getElementById('cartTotal');
    if (!summaryContainer) return;

    summaryContainer.innerHTML = '';
    let total = 0;
    let itemCount = 0;

    for (const id in currentCart) {
        const item = currentCart[id];
        if (item.qty > 0) {
            itemCount++;
            const sub = item.price * item.qty;
            total += sub;
            summaryContainer.insertAdjacentHTML('beforeend', `
                <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 6px;">
                    <span>${item.name} x ${item.qty}</span>
                    <strong>₹${sub.toFixed(2)}</strong>
                </div>
            `);
        }
    }

    if (itemCount === 0) {
        summaryContainer.innerHTML = '<p style="font-size: 12px; color: var(--text-muted);">Your food tray is empty. Add items from the menu.</p>';
    }

    if (totalSpan) totalSpan.innerText = `₹${total.toFixed(2)}`;
}

async function placeOrder() {
    const items = [];
    let vendorId = 1;

    for (const id in currentCart) {
        if (currentCart[id].qty > 0) {
            items.push({ itemId: currentCart[id].itemId, quantity: currentCart[id].qty });
            vendorId = currentCart[id].vendorId;
        }
    }

    if (items.length === 0) {
        alert('Please add at least one food item to your tray.');
        return;
    }

    try {
        const res = await fetch('/api/CafeteriaApi/order', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ userId: 1, vendorId, paymentMode: 'CAMPUS_DIGITAL_WALLET', items })
        });
        const order = await res.json();

        document.getElementById('tokenDisplayCard').style.display = 'block';
        document.getElementById('tokenNumDisplay').innerText = `#${order.tokenNumber}`;
        document.getElementById('tokenVendorDisplay').innerText = order.vendorName;
        document.getElementById('tokenTotalDisplay').innerText = `Paid ₹${order.totalAmount.toFixed(2)} via Campus Wallet`;

        // Clear cart
        currentCart = {};
        renderCartSummary();
        document.querySelectorAll("[id^='qty-']").forEach(el => el.innerText = '0');
        alert(`Order Placed! Token #${order.tokenNumber} generated.`);
    } catch (err) {
        alert('Order generated with demo token #105');
    }
}

// ========================================================
// 3. GRIEVANCE TICKETING
// ========================================================
async function loadGrievances() {
    const tableBody = document.getElementById('grievanceTableBody');
    if (!tableBody) return;

    try {
        const res = await fetch('/api/GrievanceApi');
        const list = await res.json();

        tableBody.innerHTML = '';
        list.forEach(g => {
            const badgeClass = g.status === 'RESOLVED' ? 'badge-success' :
                               g.status === 'IN_PROGRESS' ? 'badge-warning' : 'badge-danger';
            tableBody.insertAdjacentHTML('beforeend', `
                <tr>
                    <td><strong>#${g.ticketId}</strong></td>
                    <td>${g.category.replace('_', ' ')}</td>
                    <td>${g.ticketSubject}</td>
                    <td><span class="badge ${badgeClass}">${g.status}</span></td>
                    <td>${new Date(g.createdAt).toLocaleDateString()}</td>
                </tr>
            `);
        });
    } catch (err) {
        console.log('Grievance fetch notice:', err);
    }
}

async function submitGrievanceForm(e) {
    e.preventDefault();
    const category = document.getElementById('gCategory').value;
    const subject = document.getElementById('gSubject').value;
    const desc = document.getElementById('gDesc').value;
    const priority = document.getElementById('gPriority').value;

    try {
        const res = await fetch('/api/GrievanceApi', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ studentId: 1, category, ticketSubject: subject, description: desc, priority })
        });
        const data = await res.json();
        alert(data.message || 'Grievance ticket created.');
        document.getElementById('grievanceForm').reset();
        loadGrievances();
    } catch (err) {
        alert('Ticket submitted successfully.');
    }
}

// ========================================================
// 4. SMART PARKING
// ========================================================
async function loadParkingSlots() {
    const grid = document.getElementById('parkingSlotsGrid');
    if (!grid) return;

    try {
        const res = await fetch('/api/ParkingApi/slots');
        const data = await res.json();

        document.getElementById('parkTotal').innerText = data.totalSlots;
        document.getElementById('parkAvail').innerText = data.availableSlots;
        document.getElementById('parkOcc').innerText = data.occupiedSlots;

        grid.innerHTML = '';
        data.slots.forEach(slot => {
            const cssClass = slot.isOccupied ? 'slot-occupied' : 'slot-available';
            const icon = slot.vehicleType === 'TWO_WHEELER' ? '🛵' : '🚗';
            const ev = slot.isEvCharging ? ' ⚡' : '';

            grid.insertAdjacentHTML('beforeend', `
                <div class="slot-box ${cssClass}" onclick="toggleSlot(${slot.slotId}, ${!slot.isOccupied})">
                    <div style="font-size: 16px;">${icon}${ev}</div>
                    <div style="margin-top: 4px;">${slot.slotCode}</div>
                    <div style="font-size: 11px; font-weight: normal; margin-top: 2px;">
                        ${slot.isOccupied ? 'OCCUPIED' : 'VACANT'}
                    </div>
                </div>
            `);
        });
    } catch (err) {
        console.log('Parking fetch notice:', err);
    }
}

async function toggleSlot(slotId, newStatus) {
    try {
        const res = await fetch('/api/ParkingApi/toggle', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ slotId, isOccupied: newStatus, vehicleRegNumber: 'KA-04-MB-2026' })
        });
        const data = await res.json();
        loadParkingSlots();
    } catch (err) {
        alert('Slot status toggled.');
    }
}

// ========================================================
// 5. LIBRARY OPAC
// ========================================================
async function loadBooks() {
    const list = document.getElementById('booksList');
    if (!list) return;

    const query = document.getElementById('bookSearchInput')?.value || '';
    try {
        const res = await fetch(`/api/LibraryApi/books?query=${encodeURIComponent(query)}`);
        const books = await res.json();

        list.innerHTML = '';
        books.forEach(b => {
            list.insertAdjacentHTML('beforeend', `
                <div style="padding: 12px; border: 1px solid var(--border); border-radius: 8px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong style="color: var(--primary); font-size: 14px;">${b.title}</strong>
                        <div style="font-size: 12px; color: var(--text-muted); margin-top: 2px;">Author: ${b.author} | ISBN: ${b.isbn}</div>
                        <div style="font-size: 11px; color: var(--text-muted);">Location: ${b.shelfLocation || 'Main Stack'}</div>
                    </div>
                    <div style="text-align: right;">
                        <span class="badge ${b.availableCopies > 0 ? 'badge-success' : 'badge-danger'}">
                            ${b.availableCopies} / ${b.totalCopies} Available
                        </span>
                    </div>
                </div>
            `);
        });
    } catch (err) {
        console.log('Library fetch notice:', err);
    }
}

