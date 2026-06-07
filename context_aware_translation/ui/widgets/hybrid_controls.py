from __future__ import annotations

from PySide6.QtWidgets import QAbstractButton, QWidget

_HYBRID_CONTROL_STYLESHEET = """
QPushButton {
    min-height: 38px;
    padding: 0 16px;
    border-radius: 14px;
    border: 1px solid #d9d0c4;
    background: #f8f3ea;
    color: #2f251d;
    font-weight: 600;
}
QPushButton:hover:enabled {
    background: #efe7da;
}
QPushButton:pressed:enabled {
    background: #e7ddd0;
}
QPushButton:disabled {
    background: #efe7da;
    color: #8b8174;
    border-color: #e5dccf;
}
QPushButton[catTone="primary"] {
    border: none;
    background: #2f251d;
    color: #fcfaf6;
}
QPushButton[catTone="primary"]:hover:enabled {
    background: #43362b;
}
QPushButton[catTone="danger"] {
    background: #fff2f0;
    color: #b42318;
    border: 1px solid #f7b3ad;
}
QPushButton[catTone="danger"]:hover:enabled {
    background: #ffe4e1;
}
QPushButton[catTone="ghost"] {
    background: transparent;
    border: 1px solid #ddd4c8;
}
QPushButton[catSize="compact"] {
    min-height: 32px;
    padding: 0 12px;
    border-radius: 12px;
}
QPushButton[catSize="wide"] {
    min-width: 150px;
}
QLabel {
    background: transparent;
    color: #2f251d;
}
QLineEdit,
QComboBox,
QSpinBox,
QDoubleSpinBox,
QTextEdit,
QPlainTextEdit {
    border: 1px solid #d9d0c4;
    border-radius: 12px;
    background: #fffdf9;
    color: #2f251d;
    selection-background-color: #e7ddd0;
    selection-color: #2f251d;
}
QLineEdit,
QComboBox,
QSpinBox,
QDoubleSpinBox {
    min-height: 38px;
    padding: 0 12px;
}
QComboBox {
    combobox-popup: 0;
    padding-right: 34px;
}
QTextEdit,
QPlainTextEdit {
    padding: 10px 12px;
}
QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    border: none;
    width: 28px;
}
QComboBox::down-arrow {
    width: 0;
    height: 0;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #6e6154;
    margin-right: 10px;
}
QComboBox QAbstractItemView {
    border: 1px solid #d9d0c4;
    border-radius: 12px;
    background: #fffdf9;
    color: #2f251d;
    padding: 6px 0;
    selection-background-color: #efe7da;
    selection-color: #2f251d;
    outline: none;
}
QLineEdit:disabled,
QComboBox:disabled,
QSpinBox:disabled,
QDoubleSpinBox:disabled,
QTextEdit:disabled,
QPlainTextEdit:disabled {
    background: #efe7da;
    color: #8b8174;
    border-color: #e5dccf;
}
QSpinBox::up-button, QDoubleSpinBox::up-button {
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 24px;
    border: none;
    border-left: 1px solid #d9d0c4;
    border-bottom: 1px solid #d9d0c4;
    border-top-right-radius: 12px;
    background: #f8f3ea;
}
QSpinBox::down-button, QDoubleSpinBox::down-button {
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    width: 24px;
    border: none;
    border-left: 1px solid #d9d0c4;
    border-bottom-right-radius: 12px;
    background: #f8f3ea;
}
QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover,
QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {
    background: #efe7da;
}
QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {
    width: 0;
    height: 0;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-bottom: 6px solid #6e6154;
}
QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {
    width: 0;
    height: 0;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #6e6154;
}
QCheckBox {
    color: #2f251d;
    spacing: 8px;
}
QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #d9d0c4;
    border-radius: 4px;
    background: #fffdf9;
}
QCheckBox::indicator:checked {
    background: #2f251d;
    border-color: #2f251d;
}
QCheckBox::indicator:checked:hover {
    background: #43362b;
    border-color: #43362b;
}
QCheckBox::indicator:unchecked:hover {
    background: #f4ecdf;
    border-color: #bfb4a4;
}
QCheckBox::indicator:disabled {
    background: #efe7da;
    border-color: #e5dccf;
}
QRadioButton {
    color: #2f251d;
    spacing: 8px;
}
QRadioButton::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #d9d0c4;
    border-radius: 10px;
    background: #fffdf9;
}
QRadioButton::indicator:checked {
    background: #2f251d;
    border-color: #2f251d;
}
QRadioButton::indicator:checked:hover {
    background: #43362b;
    border-color: #43362b;
}
QRadioButton::indicator:unchecked:hover {
    background: #f4ecdf;
    border-color: #bfb4a4;
}
QRadioButton::indicator:disabled {
    background: #efe7da;
    border-color: #e5dccf;
}
QGroupBox {
    border: 1px solid #d9d0c4;
    border-radius: 8px;
    margin-top: 12px;
    padding: 14px 8px 8px;
    color: #2f251d;
    font-weight: 600;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 6px;
    color: #2f251d;
}
QTabWidget::pane {
    border: 1px solid #d9d0c4;
    border-radius: 8px;
    background: #fcfaf6;
}
QTabBar::tab {
    background: transparent;
    color: #6e6154;
    border: none;
    padding: 8px 16px;
    margin-right: 2px;
    font-weight: 500;
}
QTabBar::tab:selected {
    color: #2f251d;
    border-bottom: 2px solid #2f251d;
}
QTabBar::tab:hover:!selected {
    color: #43362b;
}
QProgressBar {
    border: 1px solid #d9d0c4;
    border-radius: 6px;
    background: #efe7da;
    text-align: center;
    color: #2f251d;
    height: 20px;
}
QProgressBar::chunk {
    background: #2f251d;
    border-radius: 5px;
}
QSplitter::handle {
    background: #e5ddd0;
}
QSplitter::handle:horizontal {
    width: 2px;
}
QSplitter::handle:vertical {
    height: 2px;
}
QScrollArea {
    border: none;
    background: transparent;
}
QTableView, QTableWidget {
    border: 1px solid #d9d0c4;
    border-radius: 8px;
    background: #fffdf9;
    color: #2f251d;
    gridline-color: #e5ddd0;
    selection-background-color: #efe7da;
    selection-color: #2f251d;
}
QTableView::item, QTableWidget::item {
    padding: 8px;
    color: #2f251d;
}
QTableView::item:selected, QTableWidget::item:selected {
    background-color: #efe7da;
    color: #2f251d;
}
QHeaderView::section {
    background-color: #f7f3ec;
    color: #2f251d;
    padding: 8px;
    border: none;
    border-bottom: 1px solid #e5ddd0;
    border-right: 1px solid #e5ddd0;
    font-weight: bold;
}
QListWidget {
    border: 1px solid #d9d0c4;
    border-radius: 14px;
    background: #fcfaf6;
    alternate-background-color: #f7f1e8;
    padding: 6px;
    outline: none;
}
QListWidget::item {
    padding: 10px 12px;
    border-radius: 10px;
    color: #2f251d;
}
QListWidget::item:hover:!selected {
    background: #f4ecdf;
}
QListWidget::item:selected {
    background: #efe7da;
    color: #2f251d;
}
QListWidget::item:selected:active,
QListWidget::item:selected:!active {
    background: #efe7da;
    color: #2f251d;
}
"""


def apply_hybrid_control_theme(widget: QWidget, *, extra_stylesheet: str | None = None) -> None:
    parts: list[str] = []
    existing = widget.styleSheet().strip()
    if existing:
        parts.append(existing)
    parts.append(_HYBRID_CONTROL_STYLESHEET)
    if extra_stylesheet:
        parts.append(extra_stylesheet)
    widget.setStyleSheet("\n".join(parts))


def set_button_tone(button: QAbstractButton, tone: str | None = None, *, size: str | None = None) -> None:
    button.setProperty("catTone", tone)
    button.setProperty("catSize", size)
    style = button.style()
    style.unpolish(button)
    style.polish(button)
    button.update()
