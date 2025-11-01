document.body.style.border = "5px solid red";
preSubmit()

const lockKey = ["Shift", "Alt"]
let lock = false;

addEventListener("keydown", async (event) => {
    if(lockKey.includes(event.key))
        lock = true;
    if(event.key === "Enter")
        if(!lock && (getText() != '')) {
            event.preventDefault()
            console.log('send');
        }
})

addEventListener("keyup", async (event) => {
    console.log(getText())
    if(lockKey.includes(event.key))
        lock = false;
})

function preSubmit() {
    //console.log('script roule');
    let form = document.querySelector('form')
    console.log(form)
    
    form.addEventListener("*", async (event) =>  {
        console.log(event);
    });
}

function logSubmit(event) {
    console.log('fonctionne')
    event.preventDefault();
}

function getText() {
    if (document.getElementById('prompt-textarea'))
        return document.getElementById('prompt-textarea').textContent;
    else
        return null
}