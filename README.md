<div align="center">

<br/>

```
███╗   ██╗ ██████╗ ██╗   ██╗ █████╗
████╗  ██║██╔═══██╗██║   ██║██╔══██╗
██╔██╗ ██║██║   ██║██║   ██║███████║
██║╚██╗██║██║   ██║╚██╗ ██╔╝██╔══██║
██║ ╚████║╚██████╔╝ ╚████╔╝ ██║  ██║
╚═╝  ╚═══╝ ╚═════╝   ╚═══╝  ╚═╝  ╚═╝
```

### A fully functional web browser — built from scratch in Python.

<br/>

![Python](https://img.shields.io/badge/Python-3.8+-6c63ff?style=for-the-badge&logo=python&logoColor=white)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-a78bfa?style=for-the-badge&logo=qt&logoColor=white)
![Chromium](https://img.shields.io/badge/Engine-Chromium-5dcaa5?style=for-the-badge&logo=googlechrome&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-ff6b6b?style=for-the-badge)

<br/>

![Nova Browser Screenshot](https://raw.githubusercontent.com/Mr-Farooqi/NovaBrowser/refs/heads/main/img/screenshot-home.png)

<br/>

</div>

---

## ✦ What is Nova?

**Nova** is a lightweight, dark-themed desktop web browser built entirely in Python using **PyQt5** and the **Chromium-powered QtWebEngine**. It loads real websites, supports multiple tabs, smart search, keyboard shortcuts, and features a polished custom UI — all in ~250 lines of Python.

> Built as a side project to explore what Python can do beyond scripts and data science.

---

## ⚡ Features

| Feature | Description |
|---|---|
| 🌐 **Real Websites** | Powered by Chromium — loads any site just like a real browser |
| 📑 **Multi-Tab** | Open, close, and switch tabs with ease |
| 🔍 **Smart Search** | Type a URL → opens it. Type anything else → Google search |
| 🌙 **Dark Theme** | Custom deep dark UI with purple accents |
| ⌨️ **Keyboard Shortcuts** | Full shortcut support (see below) |
| 📊 **Progress Bar** | Live page load indicator |
| 🏠 **Home Page** | Custom new tab page with quick links |
| 🔖 **Favicon Icons** | Site-aware icons in address bar |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/nova-browser.git
cd nova-browser
```

**2. Install dependencies**
```bash
pip install PyQt5 PyQtWebEngine
```

**3. Run the browser**
```bash
python nova_browser.py
```

That's it. No config files, no build steps, no nonsense.

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl + T` | Open new tab |
| `Ctrl + W` | Close current tab |
| `Ctrl + L` | Focus address bar |
| `Ctrl + R` | Reload page |
| `Alt + ←` | Go back |
| `Alt + →` | Go forward |
| `Escape` | Unfocus address bar |

---

## 🗂️ Project Structure

```
nova-browser/
│
├── nova_browser.py       # Main application — all browser logic
└── README.md             # You are here
```

---

## 🧠 How It Works

Nova uses **PyQt5** for the UI and **QtWebEngineWidgets** which wraps the Chromium browser engine. Here's the core concept:

```python
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

# Create a web view — Chromium under the hood
web = QWebEngineView()

# Navigate to any URL
web.setUrl(QUrl("https://www.google.com"))
```

The `NovaBrowser` class extends `QMainWindow` and wires together:
- A custom toolbar with nav buttons + address bar
- A `QTabWidget` for multi-tab support
- Individual `BrowserTab` widgets, each containing a `QWebEngineView`
- Signal/slot connections for URL changes, title updates, and load progress

---

## 📸 Screenshots

<div align="center">

| Home Page | Browsing |
|---|---|
| ![Home](https://raw.githubusercontent.com/Mr-Farooqi/NovaBrowser/refs/heads/main/img/screenshot-home.png) | ![Browser](https://raw.githubusercontent.com/Mr-Farooqi/NovaBrowser/refs/heads/main/img/screenshot-browse.png) |

</div>

> 💡 **Tip:** Replace the placeholder images above with real screenshots of your browser!

---

## 🛠️ Built With

- [Python](https://www.python.org/) — Core language
- [PyQt5](https://pypi.org/project/PyQt5/) — GUI framework
- [PyQtWebEngine](https://pypi.org/project/PyQtWebEngine/) — Chromium-based web engine

---

## 🤝 Contributing

Contributions are welcome! Here are some ideas for features to add:

- [ ] Bookmarks manager
- [ ] Browsing history
- [ ] Download manager
- [ ] Incognito / private mode
- [ ] Custom themes / theme switcher
- [ ] Extensions support

Feel free to open an issue or submit a pull request.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

<br/>

**Built with Python 🐍 & curiosity.**

*If you found this useful, drop a ⭐ — it means a lot!*

<br/>

</div>
