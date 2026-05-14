const map = L.map("map", { scrollWheelZoom: false }).setView([5.7, -74.5], 6);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 18,
    attribution: "&copy; OpenStreetMap"
}).addTo(map);

const colors = {
    Baja: "#32c977",
    Media: "#f2bd3d",
    Alta: "#ef4f5f"
};

const destinationInfo = {
    "Villa de Leyva": {
        description: "Uno de los pueblos coloniales mas reconocidos de Boyaca, famoso por su plaza empedrada, arquitectura blanca y entorno historico.",
        detail: "Plan recomendado: recorrer la Plaza Mayor, visitar museos como el Paleontologico o el Fosil, caminar por sus calles coloniales y reservar tiempo para Pozos Azules o Raquira.",
        query: "Villa de Leyva Plaza Mayor Boyaca Colombia"
    },
    Barichara: {
        description: "Pueblo santandereano de calles en piedra, casas blancas y miradores hacia el paisaje del canon del Suarez.",
        detail: "Plan recomendado: caminar sin prisa por el centro historico, visitar la catedral, probar la gastronomia local y hacer el Camino Real hacia Guane.",
        query: "Barichara Santander Colombia street"
    },
    Salento: {
        description: "Destino cafetero del Quindio, reconocido por sus fachadas coloridas y por ser entrada al Valle de Cocora.",
        detail: "Plan recomendado: madrugar al Valle de Cocora, tomar cafe de origen, subir a los miradores y recorrer la Calle Real antes de las horas de mayor flujo.",
        query: "Salento Valle de Cocora Quindio Colombia"
    },
    Guatape: {
        description: "Pueblo antioqueno de zocalos coloridos, malecon junto al embalse y acceso a la Piedra del Penol.",
        detail: "Plan recomendado: subir temprano a la Piedra, recorrer las calles decoradas, navegar por el embalse y evitar domingos si buscas una visita tranquila.",
        query: "Guatape Piedra del Penol Colombia"
    },
    Jardin: {
        description: "Pueblo cafetero de Antioquia con plaza viva, balcones tradicionales, montanas y rutas de naturaleza.",
        detail: "Plan recomendado: pasar por la plaza principal, tomar cafe local, usar el teleferico o miradores y reservar recorridos de naturaleza como cascadas o avistamiento de aves.",
        query: "Jardin Antioquia Colombia plaza"
    },
    Filandia: {
        description: "Municipio del Paisaje Cultural Cafetero con casas coloridas, miradores y tradicion artesanal.",
        detail: "Plan recomendado: visitar el mirador Colina Iluminada, recorrer talleres artesanales, probar cocina local y usarlo como alternativa mas calmada cerca de Salento.",
        query: "Filandia Quindio Colombia mirador"
    },
    "Santa Cruz de Mompox": {
        description: "Destino patrimonial a orillas del rio Magdalena, con iglesias coloniales, filigrana y una atmosfera historica muy marcada.",
        detail: "Plan recomendado: caminar por el centro historico, visitar templos coloniales, conocer talleres de filigrana y hacer un recorrido por el rio al atardecer.",
        query: "Mompox Colombia Magdalena colonial"
    },
    "Santa Fe de Antioquia": {
        description: "Antigua capital antioquena, de clima calido, arquitectura colonial y cercania al Puente de Occidente.",
        detail: "Plan recomendado: recorrer la plaza, visitar iglesias y casonas, cruzar al Puente de Occidente y planear desplazamientos evitando horas pico de entrada.",
        query: "Santa Fe de Antioquia Colombia colonial"
    },
    Jerico: {
        description: "Pueblo del suroeste antioqueno con balcones coloridos, tradicion religiosa, cultura cafetera y paisaje de montana.",
        detail: "Plan recomendado: conocer el parque principal, visitar museos y talleres de carriel, subir a miradores como Cristo Rey y combinar cultura con caminatas cercanas.",
        query: "Jerico Antioquia Colombia town"
    },
    Mongui: {
        description: "Pueblo boyacense de arquitectura colonial, puente historico y cercania al paramo de Oceta.",
        detail: "Plan recomendado: visitar la basilica y el Puente de Calicanto, conocer talleres de balones artesanales y hacer el paramo con guia y ropa abrigada.",
        query: "Mongui Boyaca Colombia plaza"
    },
    Salamina: {
        description: "Pueblo caldense del Paisaje Cultural Cafetero, conocido por balcones tallados, calles tranquilas y arquitectura tradicional.",
        detail: "Plan recomendado: caminar por el centro historico, observar balcones y puertas coloniales, probar cafe local y visitar el valle de la Samaria si el clima lo permite.",
        query: "Salamina Caldas Colombia town"
    },
    Honda: {
        description: "Pueblo patrimonial del Tolima junto al rio Magdalena, reconocido por puentes, cuestas, memoria comercial y ambiente ribereno.",
        detail: "Plan recomendado: recorrer el centro historico, cruzar sus puentes, visitar museos locales y planear caminatas temprano por el clima calido.",
        query: "Honda Tolima Colombia colonial"
    }
};

