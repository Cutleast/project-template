"""
Copyright (c) Cutleast
"""

from typing import Annotated

from cutleast_core_lib.core.config.app_config import AppConfig as BaseAppConfig
from cutleast_core_lib.core.utilities.base_enum import BaseEnum
from pydantic import Field


class AppConfig(BaseAppConfig):
    """
    App configuration.
    """

    class AppLanguage(BaseEnum):
        """Enum for the languages supported by the app."""

        System = "System"
        German = "de_DE"
        English = "en_US"

    language: Annotated[AppLanguage, Field(alias="ui.language")] = AppLanguage.System

    # Use this decorator to override default values from the parent class
    # @default_factory("accent_color")
    @classmethod
    def get_default_accent_color(cls) -> str:
        """
        Returns:
            str: Default accent color.
        """

        raise NotImplementedError  # Return your desired default accent color here
