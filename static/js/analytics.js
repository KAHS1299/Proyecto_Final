const chartText = "#dbeafe";
const chartGrid = "rgba(255,255,255,0.1)";

fetch("/api/analytics")
    .then((response) => response.json())
    .then((metrics) => {
        document.getElementById("accuracyMetric").textContent = `${Math.round(metrics.accuracy * 100)}%`;
        document.getElementById("precisionMetric").textContent = `${Math.round(metrics.precision * 100)}%`;
        document.getElementById("recallMetric").textContent = `${Math.round(metrics.recall * 100)}%`;
        document.getElementById("f1Metric").textContent = `${Math.round(metrics.f1 * 100)}%`;

        new Chart(document.getElementById("featureChart"), {
            type: "bar",
            data: {
                labels: metrics.feature_importance.map((item) => item.feature),
                datasets: [{
                    label: "Importance",
                    data: metrics.feature_importance.map((item) => item.importance),
                    backgroundColor: "rgba(33,199,183,0.72)",
                    borderRadius: 6
                }]
            },
            options: {
                indexAxis: "y",
                plugins: { legend: { labels: { color: chartText } } },
                scales: {
                    x: { ticks: { color: chartText }, grid: { color: chartGrid } },
                    y: { ticks: { color: chartText }, grid: { color: chartGrid } }
                }
            }
        });

        const matrix = document.getElementById("matrixGrid");
        matrix.innerHTML = `<span></span>${metrics.labels.map((label) => `<b>Pred ${label}</b>`).join("")}`;
        metrics.confusion_matrix.forEach((row, index) => {
            matrix.innerHTML += `<b>True ${metrics.labels[index]}</b>${row.map((cell) => `<strong>${cell}</strong>`).join("")}`;
        });
    });

fetch("/api/monitoring")
    .then((response) => response.json())
    .then((monitoring) => {
        new Chart(document.getElementById("driftChart"), {
            type: "line",
            data: {
                labels: monitoring.labels,
                datasets: [{
                    label: "Population Stability Drift",
                    data: monitoring.drift,
                    borderColor: "#ff7468",
                    backgroundColor: "rgba(255,116,104,0.16)",
                    fill: true,
                    tension: 0.35
                }]
            },
            options: {
                plugins: { legend: { labels: { color: chartText } } },
                scales: {
                    x: { ticks: { color: chartText }, grid: { color: chartGrid } },
                    y: { ticks: { color: chartText }, grid: { color: chartGrid } }
                }
            }
        });

        new Chart(document.getElementById("confidenceTrendChart"), {
            type: "line",
            data: {
                labels: monitoring.labels,
                datasets: [{
                    label: "Average Confidence",
                    data: monitoring.confidence,
                    borderColor: "#21c7b7",
                    backgroundColor: "rgba(33,199,183,0.16)",
                    fill: true,
                    tension: 0.35
                }]
            },
            options: {
                plugins: { legend: { labels: { color: chartText } } },
                scales: {
                    x: { ticks: { color: chartText }, grid: { color: chartGrid } },
                    y: { ticks: { color: chartText }, grid: { color: chartGrid }, min: 0.7, max: 1 }
                }
            }
        });
        document.getElementById("retrainingNote").textContent = monitoring.retraining;
    });
