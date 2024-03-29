import re
from typing import Any, Dict

import aqt
from anki.template import TemplateRenderContext

BUTTON_HTML = """\
<button class="yg-btn" id="yg-btn-{id}" style="min-width: 50px; min-height: 25px" \
onclick="onYGButtonClick(this)" data-hotkey="{hotkey}">{label}</button>
"""

WIDGET_HTML = """\
<a id="yg-widget-{id}" class="youglish-widget" data-query="{query}" data-lang="{lang}" {accent} \
data-zones="{zones}" data-components="{components}" \
data-bkg-color="{theme}" {width} {height} data-rest-mode="{restrict}" data-delay-load="1" \
rel="nofollow" href="https://youglish.com"></a>"""

# Component IDs to customize some features according to Youglish's documentation.
component_values = {
    "search_box": 1,
    "accent_panel": 2,
    "title": 4,
    "caption": 8,
    "speed_controls": 16,
    "control_buttons": 64,
    "dictionary": 128,
    "nearby_panel": 256,
    "phonetic_panel": 512,
    "draggable": 1024,
    "minimizable": 2048,
    "closable": 4096,
    "all_captions": 8192,
    "toggle_light": 16384,
    "toggle_thumbnails": 32768,
}


class YouGlishFilter:
    def __init__(
        self,
        ID: int,
        filter_text: str,
        text: str,
        context: TemplateRenderContext,
        config: Dict[str, Any],
    ):
        if not filter_text.startswith("aglish"):
            self.text = text
            raise Exception("not our filter")

        self.supported_options = {
            "nocaps",
            "lang",
            "zones",
            "accent",
            "theme",
            "autoplay",
            "label",
            "clozeonly",
            "width",
            "height",
            "restrict",
            "hotkey",
        }

        self.components = 0
        for key, value in component_values.items():
            self.components += value if config["components"].get(key, False) else 0

        self.ID = ID
        self.autoplay = False
        self.query = text
        self.context = context
        options = {}
        for option in map(lambda c: c.split("="), filter_text.split()[1:]):
            value = ""
            if len(option) >= 2:
                value = option[1]
            options[option[0].lower()] = value
        for option in self.supported_options:
            found = False
            if option in options:
                found = True
            value = options.get(option, "").lower()
            func = getattr(self, f"handle_{option}")
            func(found, value)

        self.populate_widget()

    def handle_nocaps(self, found: bool, value: str) -> None:
        if found:
            self.components -= (
                component_values["caption"] + component_values["all_captions"]
            )

    def handle_lang(self, found: bool, value: str) -> None:
        if not value:
            value = "en"
        self.lang = value

    def handle_zones(self, found: bool, value: str) -> None:
        if not value:
            value = "all"
        self.zones = value

    def handle_accent(self, found: bool, value: str) -> None:
        if value:
            value = 'data-accent="{}"'.format(value)
        self.accent = value

    def handle_theme(self, found: bool, value: str) -> None:
        if not value or value == "anki":
            if aqt.theme.theme_manager.night_mode:
                value = "dark"
            else:
                value = "light"
        value = "theme_" + value
        self.theme = value

    def handle_autoplay(self, found: bool, value: str) -> None:
        self.autoplay = found

    def handle_label(self, found: bool, value: str) -> None:
        if not value:
            value = "Youglish"
        self.label = value

    # We have a custom 'clozeonly' parameter for our filter akin to Anki's 'cloze-only' filter
    # that renders only clozed text, but on both sides of the card instead of just the back.
    # Adapted from Anki's source
    # (https://github.com/ankitects/anki/blob/e8d1a035a265e2f657f92c158f3fad40a4e0ce46/rslib/src/cloze.rs#L49)

    CLOZE = re.compile(r"(?xsi)\{\{c(\d+)::(.*?)(?:::(.*?))?\}\}")

    def _reveal_cloze_text_only(self) -> str:
        def match_cloze(match: re.Match) -> bool:
            try:
                captured_ord = int(match.group(1))
            except ValueError:
                captured_ord = 0
            return captured_ord == self.context.card().ord + 1

        matches = filter(match_cloze, self.CLOZE.finditer(self.query))
        return " ".join(map(lambda match: match.group(2), matches))

    def handle_clozeonly(self, found: bool, value: str) -> None:
        if not found:
            return
        self.query = self._reveal_cloze_text_only()

    def handle_width(self, found: bool, value: str) -> None:
        if value:
            value = f'width="{value}"'
        self.width = value

    def handle_height(self, found: bool, value: str) -> None:
        if value:
            value = f'height="{value}"'
        self.height = value

    def handle_restrict(self, found: bool, value: str) -> None:
        value = "1"
        if not found:
            value = "0"
        self.restrict = value

    def handle_hotkey(self, found: bool, value: str) -> None:
        self.hotkey = value

    def populate_widget(self) -> None:
        text = ""
        if not self.autoplay:
            text += BUTTON_HTML.format(id=self.ID, label=self.label, hotkey=self.hotkey)
        text += WIDGET_HTML.format(
            id=self.ID,
            query=self.query,
            components=self.components,
            lang=self.lang,
            accent=self.accent,
            zones=self.zones,
            theme=self.theme,
            width=self.width,
            height=self.height,
            restrict=self.restrict,
        )
        self.text = text
