document.addEventListener("DOMContentLoaded", () => {
    if (window.AOS) AOS.init({ duration: 700, once: true });

    document.querySelectorAll("[data-counter]").forEach((node) => {
        const target = Number(node.dataset.counter);
        const steps = 40;
        let current = 0;
        const timer = setInterval(() => {
            current += 1;
            const value = target * (current / steps);
            node.textContent = target % 1 === 0 
                ? Math.round(value).toLocaleString("en-US") 
                : value.toFixed(1);
            if (current >= steps) {
                clearInterval(timer);
                node.textContent = target.toLocaleString("en-US");
            }
        }, 25);
    });
});