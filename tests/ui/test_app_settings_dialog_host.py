from __future__ import annotations

import pytest

from context_aware_translation.ui.shell_hosts.app_settings_dialog_host import AppSettingsDialogHost

try:
    from PySide6.QtCore import Qt
    from PySide6.QtQuickWidgets import QQuickWidget
    from PySide6.QtWidgets import QApplication, QLabel

    HAS_PYSIDE6 = True
except ImportError:  # pragma: no cover - environment dependent
    HAS_PYSIDE6 = False

pytestmark = pytest.mark.skipif(not HAS_PYSIDE6, reason="PySide6 not available")


@pytest.fixture(autouse=True, scope="module")
def _qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


def test_app_settings_dialog_host_uses_native_title_bar_and_wraps_body_widget():
    host = AppSettingsDialogHost()
    try:
        body = QLabel("app-setup")
        host.set_app_settings_widget(body)

        assert host.chrome_host is None
        assert host.top_separator is not None
        assert host.top_separator.height() == 1
        assert host.findChildren(QQuickWidget) == []
        assert bool(host.windowFlags() & Qt.WindowType.WindowCloseButtonHint)
        assert (host.width(), host.height()) == (940, 580)
        assert host.body_widget is body
        assert host.viewmodel.title == "App Settings"
    finally:
        host.close()
        host.deleteLater()
        QApplication.processEvents()


def test_app_settings_dialog_host_present_and_native_close_update_dialog_state():
    host = AppSettingsDialogHost()
    try:
        host.present()
        assert host.viewmodel.is_presented is True

        host.close()

        assert host.viewmodel.is_presented is False
    finally:
        host.close()
        host.deleteLater()
        QApplication.processEvents()
