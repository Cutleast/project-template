"""
Copyright (c) Cutleast
"""

from typing import cast, override

from cutleast_core_lib.core.config.app_config import AppConfig as BaseAppConfig
from cutleast_core_lib.ui.settings.app_settings import AppSettings as BaseAppSettings
from cutleast_core_lib.ui.widgets.enum_dropdown import EnumDropdown

from core.config.app_config import AppConfig


class AppSettings(BaseAppSettings):
    """
    App settings widget with language dropdown.
    """

    __language_box: EnumDropdown[AppConfig.AppLanguage]

    def __init__(self, initial_config: BaseAppConfig) -> None:
        super().__init__(initial_config)

        self.__language_box.currentValueChanged.connect(
            lambda _: self.changed_signal.emit()
        )
        self.__language_box.currentValueChanged.connect(
            lambda _: self.restart_required_signal.emit()
        )

    @override
    def _init_ui(self) -> None:
        super()._init_ui()

        config = cast(AppConfig, self._initial_config)
        self.__language_box = EnumDropdown(AppConfig.AppLanguage, config.language)
        self.__language_box.installEventFilter(self)
        self._basic_flayout.insertRow(
            5, "*" + self.tr("App language:"), self.__language_box
        )

    @override
    def apply(self, config: BaseAppConfig) -> None:
        super().apply(config)

        config = cast(AppConfig, config)
        config.language = self.__language_box.getCurrentValue()
