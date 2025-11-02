let messages = [];
const messageContainer = document.getElementById("prompts-container");

browser.runtime.sendMessage({
    event: "fetchData"
});

browser.runtime.onMessage.addListener((message) => {
    if (message.event === "sendData") {
        messages = message.data;
        renderMessages();
    }
});

function renderMessages() {
    messageContainer.innerHTML = "";

    messages.forEach((msg, i) => {
        const line = document.createElement("div");
        line.classList.add("message-block");

        const header = document.createElement("h3");
        header.textContent = `Risk Level: ${msg.risk_level || "unknown"}`;
        header.classList.add("risk-header");

        let highlightedPrompt = msg.risk_prompt;
        if (Array.isArray(msg.private_data)) {
            msg.private_data.forEach(data => {
                if (data) {
                    const regex = new RegExp(data.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), "gi");
                    highlightedPrompt = highlightedPrompt.replace(regex, `<mark>${data}</mark>`);
                }
            });
        }

        const riskP = document.createElement("p");
        riskP.innerHTML = highlightedPrompt;
        riskP.classList.add("risk-prompt");

        const safeP = document.createElement("p");
        safeP.textContent = msg.safe_prompt || "";
        safeP.classList.add("safe-prompt");
        safeP.style.display = "none";

        // Toggle button
        const toggleBtn = document.createElement("button");
        toggleBtn.textContent = "Show safe prompt";
        toggleBtn.classList.add("toggle-btn");

        toggleBtn.addEventListener("click", () => {
            const isVisible = safeP.style.display === "block";
            safeP.style.display = isVisible ? "none" : "block";
            toggleBtn.textContent = isVisible ? "Show safe prompt" : "Hide safe prompt";
        });

        // --- Bouton Review ---
        const reviewBtn = document.createElement("button");
        reviewBtn.textContent = "Review";

        reviewBtn.addEventListener("click", () => {
            let intervalId;

            // Ajouter animation de rotation
            reviewBtn.classList.add("spinning");

            // Créer l'objet audio et le jouer en boucle
            const spinSound = new Audio(browser.runtime.getURL("sounds/csgo.mp3"));
            spinSound.loop = true;
            spinSound.play().catch(err => console.error("Erreur audio :", err));

            spinSound.loop = true;
            spinSound.play();

            const spin = () => {
                const randomNumber = Math.floor(Math.random() * 10) + 1;
                reviewBtn.textContent = randomNumber;
            };

            intervalId = setInterval(spin, 100);

            setTimeout(() => {
                clearInterval(intervalId);
                const finalNumber = Math.floor(Math.random() * 10) + 1;
                reviewBtn.textContent = finalNumber;
                reviewBtn.disabled = true;

                // Garder le bouton clair
                reviewBtn.style.opacity = "1";
                reviewBtn.style.backgroundColor = "#f0f0f0";
                reviewBtn.style.color = "black";
                reviewBtn.style.cursor = "default";

                // Retirer l'animation
                reviewBtn.classList.remove("spinning");

                // Arrêter le son
                spinSound.pause();
                spinSound.currentTime = 0;
            }, 6000);
        });


        // Texte message
        const p = document.createElement("p");
        p.textContent = msg.safe_prompt;

        // Bouton X
        const removeBtn = document.createElement("button");
        removeBtn.textContent = "X";
        removeBtn.classList.add("remove-btn");
        removeBtn.addEventListener("click", () => {
            const subMessage = messages.splice(i, 1);
            renderMessages();
            browser.runtime.sendMessage({
                event: "subCount",
                data: removed[0]
            });
        });


        // On assemble la ligne
        line.appendChild(header)
        line.appendChild(riskP)
        line.appendChild(toggleBtn);
        line.appendChild(safeP);
        line.appendChild(removeBtn);
        messageContainer.appendChild(line);
    });
}
