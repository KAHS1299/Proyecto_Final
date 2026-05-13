const form = document.getElementById("predictionForm");
const level = document.getElementById("resultLevel");
const text = document.getElementById("resultText");
const tourists = document.getElementById("resultTourists");
const recommendation = document.getElementById("resultRecommendation");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const payload = Object.fromEntries(new FormData(form).entries());
    payload.eventos = Number(payload.eventos);
    payload.mes = Number(payload.mes);
    payload.turistas_historicos = Number(payload.turistas_historicos);

    const response = await fetch("/api/prediccion", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });
    const result = await response.json();

    level.className = "";
    level.classList.add(`level-${result.nivel.toLowerCase()}`);
    level.textContent = `Saturacion ${result.nivel}`;
    text.textContent = result.explicacion;
    tourists.textContent = Number(result.turistas).toLocaleString("es-CO");
    recommendation.textContent = result.recomendacion;
});
