import yaml
import os


class OptionManager:
    def __init__(self, option_path=None):
        """
        初始化选项管理器
        
        Args:
            option_path (str, optional): 选项配置文件路径，默认为当前目录下的option.yml
        """
        if option_path is None:
            self.option_path = os.path.join(os.getcwd(), "option.yml")
        else:
            self.option_path = option_path
            
        # 确保download目录存在
        download_dir = os.path.join(os.getcwd(), "download")
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
            
        self.default_option = {
            "dir_rule": {
                "base_dir": download_dir,
                "rule": "JM{Aid}-{Atitle}/{Pid}-{Ptitle}"
            },
            "plugins": {
                "after_album": [
                    {
                        "plugin": "img2pdf",
                        "kwargs": {
                            "filename_rule": "JM{Aid}-{Atitle}",
                            "pdf_dir": download_dir
                        }
                    },
                    {
                        "plugin": "long_img",
                        "kwargs": {
                            "filename_rule": "JM{Aid}-{Atitle}",
                            "pdf_dir": download_dir
                        }
                    }
                ],
                "before_album": [
                    {
                        "plugin": "download_cover",
                        "kwargs": {
                            "size": "_3x4",
                            "dir_rule": {
                                "base_dir": download_dir,
                                "rule": "{Atitle}/{Aid}_cover.jpg"
                            }
                        }
                    }
                ],
                "before_photo": [
                    {
                        "plugin": "skip_photo_with_few_images",
                        "kwargs": {
                            "at_least_image_count": 3
                        }
                    }
                ]
            }
        }
        self.option = self.load_option()
        
    def load_option(self):
        """
        加载选项配置文件
        
        Returns:
            dict: 选项字典
        """
        # 如果选项配置文件不存在，创建默认配置
        if not os.path.exists(self.option_path):
            self.save_option(self.default_option)
            return self.default_option
        
        # 读取现有选项配置
        try:
            with open(self.option_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or self.default_option
        except Exception as e:
            # 如果读取失败，返回默认配置
            return self.default_option
    
    def save_option(self, option_data=None):
        """
        保存选项到文件
        
        Args:
            option_data (dict, optional): 要保存的选项数据，默认使用实例中的option
        """
        if option_data is None:
            option_data = self.option
            
        # 处理plugins字段：如果没有启用任何插件，则删除plugins字段
        processed_option_data = option_data.copy()
        if "plugins" in processed_option_data:
            plugins = processed_option_data["plugins"]
            # 检查是否有任何启用的插件
            has_enabled_plugin = False
            for plugin_section in plugins.values():
                if plugin_section:  # 如果插件列表不为空
                    has_enabled_plugin = True
                    break
            
            # 如果没有任何启用的插件，删除plugins字段
            if not has_enabled_plugin:
                del processed_option_data["plugins"]
            
        try:
            with open(self.option_path, "w", encoding="utf-8") as f:
                yaml.dump(processed_option_data, f, allow_unicode=True, default_flow_style=False, indent=2, sort_keys=False)
        except Exception as e:
            raise Exception(f"保存选项文件失败: {str(e)}")
            
    def get(self, key_path, default=None):
        """
        根据路径获取配置值
        
        Args:
            key_path (str): 配置项路径，如 "dir_rule.base_dir"
            default: 默认值
            
        Returns:
            配置项的值
        """
        keys = key_path.split(".")
        value = self.option
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
            
    def set(self, key_path, value):
        """
        根据路径设置配置值
        
        Args:
            key_path (str): 配置项路径，如 "dir_rule.base_dir"
            value: 要设置的值
        """
        keys = key_path.split(".")
        target = self.option
        
        # 遍历到倒数第二个键，确保路径存在
        for key in keys[:-1]:
            if key not in target:
                target[key] = {}
            target = target[key]
            
        # 设置最后一个键的值
        target[keys[-1]] = value