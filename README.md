# Project Template

A repository template for my projects.

## Getting Started

After creating the repository from this template, complete the following before starting the development of your new project:

### Requirements

- [uv](https://docs.astral.sh/uv/getting-started/installation/)

When using Nuitka as the build backend:

1. Install C++ Build Tools via the [Visual Studio Community Installer](https://visualstudio.microsoft.com/downloads/)
2. [scripts/build.py:19](./scripts/build.py#L19) - replace `CxFreezeBackend` by `NuitkaBackend` and update the import statement
3. Run the following from the project root to replace the cx_Freeze dependency by Nuitka:
    `uv remove --dev cx_freeze && uv add --dev nuitka`

### These are some placeholders you should replace:

- [ ] [src/core/config/app_config.py:26-35](./src/core/config/app_config.py#L26-36)
- [ ] [src/ui/menubar.py:37](./src/ui/menubar.py#L37)
- [ ] [src/ui/menubar.py:41](./src/ui/menubar.py#L41)
- [ ] [src/ui/menubar.py:45](./src/ui/menubar.py#L45)
- [ ] [src/ui/statusbar.py:26](./src/ui/statusbar.py#L26)
- [ ] [src/app.py:23](./src/app.py#L23)
- [ ] [Optional] [src/app.py:77-91](./src/app.py#L77-92) - only change if you maintain a `Changelog.md` file and an `update.json` file like the following in your repository:
  ```json
  {
      "version": "0.0.1",  // This is the latest version of your project
      "download_url": "https://github.com/you/your-repository/releases"  // Replace this by the actual download URL
  }
  ```
- [ ] [scripts/build.py:47](./scripts/build.py#L47)
- [ ] [pyproject.toml:2-6](./pyproject.toml#L2-7)
