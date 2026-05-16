fetch("/api/dashboard")
    .then((response) => response.json())
    .then((data) => {
        const grid = "rgba(255,255,255,0.11)";
        const text = "#dbeafe";
        const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

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
                labels: data.months.map((month) => monthNames[month - 1] || `Month ${month}`),
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

        new Chart(document.getElementById("occupancyChart"), {
            type: "bar",
            data: {
                labels: data.towns,
                datasets: [{
                    label: "Occupancy %",
                    data: data.occupancy,
                    backgroundColor: data.occupancy.map((value) => value > 75 ? "#ef4f5f" : value > 45 ? "#f2bd3d" : "#32c977"),
                    borderRadius: 6
                }]
            },
            options: {
                indexAxis: "y",
                plugins: { legend: { labels: { color: text } } },
                scales: {
                    x: { ticks: { color: text }, grid: { color: grid }, max: 100 },
                    y: { ticks: { color: text }, grid: { color: grid } }
                }
            }
        });
    });
