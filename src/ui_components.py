import flet as ft


class UIComponents:
    def __init__(self, page: ft.Page):
        self.page = page
        self.id_input = None
        self.download_button = None
        self.parse_button = None
        self.progress_bar = None
        self.status_text = None
        self.status_container = None
        self.logs = None
        self.view = None
        self.album_info = None
        self.create_all_components()
    
    def create_all_components(self):
        """创建所有UI组件"""
        self.create_input_components()
        self.create_info_components()
        self.create_log_components()
    
    def create_input_components(self):
        """创建输入相关组件"""
        # ID输入框
        self.id_input = ft.TextField(
            label="请输入本子ID或URL",
            hint_text="例如: 422866 或 https://jmcomic.me/album/422866",
            width=500,
            border_radius=8,
        )

        # 下载按钮
        self.download_button = ft.ElevatedButton(
            "下载", 
            icon=ft.Icons.DOWNLOAD,
            width=150,
            height=40,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
            )
        )
        
        # 解析按钮
        self.parse_button = ft.ElevatedButton(
            "解析", 
            icon=ft.Icons.INFO,
            width=150,
            height=40,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
            )
        )

        # 进度条
        self.progress_bar = ft.ProgressBar(
            width=500,
            visible=False,
            border_radius=10,
        )

        # 状态文本
        self.status_text = ft.Text("", size=14)
        
        # 包装状态文本以支持滚动
        self.status_container = ft.Container(
            content=ft.Column(
                controls=[self.status_text],
                scroll=ft.ScrollMode.AUTO,  # 启用垂直滚动
                spacing=5,
            ),
            height=60,  # 设置固定高度，足以显示2-3行文本
            width=500,
        )
    
    def create_log_components(self):
        """创建日志相关组件"""
        # 日志区域
        self.logs = ft.ListView(
            expand=True,
            spacing=5,
            auto_scroll=True,
            padding=10
        )
        # 初始化启动时间戳
        self.view = ft.Column([
            ft.Container(
                content=self.logs,
                border=ft.border.all(1, ft.Colors.GREY_400),
                padding=15,
                expand=True,
            )
        ])
    
    def create_info_components(self):
        """创建信息展示组件"""
        # 漫画详情信息区域
        self.album_info = ft.Column(
            [
                ft.Text("漫画详情", size=18, weight=ft.FontWeight.BOLD),
                ft.Divider(),
            ],
            spacing=10,
            visible=True,  # 默认可见
            scroll=ft.ScrollMode.AUTO,  # 添加滚动功能
        )
    
    def create_appbar(self, config_manager, open_settings_handler, switch_theme_handler, minimize_window_handler, exit_app_handler):
        """创建应用栏"""
        # 设置主题图标
        if config_manager.get("theme") == "light":
            theme_icon = ft.Icons.MODE_NIGHT
        else:
            theme_icon = ft.Icons.SUNNY   
        
        return ft.AppBar(
            title=ft.WindowDragArea(content=ft.Text("JMCrawler"), width=800),
            center_title=False,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            actions=[
                ft.IconButton(icon=ft.Icons.SETTINGS, on_click=open_settings_handler, icon_size=30),
                ft.IconButton(icon=theme_icon, on_click=switch_theme_handler, icon_size=30),
                ft.IconButton(ft.Icons.MINIMIZE, on_click=minimize_window_handler, icon_size=30),
                ft.IconButton(ft.Icons.CANCEL_OUTLINED, on_click=exit_app_handler, icon_size=30),
            ],
        )
    
    def create_main_layout(self):
        """创建主布局"""
        # 创建一个美观的卡片容器来放置输入组件
        input_card = ft.Card(
            content=ft.Container(
                content=ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Row([self.id_input,
                                ft.Container(
                                    content=ft.Row([self.download_button, self.parse_button], spacing=10),
                                    alignment=ft.alignment.bottom_center,
                                    padding=15,
                                ),]),
                                self.progress_bar,
                                self.status_container,
                            ],
                            spacing=15,
                            horizontal_alignment=ft.CrossAxisAlignment.START,
                        ),
                        
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    expand=True,
                ),
                padding=15,
                expand=True,
            ),
            margin=ft.margin.only(bottom=10),
        )
        
        # 创建漫画详情卡片
        album_info_card = ft.Card(
            content=ft.Container(
                content=self.album_info,
                padding=15,
                expand=True,
            ),
            margin=ft.margin.only(bottom=10),
        )
        
        # 创建日志信息卡片
        logs_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Text("日志信息:", size=18, weight=ft.FontWeight.BOLD),
                        padding=ft.padding.only(bottom=10),
                    ),
                    ft.Container(
                        content=self.view,
                        expand=True,
                    )
                ]),
                padding=15,
                expand=True,
            ),
            margin=ft.margin.only(bottom=10),  # 统一添加底部边距
        )
        
        # 使用Row和Column组合来更好地控制布局
        main_content = ft.Column(
            [
                ft.Container(
                    content=input_card,
                    height=180,
                ),
                ft.Container(
                    content=album_info_card,
                    height=220,
                ),
                ft.Container(
                    content=logs_card,
                    expand=True,
                ),
            ],
            spacing=0,
            expand=True,
        )
        
        return main_content