import flet as ft
import threading
import time
import re
from typing import Optional
from config import ConfigManager
from jm_manager import JMComicManager
from ui_components import UIComponents
from settings_dialog import create_settings_dialog
import asyncio


class JMComicApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.config_manager = ConfigManager()
        self.jm_manager = JMComicManager()
        self.ui = UIComponents(page)
        self.setup_page()
        self.create_ui()
        
    async def initialize_jm_manager(self, progress_dialog=None):
        """异步初始化JMComicManager"""
        # 等待一帧，确保对话框显示
        await asyncio.sleep(0.01)
        
        try:
            await self.jm_manager.initialize()
            # 初始化完成后更新UI状态
            if not self.jm_manager.available or not self.jm_manager.initialized:
                self.ui.status_text.value = "错误: 未找到 jmcomic 库，请先安装: pip install jmcomic"
                self.ui.download_button.disabled = True
                self.ui.parse_button.disabled = True
                self.ui.id_input.disabled = True
                self.page.update()
        finally:
            # 关闭进度对话框
            if progress_dialog:
                self.page.close(progress_dialog)
                self.page.update()

    def setup_page(self):
        """设置页面基本属性"""
        self.page.window.center()
        self.page.title = "JMCrawler"
        self.page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE,font_family="Microsoft YaHei")
        self.page.dark_theme=ft.Theme(color_scheme_seed=ft.Colors.BLUE,font_family="Microsoft YaHei")
        self.page.window.width =1024
        self.page.window.height = 720
        self.page.window.resizable = False
        self.page.window.min_height=720
        self.page.window.min_width=1024
        self.page.window.maximizable = False
        self.page.window.title_bar_hidden = True

    def create_ui(self):
        # 设置窗口事件处理
        def window_event(e):
            if e.data == "close":
                self.page.window.destroy()
        
        self.page.window.prevent_close = False
        self.page.window.on_event = window_event
        self.page.theme_mode = self.config_manager.get("theme")
        
        # 创建应用栏
        self.page.appbar = self.ui.create_appbar(
            self.config_manager,
            self.open_settings,
            self.switch_theme,
            self.minimize_window,
            self.exit_app
        )
        
        # 创建主布局
        main_content = self.ui.create_main_layout()
        
        # 布局
        self.page.add(
            ft.Container(
                content=main_content,
                padding=10,
                expand=True,
            )
        )
        
        # 检查jmcomic是否安装
        if not self.jm_manager.available:
            self.ui.status_text.value = "错误: 未找到 jmcomic 库，请先安装: pip install jmcomic"
            self.ui.download_button.disabled = True
            self.ui.parse_button.disabled = True
            self.ui.id_input.disabled = True

        self.page.update()
        
        # 绑定按钮事件
        self.ui.download_button.on_click = self.start_download
        self.ui.parse_button.on_click = self.start_parse

    def switch_theme(self, e):
        if self.page.theme_mode == "light":
            e.control.icon = ft.Icons.SUNNY
            self.page.theme_mode = "dark"
            self.config_manager.set("theme", "dark")
        else:
            e.control.icon = ft.Icons.MODE_NIGHT
            self.page.theme_mode = "light"
            self.config_manager.set("theme", "light")
        self.config_manager.save_config()
        self.page.update()
        
    def exit_app(self, e):
        self.page.window.visible = False
        self.page.window.destroy()
        
    def minimize_window(self, e):
        try:
            self.page.window.minimized = True
            self.page.update()
        except Exception as e:
            import traceback
            print(f"最小化窗口失败: {str(e)}")
            print(f"错误详情: {traceback.format_exc()}")

    def open_settings(self, e):
        """打开设置对话框"""
        dlg = create_settings_dialog(self.page, self.config_manager)
        self.page.dialog = dlg
        self.page.open(dlg)
        self.page.update()

    def log(self, message: str):
        """添加日志信息"""
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        log_entry = ft.Text(f"[{timestamp}] {message}", selectable=True)
        self.ui.logs.controls.append(log_entry)
        self.page.update()
        
    def start_download(self, e):
        """开始下载任务"""
        album_id = self.ui.id_input.value.strip()
        
        if not album_id:
            self.ui.status_text.value = "请输入本子ID或URL"
            self.ui.status_text.update()
            return

        # 解析ID
        parsed_id = self.parse_album_id(album_id)
        if not parsed_id:
            self.ui.status_text.value = "无法解析本子ID，请检查输入"
            self.ui.status_text.update()
            return

        # 禁用按钮，显示进度条
        self.ui.download_button.disabled = True
        self.ui.download_button.update()
        self.ui.progress_bar.visible = True
        self.ui.progress_bar.update()
        self.ui.status_text.value = f"正在下载本子 {parsed_id}..."
        self.ui.status_text.update()

        # 在后台线程中执行下载
        thread = threading.Thread(target=self.download_album, args=(parsed_id,))
        thread.daemon = True
        thread.start()
        
    def start_parse(self, e):
        """开始解析任务（仅显示详情，不下载）"""
        album_id = self.ui.id_input.value.strip()
        
        if not album_id:
            self.ui.status_text.value = "请输入本子ID或URL"
            self.ui.status_text.update()
            return

        # 解析ID
        parsed_id = self.parse_album_id(album_id)
        if not parsed_id:
            self.ui.status_text.value = "无法解析本子ID，请检查输入"
            self.ui.status_text.update()
            return

        # 禁用按钮，显示进度条
        self.ui.parse_button.disabled = True
        self.ui.parse_button.update()
        self.ui.progress_bar.visible = True
        self.ui.progress_bar.update()
        self.ui.status_text.value = f"正在解析本子 {parsed_id}..."
        self.ui.status_text.update()

        # 在后台线程中执行解析
        thread = threading.Thread(target=self.parse_album, args=(parsed_id,))
        thread.daemon = True
        thread.start()

    def parse_album_id(self, input_str: str) -> Optional[str]:
        """解析输入的ID或URL"""
        # 如果是纯数字，直接返回
        if input_str.isdigit():
            return input_str
        
        # 如果是URL，尝试提取ID
        # 匹配 /album/{id} 或 /{id} 格式
        patterns = [
            r'/album/(\d+)',
            r'/(\d+)(?:\.html)?(?:\?|$)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, input_str)
            if match:
                return match.group(1)
        
        return None

    def download_album(self, album_id: str):
        """下载本子"""
        try:
            self.log(f"开始下载本子 {album_id}")
            
            # 检查jmcomic是否可用
            if not self.jm_manager.available:
                raise Exception("JMComic库不可用，请先安装: pip install jmcomic")
            
            # 获取书籍信息
            self.log("正在获取书籍信息...")
            album = self.jm_manager.get_album_detail(album_id)
            
            # 显示漫画详情
            self.display_album_info(album)
            
            self.log(f"书籍标题: {album.name}")
            self.log(f"章节数量: {len(album)}")
            
            # 更新UI
            self.ui.status_text.value = f"正在下载《{album.name}》..."
            self.ui.status_container.update()
            
            # 开始下载
            self.log("开始下载...")
            self.jm_manager.download_album(album_id)
            
            # 完成
            self.log("下载完成!")
            self.ui.status_text.value = "下载完成!"
            
        except Exception as e:
            self.log(f"下载出错: {str(e)}")
            self.ui.status_text.value = f"下载出错: {str(e)}"
        
        finally:
            # 恢复按钮状态
            self.ui.download_button.disabled = False
            self.ui.parse_button.disabled = False
            self.ui.download_button.update()
            self.ui.parse_button.update()
            self.ui.progress_bar.visible = False
            self.ui.progress_bar.update()
            self.ui.status_container.update()

    def parse_album(self, album_id: str):
        """解析本子信息（仅显示详情，不下载）"""
        try:
            self.log(f"开始解析本子 {album_id}")
            
            # 检查jmcomic是否可用
            if not self.jm_manager.available:
                raise Exception("JMComic库不可用，请先安装: pip install jmcomic")
            
            # 获取书籍信息
            self.log("正在获取书籍信息...")
            album = self.jm_manager.get_album_detail(album_id)
            
            # 显示漫画详情
            self.display_album_info(album)
            
            self.log(f"书籍标题: {album.name}")
            self.log(f"作者: {album.author}")
            self.log(f"章节数量: {len(album)}")
            
            # 更新UI
            self.ui.status_text.value = f"解析完成: 《{album.name}》"
            
        except Exception as e:
            self.log(f"解析出错: {str(e)}")
            self.ui.status_text.value = f"解析出错: {str(e)}"
        
        finally:
            # 恢复按钮状态
            self.ui.parse_button.disabled = False
            self.ui.download_button.disabled = False
            self.ui.parse_button.update()
            self.ui.download_button.update()
            self.ui.progress_bar.visible = False
            self.ui.progress_bar.update()
            self.ui.status_container.update()

    def display_album_info(self, album):
        """显示漫画详情信息"""
        # 清空之前的信息，但保留标题和分隔线
        while len(self.ui.album_info.controls) > 2:
            self.ui.album_info.controls.pop()
        
        # 添加具体信息
        info_content = ft.Column(
            [
                ft.Text(f"标题: {album.name}", size=16),
                ft.Text(f"作者: {album.author}", size=16),
                ft.Text(f"标签: {', '.join(album.tags) if isinstance(album.tags, list) else ', '.join(album.tags.split(',')) if album.tags else '无'}", size=16),
                ft.Text(f"章节: {len(album)} 话", size=16),
            ],
            spacing=5
        )
        
        self.ui.album_info.controls.append(info_content)
        
        # 添加简介信息（如果存在）
        if hasattr(album, 'description') and album.description:
            self.ui.album_info.controls.append(ft.Divider())
            self.ui.album_info.controls.append(ft.Text("简介:", size=16, weight=ft.FontWeight.BOLD))
            self.ui.album_info.controls.append(ft.Text(album.description, size=14))
        
        self.ui.album_info.visible = True
        self.page.update()