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