const API_BASE = "http://hqnl0365908.online-vm.com:8000"; // Тобі потрібно буде встановити правильну URL

// 1. Додавання нової точки
const addForm = document.getElementById("add-point-form");
addForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    
    const tracknum = document.getElementById("tracknum").value;
    const latitude = parseFloat(document.getElementById("latitude").value);
    const longitude = parseFloat(document.getElementById("longitude").value);

    console.log(JSON.stringify({
        tracking_number: tracknum,
        latitude,
        longitude
    }))
    
    try {
        const res = await fetch("http://hqnl0365908.online-vm.com:8000/admin/set-location", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                tracking_number: tracknum,
                latitude,
                longitude
            })
        });

        if (!res.ok) throw new Error("Failed to add location");

        alert("Location added successfully");
        loadLocations(); // Оновити список точок
    } catch (error) {
        console.error(error);
        alert("Error adding location");
    }
});

// 2. Завантажити всі точки
async function loadLocations() {
    try {
        const res = await fetch(`${API_BASE}/admin/locations`, {
            method: "GET",
            headers: {
                "Authorization": "Bearer supersecret"
            }
        });
        
        const locations = await res.json();
        const tableBody = document.getElementById("locations-table").getElementsByTagName("tbody")[0];
        tableBody.innerHTML = ''; // Очищаємо таблицю перед додаванням нових записів

        locations.forEach(location => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${location.tracking_number}</td>
                <td>${location.latitude}</td>
                <td>${location.longitude}</td>
                <td>
                    <button onclick="editLocation('${location.tracking_number}')">Edit</button>
                    <button onclick="deleteLocation('${location.tracking_number}')">Delete</button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error("Error loading locations", error);
    }
}

// 3. Редагувати точку
async function editLocation(tracknum) {
    const newLat = parseFloat(prompt("Enter new latitude:"));
    const newLng = parseFloat(prompt("Enter new longitude:"));

    try {
        const res = await fetch(`${API_BASE}/admin/edit-location`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                tracking_number: tracknum,
                latitude: newLat,
                longitude: newLng
            })
        });

        if (!res.ok) throw new Error("Failed to edit location");

        alert("Location updated");
        loadLocations();  // Перезавантажуємо локації
    } catch (error) {
        console.error("Error editing location", error);
    }
}


// 4. Видалити точку
async function deleteLocation(tracknum) {
    if (confirm("Are you sure you want to delete this location?")) {
        try {
            const res = await fetch(`${API_BASE}/admin/delete-location?tracking_number=${tracknum}`, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                },
            });

            if (!res.ok) throw new Error("Failed to delete location");

            alert("Location deleted");
            loadLocations();  // Перезавантажуємо локації
        } catch (error) {
            console.error("Error deleting location", error);
        }
    }
}


// Завантажити локації при завантаженні сторінки
window.onload = loadLocations;
