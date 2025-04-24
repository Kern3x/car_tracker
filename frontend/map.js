let map = L.map('map').setView([0, 0], 2);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '' }).addTo(map);

function track() {
    const tracknum = document.getElementById("tracknum").value;
    fetch(`http://hqnl0365908.online-vm.com:8000/track/${tracknum}`)
        .then(res => {
            if (!res.ok) throw new Error("Not found");
            return res.json();
        })
        .then(data => {
            map.setView([data.latitude, data.longitude], 13);
            L.marker([data.latitude, data.longitude]).addTo(map)
                .bindPopup("Car Location").openPopup();
        })
        .catch(err => alert("Tracking number not found"));
}
