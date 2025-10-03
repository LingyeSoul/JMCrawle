import os
from typing import Optional
from option import OptionManager

try:
    import jmcomic
    from jmcomic import  JmModuleConfig
    JMCOMIC_AVAILABLE = True
except ImportError:
    JMCOMIC_AVAILABLE = False


class JMComicManager:
    def __init__(self):
        self.available = JMCOMIC_AVAILABLE
        self.option = None
        self.client = None
        self.initialized = False
    
    async def initialize(self):
        """异步初始化JMComic库"""
        if self.available:
            # 使用OptionManager加载配置
            option_manager = OptionManager()
            self.option = jmcomic.create_option_by_file(option_manager.option_path)
            self.client = self.option.build_jm_client()
            self.initialized = True
        else:
            self.option = None
            self.client = None
            self.initialized = False
    
    def get_album_detail(self, album_id):
        """获取漫画详情"""
        if not self.available or not self.client:
            raise Exception("JMComic库不可用")
        return self.client.get_album_detail(album_id)
    
    def download_album(self, album_id):
        """下载漫画"""
        if not self.available or not self.option:
            raise Exception("JMComic库不可用")
        jmcomic.download_album(album_id, self.option)
    
    def get_album_cover(self, album_id):
        return f'https://{JmModuleConfig.DOMAIN_IMAGE_LIST[0]}/media/albums/{album_id}.jpg'