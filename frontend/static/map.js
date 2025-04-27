let map = L.map('map').setView([0, 0], 2);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '' }).addTo(map);

// Змінна для зберігання маркеру
let currentMarker = null;

function track() {
    const tracknum = document.getElementById("tracknum").value;
    fetch(`http://localhost:8000/track/${tracknum}`)
        .then(res => {
            if (!res.ok) throw new Error("Not found");
            return res.json();
        })
        .then(data => {
            // Якщо є попередній маркер, видаляємо його
            if (currentMarker) {
                map.removeLayer(currentMarker);
            }

            // Оновлюємо картку на нові координати
            map.setView([data.latitude, data.longitude], 13);

            // Додаємо новий маркер
            currentMarker = L.marker([data.latitude, data.longitude]).addTo(map)
                .bindPopup("Car Location").openPopup();
        })
        .catch(err => alert("Tracking number not found"));
}
