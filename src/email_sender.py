import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import configparser

class EmailSender:
    def __init__(self, config_file='config.ini'):
        self.config = self._load_config(config_file)
        
    def _load_config(self, config_file):
        """从配置文件读取敏感信息"""
        config = configparser.ConfigParser()
        config.read(config_file)
        return {
            'smtp_server': config.get('email', 'smtp_server'),
            'smtp_port': config.getint('email', 'smtp_port'),
            'username': config.get('email', 'username'),
            'password': config.get('email', 'password')
        }
        
    def send_report(self, to_emails, attachment_path):
        """发送带附件的邮件"""
        msg = MIMEMultipart()
        msg['From'] = self.config['username']
        msg['To'] = ', '.join(to_emails)
        msg['Subject'] = f"南航舆情日报 {datetime.now().strftime('%Y-%m-%d')}"
        
        # 正文内容
        body = """
        <html>
          <body>
            <p>您好！</p>
            <p>附件为今日南航舆情分析报告，包含：</p>
            <ul>
              <li>情感分布分析</li>
              <li>热点关键词词云</li>
              <li>近期趋势统计</li>
            </ul>
            <p>系统自动发送，请勿直接回复。</p>
          </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))
        
        # 添加附件
        with open(attachment_path, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 
                          f'attachment; filename="{attachment_path}"')
            msg.attach(part)
            
        # 发送邮件
        try:
            with smtplib.SMTP_SSL(self.config['smtp_server'], self.config['smtp_port']) as server:
                server.login(self.config['username'], self.config['password'])
                server.sendmail(self.config['username'], to_emails, msg.as_string())
            print("邮件发送成功")
        except Exception as e:
            print(f"邮件发送失败: {str(e)}")

# 使用示例（需提前创建config.ini文件）
sender = EmailSender()
sender.send_report(
    to_emails=['professor@nuaa.edu.cn'], 
    attachment_path='daily_report.pdf'
)