const commonsCache = new Map();
const fallbackImages = [
    "https://commons.wikimedia.org/wiki/Special:FilePath/Plaza_Mayor_-_Villa_de_Leyva%2C_Boyac%C3%A1%2C_Colombia.jpg?width=900",
    "https://commons.wikimedia.org/wiki/Special:FilePath/Valle_de_Cocora_Salento.jpg?width=900",
    "https://commons.wikimedia.org/wiki/Special:FilePath/Barichara_Colombia_01.JPG?width=900"
];

const panel = {
    name: document.getElementById("placeName"),
    description: document.getElementById("placeDescription"),
    detail: document.getElementById("placeDetail"),
    level: document.getElementById("placeLevel"),
    visitors: document.getElementById("placeVisitors"),
    occupancy: document.getElementById("placeOccupancy"),
    recommendation: document.getElementById("placeRecommendation"),
    gallery: document.getElementById("placeGallery")
};

function commonsUrl(query) {
    const params = new URLSearchParams({
        action: "query",
        generator: "search",
        gsrnamespace: "6",
        gsrlimit: "10",
        gsrsearch: `${query} turismo -map -flag -logo`,
        prop: "imageinfo",
        iiprop: "url|mime",
        iiurlwidth: "900",
        format: "json",
        origin: "*"
    });

    return `https://commons.wikimedia.org/w/api.php?${params.toString()}`;
}

async function loadCommonsImages(query) {
    if (commonsCache.has(query)) {
        return commonsCache.get(query);
    }

    try {
        const response = await fetch(commonsUrl(query));
        const data = await response.json();
        const pages = Object.values(data.query?.pages || {});
        const images = pages
            .map((page) => page.imageinfo?.[0])
            .filter((image) => image && image.mime && image.mime.startsWith("image/") && image.mime !== "image/svg+xml")
            .map((image) => image.thumburl || image.url)
            .slice(0, 3);

        const result = images.length ? images : fallbackImages;
        commonsCache.set(query, result);
        return result;
    } catch (error) {
        return fallbackImages;
    }
}

function renderGallery(images, town) {
    panel.gallery.innerHTML = images.map((src, index) => `
        <figure>
            <img src="${src}" alt="Imagen turistica de ${town} ${index + 1}" loading="lazy">
        </figure>
    `).join("");
}

function renderDestination(item) {
    const info = destinationInfo[item.pueblo] || {
        description: "Destino colombiano con valor cultural, historico y natural.",
        detail: "Plan recomendado: revisar temporada, ocupacion y movilidad antes de programar el recorrido.",
        query: item.pueblo
    };
    const level = item.nivel_saturacion;

    panel.name.textContent = item.pueblo;
    panel.description.textContent = info.description;
    panel.detail.textContent = info.detail;
    panel.level.textContent = level;
    panel.level.className = `level-${level.toLowerCase()}`;
    panel.visitors.textContent = Number(item.turistas_estimados).toLocaleString("es-CO");
    panel.occupancy.textContent = `${item.ocupacion}%`;
    panel.recommendation.textContent = item.recomendacion;
    panel.gallery.innerHTML = '<div class="gallery-loading">Cargando imagenes del destino...</div>';

    loadCommonsImages(info.query).then((images) => {
        if (panel.name.textContent === item.pueblo) {
            renderGallery(images, item.pueblo);
        }
    });
}

fetch("/api/mapa")
    .then((response) => response.json())
    .then((items) => {
        items.forEach((item, index) => {
            const marker = L.circleMarker([item.lat, item.lng], {
                radius: 12,
                color: colors[item.nivel_saturacion],
                fillColor: colors[item.nivel_saturacion],
                fillOpacity: 0.82,
                weight: 3
            }).addTo(map);

            marker.bindPopup(`
                <strong>${item.pueblo}</strong><br>
                Saturacion: <b>${item.nivel_saturacion}</b><br>
                Turistas esperados: ${Number(item.turistas_estimados).toLocaleString("es-CO")}<br>
                Ocupacion: ${item.ocupacion}%<br>
                <small>${item.recomendacion}</small>
            `);

            marker.on("click", () => {
                renderDestination(item);
                marker.openPopup();
            });

            if (index === 0) {
                renderDestination(item);
            }
        });
    });