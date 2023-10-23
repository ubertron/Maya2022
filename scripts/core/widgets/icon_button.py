from pathlib import Path

from PySide2.QtCore import QSize
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QPushButton


class IconButton(QPushButton):
    def __init__(self, label: str, icon_path: Path, size: int = 24):
        super(IconButton, self).__init__()
        if icon_path.exists():
            self.setFixedSize(QSize(size, size))
            self.setIcon(QPixmap(icon_path.as_posix()))
            self.setToolTip(label)
        else:
            self.setMaximumHeight(size)
            self.setText(label)
