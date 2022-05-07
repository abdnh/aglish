import re
from typing import Any, Optional

import anki
import aqt
from anki.cards import Card
from aqt import gui_hooks
from aqt.clayout import CardLayout
from aqt.previewer import Previewer
from aqt.qt import QUrl, qtmajor
from aqt.reviewer import Reviewer
from aqt.webview import WebContent

if qtmajor > 5:
    from PyQt6.QtNetwork import QNetworkCookie
else:
    from PyQt5.QtNetwork import QNetworkCookie


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
        for config in map(lambda c: c.split("="), filter_name.split()[1:]):
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


CURRENT_ID = 0


def youglish_filter(
    field_text: str,
    field_name: str,
    filter_name: str,
    context: anki.template.TemplateRenderContext,
) -> str:

    global CURRENT_ID

    try:
        youglish = YouGlishFilter(CURRENT_ID, filter_name, field_text, context)
    except:
        return field_text

    CURRENT_ID += 1

    return youglish.text


def on_card_will_show(text: str, card: Card, kind: str) -> str:
    global CURRENT_ID
    CURRENT_ID = 0
    return text + "<script>YGParsePageDelayed(); playNonDelayedYGWidgets()</script>"


def on_webview_will_set_content(web_content: WebContent, context: Optional[Any]):

    if not isinstance(
        context,
        (Reviewer, Previewer, CardLayout),
    ):
        return

    web_content.body += (
        '<script async src="https://youglish.com/public/emb/widget.js"></script>'
    )
    web_content.body += f'<script defer src="{addon_folder}/aglish.js"></script>'

    # Experimental support for YouGlish login - not tested
    config = context.mw.addonManager.getConfig(__name__)
    cookies = config.get("cookies", {})
    if isinstance(context, Previewer):
        web = context._web  # pylint: disable=protected-access
    elif isinstance(context, CardLayout):
        web = context.preview_web
    else:
        web = context.web
    cookie_store = web.page().profile().cookieStore()
    for name, value in cookies.items():
        if value:
            cookie = QNetworkCookie(name.encode(), value.encode())
            cookie_store.setCookie(cookie, QUrl("https://youglish.com/"))


if aqt.mw:
    addon_folder = "/_addons/" + aqt.mw.addonManager.addonFromModule(__name__)
    aqt.mw.addonManager.setWebExports(__name__, r".*js")
    anki.hooks.field_filter.append(youglish_filter)
    gui_hooks.card_will_show.append(on_card_will_show)
    aqt.gui_hooks.webview_will_set_content.append(on_webview_will_set_content)
