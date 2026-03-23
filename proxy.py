# -*- coding: utf-8 -*-
import sys
import threading
import urllib.request
import json
import time
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel, QListWidget, QListWidgetItem
)
from PyQt5.QtNetwork import QNetworkProxy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

# COLORS
BG = "#0f1117"
CARD = "#1a1d27"
BORDER = "#2a2d3a"
ACCENT = "#00d4ff"
GREEN = "#00e676"
RED = "#ff5252"
YELLOW = "#ffd740"
TEXT = "#e8eaf6"

STYLE = f"""
QWidget {{ background: {BG}; color: {TEXT}; font-family: Consolas; }}
QPushButton {{ background: {CARD}; color: {ACCENT}; border: 1px solid {BORDER}; padding: 6px; }}
QPushButton:hover {{ background: {BORDER}; }}
QLineEdit {{ background: #0a0d14; border: 1px solid {BORDER}; padding: 6px; }}
QListWidget {{ background: #0a0d14; border: 1px solid {BORDER}; }}
"""


class ProxyTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Proxy Tool")
        self.resize(520, 420)
        self.setStyleSheet(STYLE)

        self.proxies = []
        self.active_proxy = ""

        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        title = QLabel("[ PROXY TOOL ]")
        title.setStyleSheet(f"color: {ACCENT}; font-size: 16px;")
        layout.addWidget(title)

        # INPUT
        row = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText("IP:PORT")
        row.addWidget(self.input)

        add_btn = QPushButton("ADD")
        add_btn.clicked.connect(self.add_proxy)
        row.addWidget(add_btn)

        layout.addLayout(row)

        # LIST
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        # BUTTONS
        btn_row = QHBoxLayout()

        use_btn = QPushButton("USE")
        use_btn.clicked.connect(self.use_proxy)
        btn_row.addWidget(use_btn)

        test_btn = QPushButton("TEST")
        test_btn.clicked.connect(self.test_proxy)
        btn_row.addWidget(test_btn)

        disable_btn = QPushButton("DISABLE")
        disable_btn.clicked.connect(self.disable_proxy)
        btn_row.addWidget(disable_btn)

        remove_btn = QPushButton("REMOVE")
        remove_btn.clicked.connect(self.remove_proxy)
        btn_row.addWidget(remove_btn)

        layout.addLayout(btn_row)

        # STATUS
        self.status = QLabel("No proxy active")
        layout.addWidget(self.status)

    def add_proxy(self):
        text = self.input.text().strip()
        if ":" not in text:
            return
        if text not in self.proxies:
            self.proxies.append(text)
            self.refresh()
        self.input.clear()

    def refresh(self):
        self.list_widget.clear()
        for p in self.proxies:
            item = QListWidgetItem(p)
            if p == self.active_proxy:
                item.setForeground(QColor(ACCENT))
                item.setText(p + "  (ACTIVE)")
            self.list_widget.addItem(item)

    def use_proxy(self):
        item = self.list_widget.currentItem()
        if not item:
            return

        proxy_str = item.text().split()[0]
        host, port = proxy_str.split(":")

        proxy = QNetworkProxy(QNetworkProxy.HttpProxy, host, int(port))
        QNetworkProxy.setApplicationProxy(proxy)

        self.active_proxy = proxy_str
        self.status.setText(f"Active: {proxy_str}")
        self.status.setStyleSheet(f"color: {GREEN};")
        self.refresh()

    def disable_proxy(self):
        QNetworkProxy.setApplicationProxy(QNetworkProxy(QNetworkProxy.NoProxy))
        self.active_proxy = ""
        self.status.setText("Proxy disabled")
        self.status.setStyleSheet(f"color: {RED};")
        self.refresh()

    def remove_proxy(self):
        item = self.list_widget.currentItem()
        if not item:
            return
        proxy = item.text().split()[0]
        if proxy in self.proxies:
            self.proxies.remove(proxy)
        self.refresh()

    # ── TEST FUNCTION ─────────────────────────
    def test_proxy(self):
        item = self.list_widget.currentItem()
        if not item:
            return

        proxy_str = item.text().split()[0]
        self.status.setText("Testing...")
        self.status.setStyleSheet(f"color: {YELLOW};")

        threading.Thread(target=self._run_test, args=(proxy_str,), daemon=True).start()

    def _run_test(self, proxy_str):
        try:
            proxy_handler = urllib.request.ProxyHandler({
                "http": f"http://{proxy_str}",
                "https": f"http://{proxy_str}",
            })
            opener = urllib.request.build_opener(proxy_handler)

            start = time.time()
            response = opener.open("http://ip-api.com/json", timeout=5)
            ms = int((time.time() - start) * 1000)

            data = json.loads(response.read().decode())
            country = data.get("country", "Unknown")

            self.status.setText(f"WORKING ({country}) - {ms}ms")
            self.status.setStyleSheet(f"color: {GREEN};")

        except Exception:
            self.status.setText("FAILED")
            self.status.setStyleSheet(f"color: {RED};")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProxyTool()
    window.show()
    sys.exit(app.exec_())
