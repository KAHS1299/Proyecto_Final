const form = document.getElementById("predictionForm");
const level = document.getElementById("resultLevel");
const text = document.getElementById("resultText");
const tourists = document.getElementById("resultTourists");
const recommendation = document.getElementById("resultRecommendation");
const confidenceBar = document.getElementById("confidenceBar");
const confidenceText = document.getElementById("confidenceText");
let probabilityChart;

function renderProbabilities(probabilities) {
    const labels = ["Low", "Medium", "High"];
    const values = labels.map((label) => probabilities[label] || 0);
    if (probabilityChart) probabilityChart.destroy();
    probabilityChart = new Chart(document.getElementById("probabilityChart"), {
        type: "bar",
        data: {
            labels,
            datasets: [{
                label: "Probability %",
                data: values,
                backgroundColor: ["#32c977", "#f2bd3d", "#ef4f5f"],
                borderRadius: 6
            }]
        },
        options: {
            plugins: { legend: { labels: { color: "#dbeafe" } } },
            scales: {
                x: { ticks: { color: "#dbeafe" }, grid: { color: "rgba(255,255,255,0.1)" } },
                y: { ticks: { color: "#dbeafe" }, grid: { color: "rgba(255,255,255,0.1)" }, max: 100 }
            }
        }
    });
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const payload = Object.fromEntries(new FormData(form).entries());
    payload.events = Number(payload.events);
    payload.month = Number(payload.month);
    payload.historical_tourists = Number(payload.historical_tourists);

    const response = await fetch("/api/prediction", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });
    const result = await response.json();

    level.className = "";
    level.classList.add(`level-${result.level.toLowerCase()}`);
    level.textContent = `Saturation: ${result.level}`;
    text.textContent = result.explanation;
    tourists.textContent = Number(result.tourists).toLocaleString("en-US");
    recommendation.textContent = result.recommendation;
    confidenceBar.style.width = `${result.confidence}%`;
    confidenceText.textContent = `${result.confidence}%`;
    renderProbabilities(result.probabilities);
});
