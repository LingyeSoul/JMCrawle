import flet as ft
import os
from option import OptionManager


def create_settings_dialog(page: ft.Page, config_manager):
    """创建设置对话框"""
    # 获取当前下载路径
    option_manager = OptionManager()
    current_download_path = option_manager.get("dir_rule.base_dir", os.path.join(os.getcwd(), "download"))
    
    # 获取当前插件设置
    plugins_config = option_manager.get("plugins", {})
    
    # 创建路径输入框
    path_field = ft.TextField(
        label="下载路径",
        value=current_download_path,
        width=300,
        read_only=True,
    )
    
    # 创建选择路径按钮
    def pick_directory(e):
        def pick_directory_result(e: ft.FilePickerResultEvent):
            if e.path:
                path_field.value = e.path
                path_field.update()
                
        file_picker = ft.FilePicker(on_result=pick_directory_result)
        page.overlay.append(file_picker)
        page.update()
        file_picker.get_directory_path(dialog_title="选择下载目录")
    
    pick_button = ft.ElevatedButton(
        "选择路径",
        icon=ft.Icons.FOLDER_OPEN,
        on_click=pick_directory,
    )
    
    # 创建插件开关
    # 定义插件信息
    plugin_info = {
        "before_album": [
            {"name": "download_cover", "label": "下载封面"}
        ],
        "after_album": [
            {"name": "img2pdf", "label": "转换为PDF"},
            {"name": "long_img", "label": "生成长图"}
        ],
        "before_photo": [
            {"name": "skip_photo_with_few_images", "label": "跳过图片过少的章节"}
        ]
    }

    # 定义插件阶段的用户友好显示映射
    plugin_stage_display = {
        "before_album": "保存本子前",
        "after_album": "保存本子后", 
        "before_photo": "保存章节前"
    }
    
    # 创建插件开关控件
    plugin_switches = {}
    plugin_controls = []
    
    # 创建ZIP插件的delete_original_file开关
    zip_delete_original_switch = ft.Switch(
        label="压缩后删除原始文件",
        value=False,  # 默认值将在下面设置
        adaptive=True
    )
    
    # 设置delete_original_file开关的默认值
    if "after_album" in plugins_config:
        for plugin_config in plugins_config["after_album"]:
            if plugin_config.get("plugin") == "zip" and "kwargs" in plugin_config:
                zip_delete_original_switch.value = plugin_config["kwargs"].get("delete_original_file", False)
                break
    
    for section, plugins in plugin_info.items():
        section_controls = [ft.Text(f"{plugin_stage_display[section]} 阶段", size=16, weight=ft.FontWeight.W_500)]
        
        for plugin in plugins:
            # 检查插件是否已启用
            is_enabled = False
            if section in plugins_config:
                for plugin_config in plugins_config[section]:
                    if plugin_config.get("plugin") == plugin["name"]:
                        is_enabled = True
                        break
            
            switch = ft.Switch(
                label=plugin["label"],
                value=is_enabled,
                adaptive=True
            )
            plugin_switches[f"{section}.{plugin['name']}"] = switch
            section_controls.append(switch)
            

        plugin_controls.extend(section_controls)
        plugin_controls.append(ft.Divider())
    
    # 如果有插件控件，移除最后一个分割线
    if plugin_controls and isinstance(plugin_controls[-1], ft.Divider):
        plugin_controls.pop()
    
    def save_settings(e):
        # 保存下载路径设置
        option_manager.set("dir_rule.base_dir", path_field.value)
        
        # 保存插件设置
        plugins_config = {}
        for key, switch in plugin_switches.items():
            section, plugin_name = key.split(".")
            if switch.value:  # 如果开关打开
                if section not in plugins_config:
                    plugins_config[section] = []
                
                # 根据插件类型添加默认配置
                plugin_config = {"plugin": plugin_name}
                if plugin_name == "download_cover":
                    plugin_config["kwargs"] = {
                        "size": "_3x4",
                        "dir_rule": {
                            "base_dir": path_field.value,
                            "rule": "JM{Aid}-{Atitle}/cover.jpg"
                        }
                    }
                elif plugin_name == "img2pdf":
                    plugin_config["kwargs"] = {
                        "pdf_dir": path_field.value,
                        "filename_rule": "JM{Aid}-{Atitle}"
                    }
                elif plugin_name == "long_img":
                    plugin_config["kwargs"] = {
                        "pdf_dir": path_field.value,
                        "filename_rule": "JM{Aid}-{Atitle}"
                    }
                elif plugin_name == "skip_photo_with_few_images":
                    plugin_config["kwargs"] = {
                        "at_least_image_count": 3
                    }
                
                plugins_config[section].append(plugin_config)
        
        # 如果有插件配置，保存它；否则确保plugins字段被正确处理
        if plugins_config:
            option_manager.set("plugins", plugins_config)
        else:
            # 确保plugins字段被移除（根据OptionManager的save_option逻辑）
            option_manager.set("plugins", {})
        
        option_manager.save_option()
        dlg.open = False
        page.update()
        
        # 显示保存成功提示
        page.open(
            ft.SnackBar(
                content=ft.Text("设置已保存"),
                action="好的",
            )
        )
    
    def close_dlg(e):
        dlg.open = False
        page.update()
        
    # 创建设置对话框内容
    dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text("设置"),
        content=ft.Column(
            [
                ft.Divider(),
                ft.Text("下载设置", size=16, weight=ft.FontWeight.W_500),
                ft.Row(
                    [
                        path_field,
                        pick_button,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Divider(),
            ] + plugin_controls,
            tight=True,
            width=500,
            height=600,
            scroll=ft.ScrollMode.AUTO,
        ),
        actions=[
            ft.TextButton("取消", on_click=close_dlg),
            ft.TextButton("保存", on_click=save_settings),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    return dlg