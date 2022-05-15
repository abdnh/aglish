
function playNonDelayedYGWidgets() {
    setTimeout(() => {
        var widgetElements = document.querySelectorAll('[id^=yg-widget-]');
        for (let el of widgetElements) {
            if (!el.previousElementSibling.classList.contains("yg-btn")) {
                let widget = YG.getWidget(el.id);
                let query = el.dataset.query;
                widget.fetch(query);
            }
        }
    }, 250);
}

function YGParsePageDelayed() {
    setTimeout(() => YG.parsePage(document), 250);
}

function onYGButtonClick(el) {
    let widgetElement = el.nextElementSibling;
    let widget = YG.getWidget(widgetElement.id);
    let query = widgetElement.dataset.query;
    widget.fetch(query)
}

document.addEventListener("keydown", (e) => {
    const ygButtons = document.getElementsByClassName("yg-btn");
    for (const button of ygButtons) {
        if (button.dataset.hotkey.toLowerCase() == e.key.toLowerCase()) {
            button.click();
        }
    }
});
