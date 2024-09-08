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

#メニュー選択画面
def draw_menu_manual(self,context):
#slef : 呼び出し元のクラスインスタンス。C++でいうthisポインタ
#context : カーソルを合わせた時のポップアップのカスタマイズなどに使用
#トップバーの「エディターメニュー」に項目(オペレーター)を追加
self.layout.operator("wm.url_open_preset",text="Manual", icon='HELP')

#トップバーの拡張メニュー
class TOPBAR_MT_my_menu(bpy.types.Menu):
    #Blenderがクラスを識別する為の固有の文字列
    bl_idname = "TOPBAR_MT_my_menu"
    #メニューのラベルとして表示される文字列
    bl_label = "Mymenu"
    #著者表示用の文字列
    bl_description = "拡張メニュー by" + bl_info["author"]

    #サブメニューの描画
    def draw(self,context):
#トップバーの「エディターメニュー」に項目(オペレーター)を追加
        self.layout.operator(MYADDON_OT_stretch_vertex.bl_idname,
            text = MYADDON_OT_stretch_vertex.bl_label)

        #トップバーの「エディターメニュー」に項目(オペレーター)を追加
        self.layout.operator(MYADDON_OT_create_ico_sphere.bl_idname,
            text = MYADDON_OT_create_ico_sphere.bl_label)


    #既存のメニューにサブメニューを追加
    def submenu(self,context):
        #ID指定でサブメニューを追加
        self.layout.menu(TOPBAR_MT_my_menu.bl_idname)
        

#トップバーの拡張メニュー
class TOPBAR_MT_my_menu(bpy.types.Menu):
    #Blenderがクラスを識別する為の固有の文字列
    bl_idname = "TOPBAR_MT_my_menu"
    #メニューのラベルとして表示される文字列
    bl_label = "Mymenu"
    #著者表示用の文字列
    bl_description = "拡張メニュー by" + bl_info["author"]

    #サブメニューの描画
    def draw(self,context):

        #トップバーの「エディターメニュー」に項目(オペレーター)を追加
        self.layout.operator(MYADDON_OT_stretch_vertex.bl_idname,
            text = MYADDON_OT_stretch_vertex.bl_label)

    #既存のメニューにサブメニューを追加
    def submenu(self,context):
        #ID指定でサブメニューを追加
        self.layout.menu(TOPBAR_MT_my_menu.bl_idname)

#Blenderに登録するクラスリスト
classes = (
    TOPBAR_MT_my_menu,
)

#Add-On有効化時コールバック
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    #メニューから項目の追加
    bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_my_menu.submenu)
    print("レベルエディタが有効化されました")

#Add-On無効化時コールバック
def unregister():
    #メニューから項目の削除
    for cls in classes:
        bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_my_menu.submenu)

    print("レベルエディタが無効化されました")

if __name__ == "__main__":
    register()