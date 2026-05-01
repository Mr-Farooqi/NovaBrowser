import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLineEdit, QPushButton, QTabWidget,
    QTabBar, QStatusBar, QProgressBar, QLabel,
    QShortcut, QSizePolicy, QFrame
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt, pyqtSignal
from PyQt5.QtGui import QKeySequence, QColor, QPalette


# ─── Theme (matches screenshot) ───────────────────────────────────────────────
STYLE = """
* { font-family: 'Segoe UI', 'SF Pro Display', sans-serif; }

QMainWindow, QWidget#central {
    background-color: #1a1a2e;
}

/* ── Toolbar ── */
QWidget#toolbar {
    background-color: #1e1e30;
    border-bottom: 1px solid #2a2a3f;
}

/* ── URL Bar ── */
QLineEdit#url_bar {
    background-color: #252538;
    color: #d0d0e8;
    border: 1px solid #35354f;
    border-radius: 6px;
    padding: 6px 14px 6px 32px;
    font-size: 13px;
    selection-background-color: #6c63ff;
}
QLineEdit#url_bar:focus {
    border: 1px solid #6c63ff;
    background-color: #2a2a40;
}

/* ── Nav Buttons (back/fwd/refresh/home) ── */
QPushButton#nav_btn {
    background-color: transparent;
    color: #8888aa;
    border: none;
    border-radius: 6px;
    font-size: 16px;
    min-width: 30px;
    max-width: 30px;
    min-height: 30px;
    max-height: 30px;
    padding: 0px;
}
QPushButton#nav_btn:hover {
    background-color: #28283c;
    color: #c0c0d8;
}
QPushButton#nav_btn:pressed {
    background-color: #35354f;
}
QPushButton#nav_btn:disabled {
    color: #3a3a52;
}

/* ── Go Button ── */
QPushButton#go_btn {
    background-color: #6c63ff;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 600;
    padding: 6px 16px;
    min-height: 30px;
    min-width: 44px;
}
QPushButton#go_btn:hover {
    background-color: #7c73ff;
}
QPushButton#go_btn:pressed {
    background-color: #5a52e0;
}

/* ── Icon Buttons (bookmark, menu) ── */
QPushButton#icon_btn {
    background-color: transparent;
    color: #8888aa;
    border: none;
    border-radius: 6px;
    font-size: 15px;
    min-width: 30px;
    max-width: 30px;
    min-height: 30px;
    max-height: 30px;
    padding: 0px;
}
QPushButton#icon_btn:hover {
    background-color: #28283c;
    color: #c0c0d8;
}

/* ── Tabs ── */
QTabWidget::pane {
    border: none;
    background: #1a1a2e;
}
QTabBar {
    background: #1e1e30;
}
QTabBar::tab {
    background: #252538;
    color: #7070a0;
    padding: 8px 14px;
    border: none;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    min-width: 120px;
    max-width: 200px;
    font-size: 12px;
    margin-right: 2px;
    margin-top: 4px;
}
QTabBar::tab:selected {
    background: #1e1e30;
    color: #e0e0f5;
    border-bottom: none;
}
QTabBar::tab:hover:!selected {
    background: #28283c;
    color: #a0a0c0;
}
QTabBar::close-button {
    subcontrol-position: right;
    padding: 2px;
}

/* ── New Tab Button ── */
QPushButton#new_tab_btn {
    background-color: transparent;
    color: #8888aa;
    border: 1px solid #35354f;
    border-radius: 6px;
    font-size: 16px;
    font-weight: bold;
    min-width: 28px;
    max-width: 28px;
    min-height: 28px;
    max-height: 28px;
    padding: 0px;
    margin-top: 6px;
    margin-right: 8px;
}
QPushButton#new_tab_btn:hover {
    background-color: #28283c;
    color: #c0c0d8;
}

/* ── Progress Bar ── */
QProgressBar#progress {
    background: transparent;
    border: none;
    border-radius: 1px;
    max-height: 2px;
}
QProgressBar#progress::chunk {
    background: #6c63ff;
    border-radius: 1px;
}

/* ── Status Bar ── */
QStatusBar {
    background: #1e1e30;
    color: #55557a;
    font-size: 11px;
    border-top: 1px solid #2a2a3f;
    padding-left: 8px;
}

/* ── Lock icon label ── */
QLabel#lock_icon {
    font-size: 13px;
    color: #7070a0;
    padding: 0 4px;
}
"""

