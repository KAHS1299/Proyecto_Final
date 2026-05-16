const map = L.map("map", { scrollWheelZoom: false }).setView([5.8, -74.6], 6);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap"
}).addTo(map);

const colors = { Low: "#32c977", Medium: "#f2bd3d", High: "#ef4f5f" };

function renderDestination(item) {
    document.getElementById("placeName").textContent = item.town;
    document.getElementById("placeDescription").textContent = item.description;
    document.getElementById("placeDetail").textContent = `Main attractions: ${item.attractions.join(", ")}.`;
    document.getElementById("placeLevel").textContent = item.saturation_level;
    document.getElementById("placeLevel").className = `level-${item.saturation_level.toLowerCase()}`;
    document.getElementById("placeVisitors").textContent = Number(item.historical_tourists).toLocaleString("en-US");
    document.getElementById("placeOccupancy").textContent = `${item.occupancy}%`;
    document.getElementById("placeSeason").textContent = item.season;
    document.getElementById("placeRecommendation").textContent = `AI recommendation: ${item.recommendation}`;

    const gallery = document.getElementById("placeGallery");
    gallery.innerHTML = item.gallery.map((src, index) => `
        <figure>
            <img src="${src}" alt="${item.town} gallery image ${index + 1}" loading="lazy">
        </figure>
    `).join("");
}

fetch("/api/map")
    .then((response) => response.json())
    .then((items) => {
        items.forEach((item, index) => {
            const marker = L.circleMarker([item.lat, item.lon], {
                radius: 12,
                color: colors[item.saturation_level] || "#dbeafe",
                fillColor: colors[item.saturation_level] || "#dbeafe",
                fillOpacity: 0.88,
                weight: 3
            }).addTo(map);

            marker.bindPopup(`
                <strong>${item.town}</strong><br>
                Saturation: ${item.saturation_level}<br>
                Occupancy: ${item.occupancy}%<br>
                ${item.recommendation}
            `);

            marker.on("click", () => renderDestination(item));
            if (index === 0) renderDestination(item);
        });
    });
