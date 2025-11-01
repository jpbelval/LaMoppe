document.body.style.border = "5px solid red";

const lockKey = ["Shift", "Alt"]
let lock = false;

addEventListener("keydown", async (event) => {
    if(lockKey.includes(event.key))
        lock = true;
    if(event.key === "Enter")
        if(!lock && (getText() != '')) {
            event.preventDefault();
            event.stopImmediatePropagation();
            event.stopPropagation();
        }
}, true);

addEventListener("keyup", async (event) => {
    if(lockKey.includes(event.key))
        lock = false;
})

document.addEventListener("click", (e) => {
    const btn = document.getElementById("composer-submit-button");
    if (!btn) return;
    e.preventDefault();
    e.stopImmediatePropagation();
    e.stopPropagation();
}, true);

function getText() {
    if (document.getElementById('prompt-textarea'))
        return document.getElementById('prompt-textarea').textContent;
    else
        return null
}