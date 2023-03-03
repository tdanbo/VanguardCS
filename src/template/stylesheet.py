SATURATION = "0%"


DARK_COLOR = "#2d2d2d"
BORDER_COLOR_LIGHT = "#3b3b3b"
RADIUS = "0px"
DISABLED_COLOR = "hsl(0, 0%, 30%)"
WHITE_LIGHT = f"hsl(0, {SATURATION}, 75%)"


# updating stylesheet
FONT_COLOR = "hsl(0, 0%, 90%);"
NEW_SATIRATON = "0%"
BORDER_COLOR = f"hsl(0, {NEW_SATIRATON}, 15%)"
GROUP_HEADER = f"hsl(0, {NEW_SATIRATON}, 15%)"
GROUP_BACKGROUND = f"hsl(0, {NEW_SATIRATON}, 20%)"
GUI_BACKGROUND = f"hsl(0, {SATURATION}, 25%)"
WIDGET_BACKGROUND = f"hsl(0, 0%, 25%)"

WIDGETS = f"QWidget {{color: hsl(45, {NEW_SATIRATON}, 70%); border-bottom: 1px solid {BORDER_COLOR}; background-color: {GROUP_BACKGROUND}}}"
COMBOBOX = f"QComboBox {{color: hsl(45, {NEW_SATIRATON}, 70%); padding-left: 20px; border-bottom: 1px solid {BORDER_COLOR}; background-color: {GROUP_BACKGROUND}}}"

PROGRASSBAR = (
    f"QProgressBar {{color: hsl(45, {NEW_SATIRATON}, 15%); border: 1px solid {BORDER_COLOR}; background-color: {WIDGET_BACKGROUND}}}"
    f"QProgressBar::chunk {{background-color: {FONT_COLOR}}}"
)
RUN_BUTTON = f"QToolButton {{color: hsl(45, {NEW_SATIRATON}, 70%); border: 1px solid {BORDER_COLOR}; background-color: {WIDGET_BACKGROUND}}}"

GUI_COLOR = "#3d1f1f"

QGROUPBOX = (
    f"QGroupBox {{background-color: {GROUP_BACKGROUND}; border: 1px solid {BORDER_COLOR}; border-bottom-right-radius: {RADIUS}; border-bottom-left-radius: {RADIUS}}}"
    f"QWidget {{color: hsl(45, {NEW_SATIRATON}, 50%); background-color: {GROUP_BACKGROUND}; }}"
    f"QScrollArea {{background-color: {GROUP_BACKGROUND}; }}"
    f"QScrollBar {{background-color: {WHITE_LIGHT}; width: 6px;}}"
    f"QScrollBar::handle:vertical {{background-color: {DARK_COLOR}; width: 6px; min-height: 20px; border: none; outline: none;}}"
)

QTITLE = (
    f"QToolButton {{background-color: {GROUP_HEADER}}}"
    f"QWidget {{font-size: 10px; color: {FONT_COLOR}; background-color: {GROUP_HEADER}; border-top-right-radius: {RADIUS}}}"
    f"QCheckBox {{background-color: {GROUP_HEADER}; border: 0px; border-top-right-radius: {RADIUS}; padding-left: 10px;}}"
    f"QWidget::disabled {{font-size: 10px; color: {DISABLED_COLOR}; background-color: {GROUP_HEADER}; border-top-right-radius: {RADIUS}}}"
)

MAIN_WINDOW = f"QWidget {{background-color: {GUI_BACKGROUND}; border-style: outset;}}"
