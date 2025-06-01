#*****************************************************************************#
#    Copyright (C) 2025 A H                                                #
#    Copyright (C) 2024 Shunsq                                                #
#    Copyright (C) 2024 Julian Xhokaxhiu                                      #
#                                                                             #
#    This file is part of FF8 MCH                                             #
#                                                                             #
#    FF8 MCH is free software: you can redistribute it and/or modify          #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License            #
#                                                                             #
#    FF8 MCH is distributed in the hope that it will be useful,               #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#*****************************************************************************#
bl_info = {
    "name": "CharaOne Extractor",
    "author": "A H,Shunsq,Julian Xhokaxhiu",
    "version": (1, 0),
    "blender": (4, 3, 0),
    "location": "File > Import > CharaOne (.one)",
    "description": "Import models from CharaOne files",
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
from src.main import copy_chara_files, process_file

class ImportCharOne(bpy.types.Operator, ImportHelper):
    """Import from CharaOne (.one)"""
    bl_idname = "ff8tools.charaone"
    bl_label = "Import CharaOne"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = ".one"
    filter_glob: StringProperty(default="*.one", options={'HIDDEN'})

    def execute(self, context: 'Context') -> set[str]:
        #copy_chara_files()
        process_file(self.filepath, 0)
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