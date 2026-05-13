const map = L.map("map").setView([5.4, -74.2], 6);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 18,
    attribution: "&copy; OpenStreetMap"
}).addTo(map);

const colors = {
    Baja: "#31d67b",
    Media: "#f6c945",
    Alta: "#ff5a73"
};

fetch("/api/mapa")
    .then((response) => response.json())
    .then((items) => {
        items.forEach((item) => {
            const marker = L.circleMarker([item.lat, item.lng], {
                radius: 11,
                color: colors[item.nivel_saturacion],
                fillColor: colors[item.nivel_saturacion],
                fillOpacity: 0.78,
                weight: 2
            }).addTo(map);

            marker.bindPopup(`
                <strong>${item.pueblo}</strong><br>
                Saturacion: <b>${item.nivel_saturacion}</b><br>
                Turistas esperados: ${Number(item.turistas_estimados).toLocaleString("es-CO")}<br>
                Ocupacion: ${item.ocupacion}%<br>
                <small>${item.recomendacion}</small>
            `);
        });
    });
