browser.notifications.create({
  type: "basic",
  iconUrl: browser.runtime.getURL("icons/logo48.png"),
  title: "Nettoyez votre requête",
  message: "T'es trop dumb pour ecrire à un AI, arrête."
});