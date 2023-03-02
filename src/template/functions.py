from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import os
import constants as cons


def set_icon(widget, icon, color, width=0):
    qicon = QIcon()
    if icon in [".png", ""]:
        pixmap = QPixmap()
    else:
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
    except:
        if width == 0:
            widget.setPixmap(pixmap)
            widget.setScaledContents(False)
        else:
            print(f"Scaled icon: {icon} {width}")
            try:
                pix_width = width  # set the desired width for the scaled icon
                height = int(
                    pixmap.height() * (pix_width / pixmap.width())
                )  # calculate the corresponding height
                scaled_pixmap = pixmap.scaled(
                    pix_width, height
                )  # create a new scaled pixmap

                widget.setPixmap(scaled_pixmap)
            except:
                widget.setPixmap(pixmap)
                print(f"Error: {icon} {width}")
