const form = document.getElementById("predictionForm");
const level = document.getElementById("resultLevel");
const text = document.getElementById("resultText");
const tourists = document.getElementById("resultTourists");
const recommendation = document.getElementById("resultRecommendation");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    // 1. Capturamos los datos del formulario
    const payload = Object.fromEntries(new FormData(form).entries());
    
    // 2. Convertimos a números con los nombres en INGLÉS que espera app.py
    // Importante: Asegúrate que en tu HTML los 'name' del formulario coincidan
    payload.events = Number(payload.events); 
    payload.month = Number(payload.month);
    payload.historical_tourists = Number(payload.historical_tourists);

    try {
        // 3. Enviamos a la ruta /api/prediction (en inglés)
        const response = await fetch("/api/prediction", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        // 4. Mostramos el resultado (usando las llaves en inglés del JSON de respuesta)
        level.className = "";
        // level, explanation, tourists, recommendation vienen de tu app.py
        level.classList.add(`level-${result.level.toLowerCase()}`);
        level.textContent = `Saturation: ${result.level}`;
        
        text.textContent = result.explanation;
        tourists.textContent = Number(result.tourists).toLocaleString("en-US");
        recommendation.textContent = result.recommendation;

    } catch (error) {
        console.error("Prediction error:", error);
    }
});
