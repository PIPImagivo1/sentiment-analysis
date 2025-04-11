import os
import configparser
from pathlib import Path

class ConfigLoader:
    def __init__(self):
        self.config = configparser.ConfigParser()
        config_path = Path(__file__).parent / 'config.ini'
        
        if not config_path.exists():
            example_path = Path(__file__).parent / 'config.ini.example'
            raise FileNotFoundError(
                f"请复制 {example_path} 为 config.ini 并填写配置"
            )
            
        self.config.read(config_path, encoding='utf-8')
        
        # 环境变量覆盖（优先级最高）
        if 'DB_PASSWORD' in os.environ:
            self.config['database']['password'] = os.environ['DB_PASSWORD']

    def get(self, section, key):
        return self.config.get(section, key)
    
    def getint(self, section, key):
        return self.config.getint(section, key)
    
    def getfloat(self, section, key):
        return self.config.getfloat(section, key)

# 单例配置对象
config = ConfigLoader()