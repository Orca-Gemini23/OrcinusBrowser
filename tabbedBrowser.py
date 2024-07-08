from modulesNeeded import *


# for multiple browser support !!
class BrowserTab(QTabWidget):
    def __init__(self):
        super().__init__()

        self.setDocumentMode(True)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_current_tab)
        self.currentChanged.connect(self.current_tab_changed)

        self.new_tab(QUrl('https://google.com'), 'Homepage')

    def new_tab(self, qurl=None, label="Blank"):
        if qurl is None:
            qurl = QUrl('')

        browser = QWebEngineView()
        browser.setUrl(qurl)

        i = self.addTab(browser, label)
        self.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_urlbar(qurl, browser))
        browser.loadFinished.connect(lambda _, i=i, browser=browser: self.tab_label(i, browser))

    def close_current_tab(self, i):
        if self.count() < 2:
            return

        self.removeTab(i)

    def current_tab_changed(self, i):
        qurl = self.currentWidget().url()
        self.update_urlbar(qurl, self.currentWidget())

    def tab_label(self, i, browser):
        self.setTabText(i, browser.page().title())

    def update_urlbar(self, qurl, browser=None):
        if browser != self.currentWidget():
            return

        self.parent().url_bar.setText(qurl.toString())
        self.parent().url_bar.setCursorPosition(0)
