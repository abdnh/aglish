import re
from typing import Optional, Any

import anki
import aqt

BUTTON_HTML = """<button id="yg-btn-{id}" style="min-width: 50px; min-height: 25px" onclick="onYGButtonClick(this)">{label}</button>"""
WIDGET_HTML = """<a id="yg-widget-{id}" class="youglish-widget" data-query="{query}" data-lang="{lang}" {accent} data-zones="{zones}" data-components="{components}" data-bkg-color="{theme}" {width} {height} data-delay-load="1" rel="nofollow" href="https://youglish.com"></a>"""

# component IDs to customize some features according to Youglish's documentation; most customizations are not utilized by this add-on yet
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
        filter_name: str,
        text: str,
        context: anki.template.TemplateRenderContext,
    ):
        if not filter_name.startswith("aglish"):
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
        for config in map(lambda c: c.split("="), filter_name.split(" ")[1:]):
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

    # we have a custom 'clozeonly' parameter for our filter akin to Anki's 'cloze-only' filter that renders only clozed text, but on both sides of the card instead of just the back
    # adapted from Anki's source (https://github.com/ankitects/anki/blob/e8d1a035a265e2f657f92c158f3fad40a4e0ce46/rslib/src/cloze.rs#L49)

    CLOZE = re.compile(r"(?xsi)\{\{c(\d+)::(.*?)(?:::(.*?))?\}\}")

    def _reveal_cloze_text_only(self) -> str:
        def match_filter(m: re.Match) -> bool:
            try:
                captured_ord = int(m.group(1))
            except ValueError:
                captured_ord = 0
            return captured_ord == self.context.card().ord + 1

        matches = filter(match_filter, self.CLOZE.finditer(self.query))
        return " ".join(map(lambda m: m.group(2), matches))

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


cur_id = 0


def youglish_filter(
    field_text: str,
    field_name: str,
    filter_name: str,
    context: anki.template.TemplateRenderContext,
) -> str:

    global cur_id

    try:
        youglish = YouGlishFilter(cur_id, filter_name, field_text, context)
    except Exception as ex:
        return field_text

    cur_id += 1

    return youglish.text


def on_card_did_render(
    output: anki.template.TemplateRenderOutput,
    context: anki.template.TemplateRenderContext,
):
    global cur_id
    cur_id = 0
    js = "<script>YGParsePageDelayed(); playNonDelayedYGWidgets()</script>"
    output.question_text += js
    output.answer_text += js


def on_webview_will_set_content(
    web_content: aqt.webview.WebContent, context: Optional[Any]
):

    if not isinstance(
        context,
        (aqt.reviewer.Reviewer, aqt.previewer.Previewer, aqt.clayout.CardLayout),
    ):
        return

    web_content.body += (
        '<script async src="https://youglish.com/public/emb/widget.js"></script>'
    )
    web_content.body += f'<script defer src="{addon_folder}/aglish.js"></script>'


if aqt.mw:
    addon_folder = "/_addons/" + aqt.mw.addonManager.addonFromModule(__name__)
    aqt.mw.addonManager.setWebExports(__name__, r".*js")
    anki.hooks.field_filter.append(youglish_filter)
    anki.hooks.card_did_render.append(on_card_did_render)
    aqt.gui_hooks.webview_will_set_content.append(on_webview_will_set_content)