"""
Copyright (c) 2018 iCyP
Released under the MIT license
https://opensource.org/licenses/mit-license.php

"""

#
#
# Please don't import anything in global scope to detect script reloading and minimize initialization.
#
#

bl_info = {
    "name": "VRM format",
    "author": "saturday06, iCyP",
    "version": (2, 1, 0),
    "blender": (2, 80, 0),
    "location": "File > Import-Export",
    "description": "Import-Edit-Export VRM",
    "warning": "",
    "support": "COMMUNITY",
    "wiki_url": "",
    "tracker_url": "https://github.com/saturday06/VRM_Addon_for_Blender/issues",
    "category": "Import-Export",
}


# Script reloading (if the user calls 'Reload Scripts' from Blender)
# https://github.com/KhronosGroup/glTF-Blender-IO/blob/04e26bef903543d08947c5a9a5fea4e787b68f17/addons/io_scene_gltf2/__init__.py#L32-L54
# http://www.apache.org/licenses/LICENSE-2.0
def reload_package(module_dict_main: dict) -> None:  # type: ignore[type-arg]
    # Lazy import to minimize initialization before reload_package()
    import importlib
    from pathlib import Path
    from typing import Any, Dict

    def reload_package_recursive(
        current_dir: Path, module_dict: Dict[str, Any]
    ) -> None:
        for path in current_dir.iterdir():
            if "__init__" in str(path) or path.stem not in module_dict:
                continue

            if path.is_file() and path.suffix == ".py":
                importlib.reload(module_dict[path.stem])
            elif path.is_dir():
                reload_package_recursive(path, module_dict[path.stem].__dict__)

    reload_package_recursive(Path(__file__).parent, module_dict_main)


if "bpy" in locals():
    reload_package(locals())


def register() -> None:
    import bpy

    if bpy.app.version < bl_info["blender"]:
        raise Exception(
            f"This add-on doesn't support Blender version less than {bl_info['blender']} "
            + f"but the current version is {bpy.app.version}"
        )

    # Lazy import to minimize initialization before blender version checking and reload_package().
    # 'import io_scene_vrm' causes an error in blender and vscode mypy integration.
    # pylint: disable=import-self,no-name-in-module
    from .io_scene_vrm import registration

    # pylint: enable=import-self,no-name-in-module

    registration.register(bl_info["version"])


def unregister() -> None:
    import bpy

    if bpy.app.version < bl_info["blender"]:
        return

    # Lazy import to minimize initialization before blender version checking and reload_package().
    # 'import io_scene_vrm' causes an error in blender and vscode mypy integration.
    # pylint: disable=import-self,no-name-in-module
    from .io_scene_vrm import registration

    # pylint: enable=import-self,no-name-in-module

    registration.unregister()


if __name__ == "__main__":
    register()
