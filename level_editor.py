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
#def draw_menu_manual(self,context):
#slef : 呼び出し元のクラスインスタンス。C++でいうthisポインタ
#context : カーソルを合わせた時のポップアップのカスタマイズなどに使用
#トップバーの「エディターメニュー」に項目(オペレーター)を追加
#self.layout.operator("wm.url_open_preset",text="Manual", icon='HELP')
#オペレーター 頂点を伸ばす
class MYADDON_OT_stretch_vertex(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_stretch_vertex"
    bl_label = "頂点を伸ばす"
    bl_description = "頂点座標を引っ張って伸ばします"
    #リドゥ、アンドゥ可能オプション
    bl_options = {'REGISTER','UNDO'}

    #メニューを実装したときに呼ばれるコールバック関数
    def execute(self,context):
        bpy.data.objects["Cube"].data.vertices[0].co.x += 1.0
        print("頂点を伸ばしました")

        #オペレーターの命令終了を通知
        return{'FINISHED'}

#オペレーター ICO球生成
class MYADDON_OT_create_ico_sphere(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_create_cbject"
    bl_label = "ICO球生成"
    bl_description = "ICO球を生成します"
    #リドゥ、アンドゥ可能オプション
    bl_options = {'REGISTER','UNDO'}

     #メニューを実装したときに呼ばれるコールバック関数
    def execute(self,context):
        bpy.ops.mesh.primitive_ico_sphere_add()
        print("ICO球を生成しました。")
        return{'FINISHED'}


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


#オペレーター シーン出力
class MYADDON_OT_export_scene(bpy.types.Operator,bpy_extras.io_utils.ExportHelper):
    bl_idname = "myaddon.myaddon_ot_export_scene"
    bl_label = "シーン出力"
    bl_description = "シーン情報をExportします"


    def parse_scene_recursive(self, file, object, level):
        """シーン解析用再起関数"""

        #深さ分インデントする(タブを挿入)
        indent = ''
        for i in range(level):
            indent += "\t"

        #オブジェクト名書き込み
        self.write_and_print(file, indent + object.type + " - " + object.name)
        #ローカルトランスフォーム行列から平行移動、回転、スケーリングを抽出
        #型は Vector, Quaternion, Vector
        trans, rot, scale = object.matrix_local.decompose()
        #回転を Quaternion から Euler (3軸での回転角)に変換
        rot = rot.to_euler()
        #ラジアンから度数法に変換
        rot.x = math.degrees(rot.x)
        rot.y = math.degrees(rot.y)
        rot.z = math.degrees(rot.z)

        #トランスフォーム情報を表示
        self.write_and_print(file, indent + "Trans(%f,%f,%f)" % (trans.x, trans.y, trans.z) )
        self.write_and_print(file, indent + "Rot(%f,%f,%f)" % (rot.x, rot.y, rot.z) )
        self.write_and_print(file, indent + "Scale(%f,%f,%f)" % (scale.x, scale.y, scale.z) )
        self.write_and_print(file, '')

        #子ノードへ進む(深さが1上がる)
        for child in object.children:
            self.parse_secne_recursive(file, child, level + 1)


    def write_and_print(self, file, str):
        print(str)

        file.write(str)
        file.write('\n')

    def export(self):
        """ファイルに出力"""

        print("シーン情報出力開始... %r" % self.filepath)

        #ファイルをテキスト形式で書き出し用にオープン
        #スコープを抜けると自動的にクローズされる
        with open(self.filepath, "wt") as file:

            #ファイルに文字列を書き込む
            self.write_and_print(file, "SCENE")

            #シーン内の全オブジェクトについて
            for object in bpy.context.scene.objects:

                #親オブジェクトがあるものはスキップ (代わりに親から呼び出すから)
                if (object.parent):
                    continue
                #シーン直下のオブジェクトをルートノード(深さ0)とし、再起関数で走査
                self.parse_scene_recursive(file, object, 0)

    def execute(self, context):
    
        print("シーン情報をExportします")
        #ファイルに出力
        self.export()
        return{'FINISHED'}
        
        

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
        
         #トップバーの「エディターメニュー」に項目(オペレーター)を追加
        self.layout.operator(MYADDON_OT_export_scene.bl_idname,
            text = MYADDON_OT_export_scene.bl_label)


    #既存のメニューにサブメニューを追加
    def submenu(self,context):
        #ID指定でサブメニューを追加
        self.layout.menu(TOPBAR_MT_my_menu.bl_idname)

#Blenderに登録するクラスリスト
classes = (
    MYADDON_OT_create_ico_sphere,
    MYADDON_OT_stretch_vertex,
    MYADDON_OT_export_scene,
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