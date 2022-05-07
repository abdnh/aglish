import re

import aqt
from anki.template import TemplateRenderContext

BUTTON_HTML = """\
<button id="yg-btn-{id}" style="min-width: 50px; min-height: 25px" \
onclick="onYGButtonClick(this)">{label}</button>
"""

WIDGET_HTML = """\
<a id="yg-widget-{id}" class="youglish-widget" data-query="{query}" data-lang="{lang}" {accent} \
data-zones="{zones}" data-components="{components}" \
data-bkg-color="{theme}" {width} {height} data-delay-load="1" \
rel="nofollow" href="https://youglish.com"></a>"""

# Component IDs to customize some features according to Youglish's documentation.
# Most customizations are not utilized by this add-on yet
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
    ):
        if not filter_text.startswith("aglish"):
            self.text = text
            raise Exception("not our filter")

        self.funcs = {
            "nocaps": self.nocaps_filter,
            "lang": self.lang_filter,
            "zones": self.zones_filter,
            "accent": self.accent_filter,
            "theme": self.theme_filter,
            "autoplay": self.autoplay_filter,
            "label": self.label_filter,
            "clozeonly": self.cloze_only_filter,
            "width": self.width_filter,
            "height": self.height_filter,
        }

        self.components = 10495
        self.ID = ID
        self.autoplay = False
        self.query = text
        self.context = context
        configs = {}
        for config in map(lambda c: c.split("="), filter_text.split()[1:]):
            value = ""
            if len(config) >= 2:
                value = config[1]
            configs[config[0]] = value

        for config_filter in self.funcs:
            found = False
            if config_filter in configs:
                found = True
            value = configs.get(config_filter, "")
            func = self.funcs[config_filter]
            func(found, value.lower())

        self.populate_widget()

    def nocaps_filter(self, found: bool, value: str):
        if found:
            self.components -= (
                component_values["caption"] + component_values["all_captions"]
            )

    def lang_filter(self, found: bool, value: str):
        if not value:
            value = "en"
        self.lang = value

    def zones_filter(self, found: bool, value: str):
        if not value:
            value = "all"
        self.zones = value

    def accent_filter(self, found: bool, value: str):
        if value:
            value = 'data-accent="{}"'.format(value)
        self.accent = value

    def theme_filter(self, found: bool, value: str):
        if not value or value == "anki":
            if aqt.theme.theme_manager.night_mode:
                value = "dark"
            else:
                value = "light"
        value = "theme_" + value
        self.theme = value

    def autoplay_filter(self, found: bool, value: str):
        self.autoplay = found

    def label_filter(self, found: bool, value: str):
        if not value:
            value = "Youglish"
        self.label = value

    # We have a custom 'clozeonly' parameter for our filter akin to Anki's 'cloze-only' filter
    # that renders only clozed text, but on both sides of the card instead of just the back.
    # Adapted from Anki's source
    # (https://github.com/ankitects/anki/blob/e8d1a035a265e2f657f92c158f3fad40a4e0ce46/rslib/src/cloze.rs#L49)

    CLOZE = re.compile(r"(?xsi)\{\{c(\d+)::(.*?)(?:::(.*?))?\}\}")

    def _reveal_cloze_text_only(self) -> str:
        def match_filter(match: re.Match) -> bool:
            try:
                captured_ord = int(match.group(1))
            except ValueError:
                captured_ord = 0
            return captured_ord == self.context.card().ord + 1

        matches = filter(match_filter, self.CLOZE.finditer(self.query))
        return " ".join(map(lambda match: match.group(2), matches))

    def cloze_only_filter(self, found: bool, value: str):
        if not found:
            return
        self.query = self._reveal_cloze_text_only()

    def width_filter(self, found: bool, value: str):
        if value:
            value = f'width="{value}"'
        self.width = value

    def height_filter(self, found: bool, value: str):
        if value:
            value = f'height="{value}"'
        self.height = value

    def populate_widget(self):
        text = ""
        if not self.autoplay:
            text += BUTTON_HTML.format(id=self.ID, label=self.label)
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
        )
        self.text = text
