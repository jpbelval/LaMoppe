//import * as popup from "./lamoppe.js";

document.body.style.border = "5px solid red";

// Variables
const lockKey = ["Shift", "Alt"]
let lock = false;
let prevent = true;

// Event for keydown
addEventListener("keydown", async (event) => {
    if(lockKey.includes(event.key))
        lock = true;
    if(event.key === "Enter")
        if(!lock && (getText() != '')) {
            checkPrevention(event);
        }
}, true);

// Event for keyup
addEventListener("keyup", async (event) => {
    if(lockKey.includes(event.key))
        lock = false;
})

// Event for the right click on the send button
document.addEventListener("click", (event) => {
    const btn = event.target.closest("#composer-submit-button");
    if (!btn) return;
    checkPrevention(event);
}, true);

// Get the text in ChatGPT
function getText() {
    if (document.getElementById('prompt-textarea'))
        return document.getElementById('prompt-textarea').textContent;
    else
        return null
}

// Check for prevention
function checkPrevention(event) {
    if(prevent) {
        event.preventDefault();
        event.stopImmediatePropagation();
        event.stopPropagation();
        
        prevent = checkSafety();
    }
    else {
        prevent = true
    }
}

// Check the prompt with AI
function checkSafety() {
    // test 
    promptText = getText()
    const apiUrl = 'http://localhost:5000/classifyText';
    const postData = {
        prompt: promptText
    };
    console.log(JSON.stringify(postData))

    fetch(apiUrl, {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(postData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
    })
    .catch(error => {
        console.error('Error during fetch operation:', error);
    });

    let isNotSafe = true;
    //check
    //si pas safe
    // laisse a vrai
    // envoie au popup
    //sinon
    // met a faux et reclick
    if(!isNotSafe) {
        document.getElementById("composer-submit-button").click();
    }
    return isNotSafe;
}