HOME_HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: #1a1a2e;
    color: #e2e2f0;
    font-family: 'Segoe UI', sans-serif;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0;
    user-select: none;
  }
  .logo-wrap {
    display: flex; flex-direction: column; align-items: center; gap: 8px;
    margin-bottom: 32px;
  }
  .logo-icon {
    width: 72px; height: 72px;
    background: linear-gradient(135deg, #4a3fcc 0%, #7c5cfc 50%, #a78bfa 100%);
    border-radius: 20px;
    display: flex; align-items: center; justify-content: center;
    font-size: 32px;
    box-shadow: 0 8px 32px rgba(108,99,255,0.4);
    margin-bottom: 4px;
    position: relative;
    overflow: hidden;
  }
  .logo-icon::after {
    content: '';
    position: absolute;
    top: -30%; left: 15%;
    width: 30%; height: 55%;
    background: rgba(255,255,255,0.18);
    border-radius: 50%;
    transform: rotate(-20deg);
  }
  .logo-letter {
    font-size: 36px; font-weight: 700; color: white;
    text-shadow: 0 2px 8px rgba(0,0,0,0.3);
    font-family: 'Segoe UI', sans-serif;
    z-index:1;
  }
  .logo-dot {
    width: 8px; height: 8px;
    background: #fff;
    border-radius: 50%;
    position: absolute;
    top: 12px; right: 16px;
    opacity: 0.9;
    z-index:2;
  }
  h1 {
    font-size: 1.6rem; font-weight: 700;
    letter-spacing: 6px; color: #e2e2f0;
    text-transform: uppercase;
  }
  .tagline { color: #55557a; font-size: 11px; letter-spacing: 4px; text-transform: uppercase; margin-top: 2px; }

  .search-bar {
    width: 420px; max-width: 90vw;
    background: #252538;
    border: 1px solid #35354f;
    border-radius: 10px;
    display: flex; align-items: center;
    padding: 4px 6px 4px 14px;
    gap: 8px;
    margin-bottom: 28px;
  }
  .search-bar:focus-within { border-color: #6c63ff; }
  .search-icon { color: #55557a; font-size: 14px; }
  .search-bar input {
    flex: 1; background: none; border: none; outline: none;
    color: #d0d0e8; font-size: 14px; padding: 8px 0;
  }
  .search-bar input::placeholder { color: #55557a; }
  .search-bar button {
    background: #6c63ff; border: none; border-radius: 8px;
    color: white; padding: 8px 20px; font-size: 13px; font-weight: 600;
    cursor: pointer; transition: background 0.2s;
  }
  .search-bar button:hover { background: #7c73ff; }

  .quick-links {
    display: flex; gap: 10px; flex-wrap: wrap; justify-content: center;
    max-width: 520px;
  }
  .chip {
    background: #252538;
    border: 1px solid #2e2e48;
    border-radius: 12px;
    padding: 12px 18px;
    font-size: 12px; color: #9090b8;
    cursor: pointer; text-decoration: none;
    transition: all 0.2s;
    display: flex; flex-direction: column; align-items: center; gap: 6px;
    min-width: 80px;
  }
  .chip:hover {
    background: #2e2e48; color: #c8c8e8;
    border-color: #6c63ff; transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(108,99,255,0.2);
  }
  .chip-icon {
    width: 38px; height: 38px; border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px; background: #1e1e30;
  }
  .chip-label { font-size: 11px; color: #8888aa; }

  /* Real favicon images */
  .chip-img { width: 38px; height: 38px; border-radius: 10px; object-fit: contain; background: #fff; }

  .add-chip {
    background: #252538;
    border: 1px dashed #35354f;
    border-radius: 12px;
    padding: 12px 18px;
    font-size: 20px; color: #55557a;
    cursor: pointer;
    transition: all 0.2s;
    display: flex; flex-direction: column; align-items: center; gap: 6px;
    min-width: 80px;
  }
  .add-chip:hover { background: #2e2e48; color: #c0c0d8; border-color: #6c63ff; }
  .add-chip .chip-label { font-size: 11px; color: #55557a; }
</style>
</head>
<body>
  <div class="logo-wrap">
    <div class="logo-icon">
      <span class="logo-letter">N</span>
      <span class="logo-dot"></span>
    </div>
    <h1>Nova</h1>
    <p class="tagline">Browser</p>
  </div>

  <div class="search-bar">
    <span class="search-icon">🔍</span>
    <input type="text" id="q" placeholder="Search the web..." autofocus
      onkeydown="if(event.key==='Enter') go()">
    <button onclick="go()">Search</button>
  </div>

  <div class="quick-links">
    <a class="chip" href="https://www.youtube.com">
      <img class="chip-img" src="https://www.youtube.com/favicon.ico" onerror="this.style.display='none';this.nextSibling.style.display='flex'" alt="">
      <div class="chip-icon" style="display:none">▶</div>
      <span class="chip-label">YouTube</span>
    </a>
    <a class="chip" href="https://github.com">
      <img class="chip-img" src="https://github.com/favicon.ico" onerror="this.style.display='none';this.nextSibling.style.display='flex'" alt="">
      <div class="chip-icon" style="display:none">💻</div>
      <span class="chip-label">GitHub</span>
    </a>
    <a class="chip" href="https://www.linkedin.com">
      <img class="chip-img" src="https://www.linkedin.com/favicon.ico" onerror="this.style.display='none';this.nextSibling.style.display='flex'" alt="">
      <div class="chip-icon" style="display:none">💼</div>
      <span class="chip-label">LinkedIn</span>
    </a>
    <a class="chip" href="https://www.twitter.com">
      <img class="chip-img" src="https://twitter.com/favicon.ico" onerror="this.style.display='none';this.nextSibling.style.display='flex'" alt="">
      <div class="chip-icon" style="display:none">🐦</div>
      <span class="chip-label">Twitter</span>
    </a>
    <a class="chip" href="https://stackoverflow.com">
      <img class="chip-img" src="https://stackoverflow.com/favicon.ico" onerror="this.style.display='none';this.nextSibling.style.display='flex'" alt="">
      <div class="chip-icon" style="display:none">📚</div>
      <span class="chip-label">Stack Overflow</span>
    </a>
    <a class="add-chip" href="#">
      <span>+</span>
      <span class="chip-label">Add</span>
    </a>
  </div>

  <script>
    function go() {
      const q = document.getElementById('q').value.trim();
      if (!q) return;
      if (q.startsWith('http') || (q.includes('.') && !q.includes(' ')))
        window.location.href = q.startsWith('http') ? q : 'https://' + q;
      else
        window.location.href = 'https://www.google.com/search?q=' + encodeURIComponent(q);
    }
    document.getElementById('q').focus();
  </script>
</body>
</html>"""


# ─── Browser Tab ──────────────────────────────────────────────────────────────
class BrowserTab(QWidget):
    url_changed = pyqtSignal(str)
    title_changed = pyqtSignal(str)
    load_progress = pyqtSignal(int)
    load_finished = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.web = QWebEngineView()
        self.web.setHtml(HOME_HTML, QUrl("about:blank"))
        layout.addWidget(self.web)

        self.web.loadProgress.connect(self.load_progress)
        self.web.loadFinished.connect(self.load_finished)
        self.web.urlChanged.connect(lambda u: self.url_changed.emit(u.toString()))
        self.web.titleChanged.connect(self.title_changed)

    def navigate(self, text):
        text = text.strip()
        if not text:
            return
        if text.startswith(("http://", "https://")):
            url = QUrl(text)
        elif "." in text and " " not in text:
            url = QUrl("https://" + text)
        else:
            url = QUrl("https://www.google.com/search?q=" + text.replace(" ", "+"))
        self.web.setUrl(url)

    def current_url(self):
        return self.web.url().toString()

    def current_title(self):
        return self.web.title()


# ─── Main Window ──────────────────────────────────────────────────────────────
class NovaBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nova Browser")
        self.resize(900, 640)
        self.setMinimumSize(700, 450)
        self.setStyleSheet(STYLE)

        central = QWidget()
        central.setObjectName("central")
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Tab Bar + New Tab Button Row ──────────────────────────────────────
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.setDocumentMode(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.on_tab_changed)

        # New tab button in corner
        self.btn_new_tab = QPushButton("+")
        self.btn_new_tab.setObjectName("new_tab_btn")
        self.btn_new_tab.setCursor(Qt.PointingHandCursor)
        self.btn_new_tab.setToolTip("New Tab  (Ctrl+T)")
        self.tabs.setCornerWidget(self.btn_new_tab, Qt.TopRightCorner)

        root.addWidget(self.tabs, stretch=1)

        # ── Toolbar ───────────────────────────────────────────────────────────
        # Insert toolbar BEFORE tabs — we need to reorder
        # Actually build it first, insert at position 0
        toolbar = QWidget()
        toolbar.setObjectName("toolbar")
        toolbar.setFixedHeight(52)
        tb = QHBoxLayout(toolbar)
        tb.setContentsMargins(10, 8, 10, 8)
        tb.setSpacing(4)

        def nav_btn(icon_text, tip=""):
            b = QPushButton(icon_text)
            b.setObjectName("nav_btn")
            b.setCursor(Qt.PointingHandCursor)
            if tip:
                b.setToolTip(tip)
            return b

        self.btn_back    = nav_btn("←", "Back (Alt+Left)")
        self.btn_fwd     = nav_btn("→", "Forward (Alt+Right)")
        self.btn_refresh = nav_btn("↻", "Reload (Ctrl+R)")
        self.btn_home    = nav_btn("⌂", "Home")

        tb.addWidget(self.btn_back)
        tb.addWidget(self.btn_fwd)
        tb.addWidget(self.btn_refresh)
        tb.addWidget(self.btn_home)
        tb.addSpacing(6)

        # URL bar wrapper (lock icon inside)
        url_container = QWidget()
        url_layout = QHBoxLayout(url_container)
        url_layout.setContentsMargins(0, 0, 0, 0)
        url_layout.setSpacing(0)

        self.lock_label = QLabel("🔒")
        self.lock_label.setObjectName("lock_icon")
        self.lock_label.setFixedWidth(26)

        self.url_bar = QLineEdit()
        self.url_bar.setObjectName("url_bar")
        self.url_bar.setPlaceholderText("Search Google or type a URL")
        self.url_bar.setClearButtonEnabled(True)

        # Stack lock inside url_bar via padding — simpler: just put them side by side in a frame
        url_frame = QFrame()
        url_frame.setStyleSheet("""
            QFrame {
                background: #252538;
                border: 1px solid #35354f;
                border-radius: 6px;
            }
            QFrame:focus-within {
                border-color: #6c63ff;
            }
        """)
        url_frame_layout = QHBoxLayout(url_frame)
        url_frame_layout.setContentsMargins(8, 0, 4, 0)
        url_frame_layout.setSpacing(4)

        lock_lbl = QLabel("🔒")
        lock_lbl.setStyleSheet("font-size:12px; color:#55557a; background:transparent; border:none;")
        lock_lbl.setFixedWidth(20)
        self.lock_label = lock_lbl

        self.url_bar = QLineEdit()
        self.url_bar.setStyleSheet("""
            QLineEdit {
                background: transparent;
                color: #d0d0e8;
                border: none;
                padding: 6px 4px;
                font-size: 13px;
                selection-background-color: #6c63ff;
            }
        """)
        self.url_bar.setPlaceholderText("Search Google or type a URL")
        self.url_bar.setClearButtonEnabled(True)

        url_frame_layout.addWidget(lock_lbl)
        url_frame_layout.addWidget(self.url_bar)

        tb.addWidget(url_frame, stretch=1)
        tb.addSpacing(6)

        self.go_btn = QPushButton("Go")
        self.go_btn.setObjectName("go_btn")
        self.go_btn.setCursor(Qt.PointingHandCursor)
        tb.addWidget(self.go_btn)

        tb.addSpacing(4)

        # Bookmark star button
        self.btn_bookmark = QPushButton("☆")
        self.btn_bookmark.setObjectName("icon_btn")
        self.btn_bookmark.setCursor(Qt.PointingHandCursor)
        self.btn_bookmark.setToolTip("Bookmark")
        tb.addWidget(self.btn_bookmark)

        # Menu / settings button
        self.btn_menu = QPushButton("⋮")
        self.btn_menu.setObjectName("icon_btn")
        self.btn_menu.setCursor(Qt.PointingHandCursor)
        self.btn_menu.setToolTip("Settings")
        tb.addWidget(self.btn_menu)

        # Insert toolbar before tabs widget
        root.insertWidget(0, toolbar)

        # ── Progress ─────────────────────────────────────────────────────────
        self.progress = QProgressBar()
        self.progress.setObjectName("progress")
        self.progress.setFixedHeight(2)
        self.progress.setTextVisible(False)
        self.progress.setValue(0)
        root.insertWidget(1, self.progress)

        # ── Status Bar ───────────────────────────────────────────────────────
        self.status = QStatusBar()
        self.status.setFixedHeight(22)
        self.setStatusBar(self.status)
        # Add "Ready" left and "100%" right
        self.status_left = QLabel("Ready")
        self.status_right = QLabel("100%")
        self.status_right.setStyleSheet("color: #55557a; font-size: 11px; padding-right: 8px;")
        self.status.addWidget(self.status_left)
        self.status.addPermanentWidget(self.status_right)

        # ── Signals ──────────────────────────────────────────────────────────
        self.btn_back.clicked.connect(self.go_back)
        self.btn_fwd.clicked.connect(self.go_forward)
        self.btn_refresh.clicked.connect(self.go_refresh)
        self.btn_home.clicked.connect(self.go_home)
        self.btn_new_tab.clicked.connect(self.add_tab)
        self.go_btn.clicked.connect(self.navigate)
        self.url_bar.returnPressed.connect(self.navigate)
        self.btn_bookmark.clicked.connect(self.toggle_bookmark)

        # ── Shortcuts ────────────────────────────────────────────────────────
        QShortcut(QKeySequence("Ctrl+T"), self, self.add_tab)
        QShortcut(QKeySequence("Ctrl+W"), self, self.close_current_tab)
        QShortcut(QKeySequence("Ctrl+L"), self, lambda: (self.url_bar.setFocus(), self.url_bar.selectAll()))
        QShortcut(QKeySequence("Ctrl+R"), self, self.go_refresh)
        QShortcut(QKeySequence("Alt+Left"), self, self.go_back)
        QShortcut(QKeySequence("Alt+Right"), self, self.go_forward)
        QShortcut(QKeySequence("Escape"), self, lambda: self.url_bar.clearFocus())

        # ── First Tab ────────────────────────────────────────────────────────
        self.add_tab()
        self.update_nav_buttons()

    # ── Helpers ───────────────────────────────────────────────────────────────
    def current_tab(self) -> BrowserTab:
        return self.tabs.currentWidget()

    def add_tab(self, url=None):
        tab = BrowserTab()
        tab.url_changed.connect(lambda u, t=tab: self._on_url_changed(t, u))
        tab.title_changed.connect(lambda title, t=tab: self._on_title_changed(t, title))
        tab.load_progress.connect(self._on_load_progress)
        tab.load_finished.connect(self._on_load_finished)

        idx = self.tabs.addTab(tab, "  New Tab  ")
        self.tabs.setCurrentIndex(idx)

        if url:
            tab.navigate(url)
        else:
            self.url_bar.clear()
            self.url_bar.setFocus()

        self.update_nav_buttons()

    def close_tab(self, idx):
        if self.tabs.count() > 1:
            self.tabs.removeTab(idx)
        else:
            self.close()

    def close_current_tab(self):
        self.close_tab(self.tabs.currentIndex())

    def on_tab_changed(self, idx):
        tab = self.tabs.widget(idx)
        if not tab:
            return
        url = tab.current_url()
        self.url_bar.setText("" if url in ("about:blank", "") else url)
        self._update_lock(url)
        title = tab.current_title() or "Nova Browser"
        self.setWindowTitle(f"{title} — Nova" if title else "Nova Browser")
        self.update_nav_buttons()

    def update_nav_buttons(self):
        tab = self.current_tab()
        if tab:
            self.btn_back.setEnabled(tab.web.history().canGoBack())
            self.btn_fwd.setEnabled(tab.web.history().canGoForward())

    def toggle_bookmark(self):
        if self.btn_bookmark.text() == "☆":
            self.btn_bookmark.setText("★")
            self.btn_bookmark.setStyleSheet("QPushButton#icon_btn { color: #f0c040; }")
        else:
            self.btn_bookmark.setText("☆")
            self.btn_bookmark.setStyleSheet("")

    # ── Tab event handlers ───────────────────────────────────────────────────
    def _on_url_changed(self, tab, url):
        idx = self.tabs.indexOf(tab)
        if idx == self.tabs.currentIndex():
            self.url_bar.setText("" if url in ("about:blank", "") else url)
            self._update_lock(url)
            # Reset bookmark star on navigation
            self.btn_bookmark.setText("☆")
            self.btn_bookmark.setStyleSheet("")
        self.update_nav_buttons()

    def _update_lock(self, url):
        if url.startswith("https://"):
            self.lock_label.setText("🔒")
            self.lock_label.setStyleSheet("font-size:12px; color:#5aba8a; background:transparent; border:none;")
        elif url.startswith("http://"):
            self.lock_label.setText("⚠")
            self.lock_label.setStyleSheet("font-size:12px; color:#e0a040; background:transparent; border:none;")
        else:
            self.lock_label.setText("🔒")
            self.lock_label.setStyleSheet("font-size:12px; color:#55557a; background:transparent; border:none;")

    def _on_title_changed(self, tab, title):
        idx = self.tabs.indexOf(tab)
        short = (title[:16] + "…") if len(title) > 18 else title or "New Tab"
        self.tabs.setTabText(idx, f"  {short}  ")
        if idx == self.tabs.currentIndex():
            self.setWindowTitle(f"{title} — Nova" if title else "Nova Browser")

    def _on_load_progress(self, p):
        self.progress.setValue(p if p < 100 else 0)
        self.status_right.setText(f"{p}%")

    def _on_load_finished(self, ok):
        self.progress.setValue(0)
        self.status_right.setText("100%")
        msg = "Ready" if ok else "✗  Failed to load"
        self.status_left.setText(msg)
        self.update_nav_buttons()

    # ── Navigation ────────────────────────────────────────────────────────────
    def navigate(self):
        self.current_tab().navigate(self.url_bar.text())
        self.url_bar.clearFocus()

    def go_back(self):
        self.current_tab().web.back()

    def go_forward(self):
        self.current_tab().web.forward()

    def go_refresh(self):
        tab = self.current_tab()
        if tab.web.url().isEmpty() or tab.web.url() == QUrl("about:blank"):
            return
        tab.web.reload()

    def go_home(self):
        self.current_tab().web.setHtml(HOME_HTML, QUrl("about:blank"))
        self.url_bar.clear()
        self._update_lock("")


# ─── Entry ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import os
    os.environ.setdefault("QTWEBENGINE_CHROMIUM_FLAGS", "--disable-logging")

    app = QApplication(sys.argv)
    app.setApplicationName("Nova Browser")
    app.setStyle("Fusion")

    dark = QPalette()
    dark.setColor(QPalette.Window,          QColor("#1a1a2e"))
    dark.setColor(QPalette.WindowText,      QColor("#e2e2f0"))
    dark.setColor(QPalette.Base,            QColor("#252538"))
    dark.setColor(QPalette.Text,            QColor("#d0d0e8"))
    dark.setColor(QPalette.Button,          QColor("#1e1e30"))
    dark.setColor(QPalette.ButtonText,      QColor("#e2e2f0"))
    dark.setColor(QPalette.Highlight,       QColor("#6c63ff"))
    dark.setColor(QPalette.HighlightedText, QColor("#ffffff"))
    app.setPalette(dark)

    window = NovaBrowser()
    window.show()
    sys.exit(app.exec_())
