from config import config

# 获取数据库路径
db_path = config.get('database', 'path')

# 获取邮件配置
smtp_settings = {
    'server': config.get('email', 'smtp_server'),
    'port': config.getint('email', 'smtp_port'),
    'user': config.get('email', 'username'),
    'password': os.environ.get('EMAIL_PASSWORD')  # 更安全的密码加载方式
}

# 使用日志配置
logging.basicConfig(
    filename=config.get('logging', 'file_path'),
    level=config.get('logging', 'level'),
    format='%(asctime)s - %(levelname)s - %(message)s'
)