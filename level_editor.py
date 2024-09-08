import math
import bpy
import bpy_extras

bl_info = {
    "name": "level_editor",
    "author": "Kuma Watanabe",
    "version": (1, 0),
    "blender": (3, 5),
    "location": "",
    "description": "level_editor",
    "warning": "",
    "support": "TESTING" ,
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}

#Add-On有効化時コールバック
def register():
    #メニューから項目の追加
    bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_my_menu.submenu)
    print("レベルエディタが有効化されました")

#Add-On無効化時コールバック
def unregister():
        bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_my_menu.submenu)

    print("レベルエディタが無効化されました")

if __name__ == "__main__":
    register()