from typing import Dict, cast

from aqt.main import AnkiQt
from aqt.qt import *
from aqt.utils import showInfo
from aqt.webview import AnkiWebView

if qtmajor > 5:
    from PyQt6.QtNetwork import QNetworkCookie
else:
    from PyQt5.QtNetwork import QNetworkCookie  # type: ignore


class YouGlishLoginDialog(QDialog):
    """This dialog allows the user to log in to their YouGlish account via a webview to use their paid subscription with the widget. Not tested."""

    def __init__(self, mw: AnkiQt):
        super().__init__(mw)
        self.mw = mw
        self.config = self.mw.addonManager.getConfig(__name__)
        self.youglish_cookies: Dict[str, str] = {}
        self.setWindowTitle("YouGlish Login")
        # pylint: disable=no-member
        self.setWindowFlags(
            cast(
                Qt.WindowType,
                self.windowFlags() | Qt.WindowType.WindowContextHelpButtonHint,
            )
        )
        vbox = QVBoxLayout()
        self.web = AnkiWebView(self, title="Log in to YouGlish")
        vbox.addWidget(self.web)
        self.web.set_open_links_externally(False)
        self.restore_cookies()
        self.web.load(QUrl("https://youglish.com/login"))
        self.web.setZoomFactor(1)
        # pylint: disable=no-member
        self.web.settings().setAttribute(
            QWebEngineSettings.WebAttribute.AllowRunningInsecureContent,
            True,
        )
        self.setLayout(vbox)
        self.resize(800, 600)
        qconnect(
            self.web.page().profile().cookieStore().cookieAdded, self.on_cookie_added
        )

    def restore_cookies(self) -> None:
        cookie_store = self.web.page().profile().cookieStore()
        for name, value in self.config.get("cookies", {}).items():
            if value:
                cookie = QNetworkCookie(name.encode(), value.encode())
                cookie_store.setCookie(cookie, QUrl("https://youglish.com/"))

    def exec(self) -> int:
        if self.config.get("show_login_help", True):
            self.config["show_login_help"] = False
            self.mw.addonManager.writeConfig(__name__, self.config)
            self.show_help()
        return super().exec()

    def on_cookie_added(self, cookie: QNetworkCookie) -> None:
        name = bytes(cast(bytes, cookie.name())).decode("utf-8")
        value = bytes(cast(bytes, cookie.value())).decode("utf-8")
        domain = cookie.domain()
        if domain == "youglish.com":
            self.youglish_cookies[name] = value

    def closeEvent(self, event: QCloseEvent) -> None:  # pylint: disable=invalid-name
        if self.youglish_cookies:
            self.config["cookies"].update(self.youglish_cookies)
            self.mw.addonManager.writeConfig(__name__, self.config)
        return super().closeEvent(event)

    def event(self, event: QEvent) -> bool:
        # pylint: disable=no-member
        if event.type() == QEvent.Type.EnterWhatsThisMode:
            self.show_help()
        return super().event(event)

    def show_help(self) -> None:
        showInfo(
            """This dialog allows you to use your YouGlish credentials with the Aglish add-on. You only need to log in to YouGlish from their login page shown here and close the window. The add-on will then save your credentials and use them when showing the YouGlish widget on cards.<br>
                Logging in is mainly useful if you have a <a href='https://youglish.com/subscribe'>paid subscription</a> to increase the number of queries you can make per day.
                """,
            parent=self,
            title="Aglish Add-on",
            textFormat="rich",
        )
