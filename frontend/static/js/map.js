const API_BASE = "";

let map = L.map("map").setView([0, 0], 2);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "",
}).addTo(map);

let currentMarker = null;

function track() {
  const tracknum = document.getElementById("tracknum").value;
  fetch(`${API_BASE}/track/${tracknum}`)
    .then((res) => {
      if (!res.ok) throw new Error("Not found");
      return res.json();
    })
    .then((data) => {
      if (currentMarker) {
        map.removeLayer(currentMarker);
      }

      map.setView([data.latitude, data.longitude], 13);

      currentMarker = L.marker([data.latitude, data.longitude])
        .addTo(map)
        .bindPopup("Местоположение вашего автомобиля")
        .openPopup();
    })
    .catch((err) => alert("Трек-номер не найден!"));
}
