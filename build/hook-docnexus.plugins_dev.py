
import os
import sys
from PyInstaller.utils.hooks import collect_submodules

# This hook ensures that if 'docnexus.plugins_dev' is imported,
# PyInstaller searches that directory for all submodules (our plugins)
# and includes them as hidden imports.

# Note: This runs during the build process.
hiddenimports = collect_submodules('docnexus.plugins_dev')

print(f" [HOOK] Collected plugin modules: {hiddenimports}")
