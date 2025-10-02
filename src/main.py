import asyncio
import flet as ft
from app import JMComicApp


def main(page: ft.Page):
    app = JMComicApp(page)
    
    # 创建异步任务来初始化JMComicManager
    async def init_app():
        # 创建初始化进度对话框
        progress_dialog = ft.AlertDialog(
            content_padding=ft.padding.symmetric(vertical=20, horizontal=20),
            content=ft.Container(
                content=ft.Row(
                    [
                        ft.ProgressRing(width=50, height=50),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    #spacing=15,
                ),
                padding=50,
            ),
            modal=True,
        )
        
        # 先显示进度对话框
        page.open(progress_dialog)
        page.update()
        
        # 等待UI更新完成
        await asyncio.sleep(0)
        
        # 再执行初始化
        await app.initialize_jm_manager(progress_dialog)
    
    # 使用 page.run_task 来执行异步初始化，传递函数引用而不是调用结果
    page.run_task(init_app)

ft.app(target=main)