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
        messages.splice(messages.indexOf(message.data), 1);
    }
    else if (message.event === "fetchData") {
        browser.runtime.sendMessage({
            event: "sendData",
            data: messages
        });
    }
});

function sendNotification() {
    browser.notifications.create({
        type: "basic",
        iconUrl: browser.runtime.getURL("icons/logo48.png"),
        title: "Nettoyez votre requête",
        message: "Référez vous à l'extension"
    });

    count = count + 1;
    updateNotif();
}

function sendCustom(text) {
    browser.notifications.create({
        type: "basic",
        iconUrl: browser.runtime.getURL("icons/logo48.png"),
        title: "Nettoyez votre requête",
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