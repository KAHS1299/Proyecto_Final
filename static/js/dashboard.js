fetch("/api/dashboard")
    .then((response) => response.json())
    .then((data) => {
        const grid = "rgba(255,255,255,0.11)";
        const text = "#dbeafe";

        new Chart(document.getElementById("barChart"), {
            type: "bar",
            data: {
                labels: data.pueblos,
                datasets: [{
                    label: "Turistas",
                    data: data.turistas,
                    borderWidth: 0,
                    borderRadius: 6,
                    backgroundColor: "rgba(22,184,255,0.72)"
                }]
            },
            options: {
                plugins: { legend: { labels: { color: text } } },
                scales: {
                    x: { ticks: { color: text }, grid: { color: grid } },
                    y: { ticks: { color: text }, grid: { color: grid } }
                }
            }
        });

        new Chart(document.getElementById("donutChart"), {
            type: "doughnut",
            data: {
                labels: ["Baja", "Media", "Alta"],
                datasets: [{
                    data: data.niveles,
                    backgroundColor: ["#31d67b", "#f6c945", "#ff5a73"],
                    borderColor: "#0c1224"
                }]
            },
            options: {
                plugins: { legend: { labels: { color: text } } }
            }
        });

        new Chart(document.getElementById("lineChart"), {
            type: "line",
            data: {
                labels: data.meses.map((month) => `Mes ${month}`),
                datasets: [{
                    label: "Turistas por mes",
                    data: data.mensual,
                    borderColor: "#ff4fd8",
                    backgroundColor: "rgba(255,79,216,0.16)",
                    fill: true,
                    tension: 0.36
                }]
            },
            options: {
                plugins: { legend: { labels: { color: text } } },
                scales: {
                    x: { ticks: { color: text }, grid: { color: grid } },
                    y: { ticks: { color: text }, grid: { color: grid } }
                }
            }
        });
    });
