from tabbedBrowser import BrowserTab
from modulesNeeded import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Creating browser
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('https://google.com'))
        self.setCentralWidget(self.browser)

        # Enable JavaScript
        self.browser.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)

        self.showMaximized()

        # Status Bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # To make the nav bar:
        navbar = QToolBar()
        self.addToolBar(navbar)

        back_btn = QAction('Back', self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        forward_btn = QAction('Forward', self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        reload_btn = QAction('Reload', self)
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        home_btn = QAction('Home', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        self.browser.urlChanged.connect(self.update_url)
        self.browser.loadFinished.connect(self.update_status)

    def navigate_home(self):
        self.browser.setUrl(QUrl('https://google.com'))

    def navigate_to_url(self):
        url = self.url_bar.text().strip()
        if not self.is_valid_url(url):
            self.status.showMessage("Invalid URL", 2000)
            return

        # Add http:// if no scheme is provided
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            url = 'http://' + url

        self.browser.setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())

    def update_status(self, status):
        if status:
            self.status.showMessage("Page loaded successfully", 2000)
        else:
            self.status.showMessage("Failed to load page", 2000)

    def is_valid_url(self, url):
        # Basic URL validation using regex
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        if re.match(regex, url) is not None:
            return True

        # Check if it's a valid domain by resolving it
        try:
            host = urlparse(url).netloc or urlparse('http://' + url).netloc
            socket.gethostbyname(host)
            return True
        except socket.error:
            return False

    def construct_url(self, text):
        # If text does not have a scheme and is not a full domain, assume it is a domain name
        try:
            # Check if the text can be resolved as a hostname
            socket.gethostbyname(text)
            return 'http://' + text
        except socket.error:
            # If not, assume it's a shorthand for a .com domain
            return 'http://' + text + '.com'


app = QApplication(sys.argv)
QApplication.setApplicationName('Orcinus-Browser')
window = MainWindow()
app.exec_()
