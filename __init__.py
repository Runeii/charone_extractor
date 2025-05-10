bl_info = {
    "name": "CharOne Extractor",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (4, 3, 0),
    "location": "File > Import > CharOne (.one)",
    "description": "Import models from CharOne files",
    "warning": "",
    "doc_url": "",
    "category": "Import-Export",
}

import bpy
import os
import sys

# Add the addon directory to Python path
addon_dir = os.path.dirname(os.path.realpath(__file__))
if addon_dir not in sys.path:
    sys.path.insert(0, addon_dir)

from bpy.props import StringProperty
from bpy_extras.io_utils import ImportHelper
from bpy.types import Context, Panel

# Import local modules
from src.main import process_file

class ImportCharOne(bpy.types.Operator, ImportHelper):
    """Import from CharOne (.one)"""
    bl_idname = "import.charone"
    bl_label = "Import CharOne"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = ".one"
    filter_glob: StringProperty(default="*.one", options={'HIDDEN'})

    def execute(self, context: 'Context') -> set[str]:
        process_file(self.filepath)
        return {'FINISHED'}

def menu_func_import(self: 'Panel', context: 'Context') -> None:
    if self.layout is not None:
        layout: UILayout = self.layout
        layout.operator(ImportCharOne.bl_idname, text="CharOne (.one)")

def register() -> None:
    bpy.utils.register_class(ImportCharOne)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

def unregister() -> None:
    bpy.utils.unregister_class(ImportCharOne)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)  # type: ignore

if __name__ == "__main__":
    register() 