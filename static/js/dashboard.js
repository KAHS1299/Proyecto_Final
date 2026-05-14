fetch("/api/dashboard")
    .then((response) => response.json())
    .then((data) => {
        const grid = "rgba(255,255,255,0.11)";
        const text = "#dbeafe";

        // Bar Chart
        new Chart(document.getElementById("barChart"), {
            type: "bar",
            data: {
                labels: data.towns,
                datasets: [{
                    label: "Tourists",
                    data: data.tourists,
                    backgroundColor: "rgba(33,199,183,0.72)",
                    borderRadius: 6
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

        // Donut Chart
        new Chart(document.getElementById("donutChart"), {
            type: "doughnut",
            data: {
                labels: ["Low", "Medium", "High"],
                datasets: [{
                    data: data.levels,
                    backgroundColor: ["#32c977", "#f2bd3d", "#ef4f5f"],
                    borderColor: "#0c1224"
                }]
            },
            options: {
                plugins: { legend: { labels: { color: text } } }
            }
        });

        // Line Chart
        new Chart(document.getElementById("lineChart"), {
            type: "line",
            data: {
                labels: data.months.map(m => `Month ${m}`),
                datasets: [{
                    label: "Monthly Flow",
                    data: data.monthly,
                    borderColor: "#ff7468",
                    fill: true,
                    tension: 0.3
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
