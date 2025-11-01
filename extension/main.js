document.body.style.border = "5px solid red";
preSubmit();


function preSubmit() {
    //console.log('script roule');
    let abc = document.querySelector('form')
    console.log(abc)
    document.querySelector('form').addEventListener('onsubmit', async (event) =>  {
        event.preventDefault();
        console.log('fonctionne');
    });
}

function getText() {
    if (document.getElementById('prompt-textarea'))
        return document.getElementById('prompt-textarea').textContent;
    else
        return null
}