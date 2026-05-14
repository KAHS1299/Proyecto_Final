const map = L.map("map", { scrollWheelZoom: false }).setView([5.7, -74.5], 6);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap"
}).addTo(map);

const colors = { Low: "#32c977", Medium: "#f2bd3d", High: "#ef4f5f" };

function renderDestination(item) {
    document.getElementById("placeName").textContent = item.town;
    document.getElementById("placeLevel").textContent = item.saturation_level;
    document.getElementById("placeLevel").className = `level-${item.saturation_level.toLowerCase()}`;
    document.getElementById("placeVisitors").textContent = Number(item.historical_tourists).toLocaleString("en-US");
    document.getElementById("placeOccupancy").textContent = `${item.occupancy}%`;
    document.getElementById("placeRecommendation").textContent = item.recommendation;
}

fetch("/api/map")
    .then((response) => response.json())
    .then((items) => {
        items.forEach((item, index) => {
            // USES item.lon FROM CSV
            const marker = L.circleMarker([item.lat, item.lon], {
                radius: 12,
                color: colors[item.saturation_level] || "#ccc",
                fillColor: colors[item.saturation_level] || "#ccc",
                fillOpacity: 0.8,
                weight: 2
            }).addTo(map);

            marker.bindPopup(`<b>${item.town}</b><br>Saturation: ${item.saturation_level}`);

            marker.on("click", () => renderDestination(item));

            if (index === 0) renderDestination(item);
        });
    });