function getText() {
    if (document.getElementById('prompt-textarea'))
        return document.getElementById('prompt-textarea').textContent;
    else
        return null
}

console.log(getText());