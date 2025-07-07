const API_BASE = "/admin";
const addForm = document.getElementById("add-point-form");

addForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const tracknum = document.getElementById("tracknum").value;
  const latitude = parseFloat(document.getElementById("latitude").value);
  const longitude = parseFloat(document.getElementById("longitude").value);
  const timestamp = document.getElementById("timestamp").value;

  try {
    const res = await fetch(`${API_BASE}/set-location`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        tracking_number: tracknum,
        latitude,
        longitude,
        timestamp,
      }),
    });

    if (!res.ok) throw new Error("Failed to add location");

    loadLocations();

    addForm.reset();
  } catch (error) {
    console.error(error);
    alert("Возникла ошибка при добавлении точки!");
  }
});

async function loadLocations() {
  try {
    const res = await fetch(`${API_BASE}/locations`);
    const locations = await res.json();

    const tableBody = document
      .getElementById("locations-table")
      .getElementsByTagName("tbody")[0];
    tableBody.innerHTML = "";

    locations.forEach((location) => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${location.tracking_number}</td>
        <td>${location.latitude}</td>
        <td>${location.longitude}</td>
        <td>${new Date(location.timestamp).toLocaleString()}</td>
        <td>
          <button onclick="editLocation('${location.tracking_number}')">Редактировать</button>
          <button onclick="deleteLocation('${location.tracking_number}')">Удалить</button>
        </td>
      `;
      tableBody.appendChild(row);
    });
  } catch (error) {
    console.error("Error loading locations", error);
  }
}

async function editLocation(tracknum) {
  const newLat = parseFloat(prompt("Введите новую широту:"));
  const newLng = parseFloat(prompt("Введите новую долготу:"));
  const newTime = prompt("Введите новую дату и время (ISO формат):");

  try {
    const res = await fetch(`${API_BASE}/edit-location`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        tracking_number: tracknum,
        latitude: newLat,
        longitude: newLng,
        timestamp: newTime,
      }),
    });

    if (!res.ok) throw new Error("Failed to edit location");

    loadLocations();
  } catch (error) {
    console.error("Error editing location", error);
    alert("Возникла ошибка при редактировании точки!");
  }
}

async function deleteLocation(tracknum) {
  if (confirm("Вы уверены, что хотите удалить эту точку?")) {
    try {
      const res = await fetch(
        `${API_BASE}/delete-location?tracking_number=${tracknum}`,
        {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (!res.ok) throw new Error("Failed to delete location");

      loadLocations();
    } catch (error) {
      console.error("Error deleting location", error);
      alert("Возникла ошибка при удалении точки!");
    }
  }
}

window.onload = loadLocations;
