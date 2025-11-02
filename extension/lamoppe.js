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
        p.textContent = msg;

        // --- Bouton X ---
        const delBtn = document.createElement("button");
        delBtn.textContent = "X";

        delBtn.addEventListener("click", () => {
            const removed = messages.splice(i, 1);
            renderMessages();

            browser.runtime.sendMessage({
                event: "subCount",
                data: removed[0]
            });
        });

        // Assemble
        line.appendChild(reviewBtn);
        line.appendChild(p);
        line.appendChild(delBtn);
        messageContainer.appendChild(line);
    });
}
