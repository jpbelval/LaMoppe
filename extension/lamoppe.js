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
    // Vide le conteneur avant de réafficher
    messageContainer.innerHTML = "";

    messages.forEach((msg, i) => {
        // Conteneur de la ligne
        const line = document.createElement("div");

        // Texte
        const p = document.createElement("p");
        p.textContent = msg;

        // Bouton X
        const btn = document.createElement("button");
        btn.textContent = "X"; // plus joli que "X"

        // Quand on clique sur le bouton, on supprime le message
        btn.addEventListener("click", () => {
            subMessage = messages.splice(i, 1);
            renderMessages();

            browser.runtime.sendMessage({
                event: "subCount",
                data: subMessage[0]
            });
        });

        // On assemble la ligne
        line.appendChild(p);
        line.appendChild(btn);
        messageContainer.appendChild(line);
    });
}