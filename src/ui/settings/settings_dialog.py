"""
Copyright (c) Cutleast
"""

import os
import subprocess

from cutleast_core_lib.core.config.exceptions import ConfigValidationError
from cutleast_core_lib.core.config.manager import ConfigManager
from cutleast_core_lib.core.utilities.exe_info import get_execution_info
from cutleast_core_lib.ui.theme.manager import ThemeManager
from cutleast_core_lib.ui.utilities.icon_provider import IconProvider
from cutleast_core_lib.ui.widgets.tab_widget import TabWidget
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from core.config.app_config import AppConfig

from .app_settings import AppSettings


class SettingsDialog(QDialog):
    """
    Dialog for application settings.
    """

    __app_config_manager: ConfigManager[AppConfig]
    __app_config: AppConfig

    __vlayout: QVBoxLayout
    __tab_widget: TabWidget

    __app_settings_widget: AppSettings

    __validation_label: QLabel
    __save_button: QPushButton

    __restart_required: bool = False
    __theme_update_required: bool = False

    def __init__(self, app_config_manager: ConfigManager[AppConfig]) -> None:
        """
        Args:
            app_config_manager (ConfigManager[AppConfig]):
                Manager for the application configuration.
        """

        super().__init__()

        self.__app_config_manager = app_config_manager
        self.__app_config = app_config_manager.config

        self.__init_ui()
        self.setWindowTitle(self.tr("Settings"))

        self.__tab_widget.tabBar().hide()  # remove this when you add more tabs
        # remove this when a scrollbar is required
        self.__tab_widget.pane().setContentsMargins(0, 0, 0, 0)

        self.__app_settings_widget.changed_signal.connect(self.__on_change)
        self.__app_settings_widget.restart_required_signal.connect(
            self.__on_restart_required
        )
        self.__app_settings_widget.theme_update_required_signal.connect(
            self.__on_theme_update_required
        )

    def __init_ui(self) -> None:
        self.__vlayout = QVBoxLayout()
        self.__vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.__vlayout)

        self.__init_header()
        self.__init_settings_widget()
        self.__init_footer()

    def __init_header(self) -> None:
        hlayout = QHBoxLayout()
        hlayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.__vlayout.addLayout(hlayout)

        icon_label = QLabel()
        IconProvider.bind_qta_icon(
            icon_label,
            lambda icon: icon_label.setPixmap(
                icon.pixmap(
                    ThemeManager.get().theme.metrics.icon_xl,
                    ThemeManager.get().theme.metrics.icon_xl,
                )
            ),
            "mdi6.cog",
        )
        hlayout.addWidget(icon_label)

        title_label = QLabel(self.tr("Settings"))
        title_label.setProperty("title", True)
        hlayout.addWidget(title_label)

        restart_hint_label = QLabel(
            self.tr("Settings marked with * require a restart to take effect.")
        )
        restart_hint_label.setProperty("secondary", True)
        self.__vlayout.addWidget(restart_hint_label)

    def __init_settings_widget(self) -> None:
        self.__tab_widget = TabWidget()
        self.__vlayout.addWidget(self.__tab_widget)

        self.__app_settings_widget = AppSettings(self.__app_config_manager)
        self.__tab_widget.addTab(self.__app_settings_widget, self.tr("App Settings"))

    def __init_footer(self) -> None:
        hlayout = QHBoxLayout()
        self.__vlayout.addLayout(hlayout)

        cancel_button = QPushButton(self.tr("Cancel"))
        cancel_button.clicked.connect(self.reject)
        hlayout.addWidget(cancel_button)

        hlayout.addStretch()

        self.__validation_label = QLabel()
        self.__validation_label.setProperty("state", "error")
        hlayout.addWidget(self.__validation_label)

        self.__save_button = QPushButton(self.tr("Save"))
        self.__save_button.setDefault(True)
        self.__save_button.clicked.connect(self.__save)
        self.__save_button.setDisabled(True)
        hlayout.addWidget(self.__save_button)

    def __on_change(self) -> None:
        self.setWindowTitle(self.tr("Settings") + "*")

        try:
            self.__app_settings_widget.validate()

            self.__validation_label.setHidden(True)
            self.__save_button.setEnabled(True)
        except ConfigValidationError as ex:
            self.__validation_label.setText(str(ex))
            self.__validation_label.setVisible(True)
            self.__save_button.setDisabled(True)

    def __on_restart_required(self) -> None:
        self.__restart_required = True

    def __on_theme_update_required(self) -> None:
        self.__theme_update_required = True

    def __save(self) -> None:
        self.__app_settings_widget.apply()
        self.__app_config_manager.save()

        if self.__theme_update_required:
            ThemeManager.get().set_primary_color(
                self.__app_config.accent_color, apply=False
            )
            ThemeManager.get().set_ui_mode(self.__app_config.ui_mode)

        self.accept()

        if self.__restart_required:
            messagebox = QMessageBox()
            messagebox.setWindowTitle(self.tr("Restart required"))
            messagebox.setText(
                self.tr(
                    "The app must be restarted for the changes to take effect! Restart now?"
                )
            )
            messagebox.setStandardButtons(
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            messagebox.button(QMessageBox.StandardButton.No).setText(self.tr("No"))
            messagebox.button(QMessageBox.StandardButton.Yes).setText(self.tr("Yes"))
            choice = messagebox.exec()

            if choice == QMessageBox.StandardButton.Yes:
                from app import App

                if App.get().main_window.close():
                    os.startfile(subprocess.list2cmdline(get_execution_info()[0]))
