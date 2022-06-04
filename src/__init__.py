import json
from typing import Any, Optional

import anki
import aqt
from anki.cards import Card
from aqt import gui_hooks
from aqt.clayout import CardLayout
from aqt.previewer import Previewer
from aqt.qt import *
from aqt.qt import QUrl, qtmajor
from aqt.reviewer import Reviewer
from aqt.webview import WebContent

from .filter import YouGlishFilter
from .youglish_login import YouGlishLoginDialog

if qtmajor > 5:
    from PyQt6.QtNetwork import QNetworkCookie
else:
    from PyQt5.QtNetwork import QNetworkCookie  # type: ignore


def youglish_filter(
    field_text: str,
    field_name: str,
    filter_name: str,
    context: anki.template.TemplateRenderContext,
) -> str:
    current_id = context.extra_state.get("aglish_id", 0)

    try:
        youglish = YouGlishFilter(current_id, filter_name, field_text, context)
    except:
        return field_text

    context.extra_state["aglish_id"] = current_id + 1

    return youglish.text


def on_card_will_show(text: str, card: Card, kind: str) -> str:
    return text + "<script>YGParsePageDelayed(); playNonDelayedYGWidgets()</script>"


def on_webview_will_set_content(
    web_content: WebContent, context: Optional[Any]
) -> None:

    if not isinstance(
        context,
        (Reviewer, Previewer, CardLayout),
    ):
        return

    config = context.mw.addonManager.getConfig(__name__)

    web_content.body += (
        '<script async src="https://youglish.com/public/emb/widget.js"></script>'
    )
    web_content.body += f'<script defer src="{addon_folder}/aglish.js"></script>'

    hotkey = json.dumps(config["hotkey"])
    web_content.body += f"<script>window.aglishHotkey = {hotkey};</script>"

    # Experimental support for YouGlish login - not tested
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


def add_aglish_menu() -> None:
    def on_login_clicked() -> None:
        page = YouGlishLoginDialog(aqt.mw)
        page.exec()
        if hasattr(page.web, "cleanup"):
            # Avoid leaking memory - works on Anki 2.1.50+
            page.web.cleanup()

    menu = QMenu("Aglish", aqt.mw)
    login_action = QAction("Log in to YouGlish", menu)
    qconnect(login_action.triggered, on_login_clicked)
    menu.addAction(login_action)
    aqt.mw.form.menuTools.addMenu(menu)


if aqt.mw:
    addon_folder = "/_addons/" + aqt.mw.addonManager.addonFromModule(__name__)
    aqt.mw.addonManager.setWebExports(__name__, r".*js")
    anki.hooks.field_filter.append(youglish_filter)
    gui_hooks.card_will_show.append(on_card_will_show)
    aqt.gui_hooks.webview_will_set_content.append(on_webview_will_set_content)
    add_aglish_menu()
