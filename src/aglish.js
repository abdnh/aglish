
function playNonDelayedYGWidgets() {
    setTimeout(() => {
        const widgetElements = document.getElementsByClassName("youglish-widget");
        for (const el of widgetElements) {
            if (!el.previousElementSibling.classList.contains("yg-btn")) {
                const widget = YG.getWidget(el.id);
                const query = el.dataset.query;
                widget.fetch(query);
            }
        }
    }, 250);
}

function YGParsePageDelayed() {
    setTimeout(() => YG.parsePage(document), 250);
}

function onYGButtonClick(el) {
    const widgetElement = el.nextElementSibling;
    const widget = YG.getWidget(widgetElement.id);
    const query = widgetElement.dataset.query;
    widget.fetch(query)
}

document.addEventListener("keydown", (e) => {
    const ygButtons = document.getElementsByClassName("yg-btn");
    for (const button of ygButtons) {
        const key = e.key.toLowerCase();
        if (window.aglishHotkey.toLowerCase() == key || button.dataset.hotkey.toLowerCase() == key) {
            button.click();
        }
    }
});
