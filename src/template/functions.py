from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import os
import constants as cons


def clear_layout(layout):
    for item in range(layout.count()):
        layout.itemAt(item).widget().deleteLater()


def set_icon(widget, icon, color, width=20):
    qicon = QIcon()
    pixmap = QPixmap(os.path.join(cons.ICONS, icon))

    if color != "":
        paint = QPainter(pixmap)
        if paint.isActive():
            paint.setCompositionMode(QPainter.CompositionMode_SourceIn)
            paint.fillRect(pixmap.rect(), QColor(color))
            paint.end()

    qicon.addPixmap(pixmap)

    try:
        widget.setIcon(qicon)
        widget.setIconSize(QSize(width, width))
    except:
        pixmap.scaled(width, width)
        widget.setPixmap(pixmap)
