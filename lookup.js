function onCreated() {
  if (browser.runtime.lastError) {
    console.log(`Error: ${browser.runtime.lastError}`);
  }
}

function onError(error) {
  console.log(`Error: ${error}`);
}

function getImageUrl(id) {
  return "http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=" + id + "&type=card";
}

function getGathererUrl(id) {
  return "http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=" + id;
}

browser.menus.create({
  id: "lookupOnGatherer",
  title: browser.i18n.getMessage("lookupOnGatherer"),
  icons: {
    "64": "icons/64.png"
  },
  contexts: ["selection"]
}, onCreated());

browser.menus.create({
  id: "lookupImage",
  title: browser.i18n.getMessage("lookupImage"),
  icons: {
    "64": "icons/img.png"
  },
  contexts: ["selection"]
}, onCreated());

browser.menus.onClicked.addListener((info, tab) => {
  let trimmed = info.selectionText.toLowerCase().trim();

  switch (info.menuItemId) {

    case "lookupImage":
      if (trimmed in cards) {
        var imagePopup = browser.windows.create({
          url: getImageUrl(cards[trimmed]),
          type: "panel"
        });
        imagePopup.then(onCreated, onError);
      }
      break;

      case "lookupOnGatherer":
      if (trimmed in cards) {
        var gathererTab = browser.tabs.create({
          url: getGathererUrl(cards[trimmed])
        });
        imagePopup.then(onCreated, onError);
      }
      break;
  }

});
