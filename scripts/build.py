"""
Copyright (c) Cutleast

Run this script from the project's root folder to build the standalone executable in
`./dist`.
"""

import logging
import re
from pathlib import Path
from typing import override

from cutleast_core_lib.builder.backends.cx_freeze_backend import CxFreezeBackend
from cutleast_core_lib.builder.build_config import BuildConfig
from cutleast_core_lib.builder.build_metadata import BuildMetadata
from cutleast_core_lib.builder.builder import Builder


class Backend(CxFreezeBackend):
    """
    Backend that injects the project version into the app module before building.
    """

    # this injects the version at, e.g. `APP_VERSION: str = "development"`
    VERSION_PATTERN: re.Pattern[str] = re.compile(
        r'(?<=APP_VERSION: str = ")[^"]+(?=")'
    )

    @override
    def preprocess_source(self, source_folder: Path, metadata: BuildMetadata) -> None:
        app_module: Path = source_folder / "app.py"
        app_module.write_text(
            Backend.VERSION_PATTERN.sub(
                str(metadata.project_version), app_module.read_text(encoding="utf8")
            ),
            encoding="utf8",
        )
        self.log.info(
            f"Injected version '{metadata.project_version}' into '{app_module}'."
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    config = BuildConfig(
        exe_stem="template",  # Enter the name of the executable without ".exe" suffix here
        ext_resources_json=Path("res") / "ext_resources.json",
    )
    backend = Backend()
    builder = Builder(config, backend)

    builder.run()
