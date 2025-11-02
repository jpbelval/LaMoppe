let count = 0;
let messages = [];

browser.runtime.onMessage.addListener((message) => {
    if (message.event === "NewMessage") {
        sendNotification();
        messages.push(message.data);
    }
    else if (message.event === "subCount") {
        count = count - 1;
        updateNotif();
        let i = 0;
        while(messages[i].uuid !== message.data)
            i = i + 1;
        sendReview(messages[i])
        messages.splice(i, 1);
    }
    else if (message.event === "fetchData") {
        browser.runtime.sendMessage({
            event: "sendData",
            data: messages
        });
    }
    else if (message.event === "updateMessages") {
        messages = message.data;
    }
});

function sendNotification() {
    browser.notifications.create({
        type: "basic",
        iconUrl: browser.runtime.getURL("icons/logo48.png"),
        title: "Clean your prompt",
        message: "See extension for more info"
    });

    count = count + 1;
    updateNotif();
}

function sendCustom(text) {
    browser.notifications.create({
        type: "basic",
        iconUrl: browser.runtime.getURL("icons/logo48.png"),
        title: "Clean your prompt",
        message: text
    });

    count = count + 1;
    updateNotif();
}

function updateNotif() {
    if(count) {
        browser.browserAction.setBadgeText({ text: String(count)});
        browser.browserAction.setBadgeBackgroundColor({ color: "#FF3B30" });
    }
    else
        browser.browserAction.setBadgeText({text: ""})
}

async function sendReview(data){
    const apiUrl = 'http://localhost:5000/createRating';
    const postData = {
        risk_level: data.risk_level,
        private_data: data.private_data,
        safe_prompt: data.safe_prompt,
        review: data.review
    };
    try {
        const response = await fetch(apiUrl, {
            method: 'POST', 
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(postData)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Success:', data);
    } catch (error) {
        console.error('Error during fetch operation:', error);
    }
}