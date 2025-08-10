"""
Copyright (c) Cutleast
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class MainWidget(QWidget):
    """
    The central widget of the main window.
    """

    def __init__(self) -> None:
        super().__init__()

        vlayout = QVBoxLayout()
        self.setLayout(vlayout)

        label = QLabel(self.tr("Hello World!"))
        label.setObjectName("h1")
        vlayout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
