from __future__ import annotations

from PySide6.QtWidgets import QWidget

from context_aware_translation.ui.shell_hosts.hybrid import HybridDialogHost
from context_aware_translation.ui.viewmodels.app_settings_dialog import AppSettingsDialogViewModel


class AppSettingsDialogHost(HybridDialogHost):
    """Dialog host for the app-settings body."""

    def __init__(self, parent: QWidget | None = None) -> None:
        self.viewmodel = AppSettingsDialogViewModel(parent)
        super().__init__(None, parent=parent)
        self.setModal(False)
        self.setWindowTitle(self.viewmodel.title)
        self.resize(1120, 760)
        self.finished.connect(lambda _result: self.viewmodel.dismiss())

    def set_app_settings_widget(self, widget: QWidget) -> QWidget:
        return self.set_body_widget(widget)

    def set_app_setup_widget(self, widget: QWidget) -> QWidget:
        return self.set_app_settings_widget(widget)

    def present(self) -> None:
        self.viewmodel.present()
        self.show()
        self.raise_()
        self.activateWindow()

    def dismiss(self) -> None:
        self.close()

    def retranslate(self) -> None:
        self.viewmodel.retranslate()
        self.setWindowTitle(self.viewmodel.title)
