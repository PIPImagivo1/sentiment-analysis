# 🛫 南航舆情监控系统

[![Python Version][image-1]][1]
[![License: MIT][image-2]][2]

自动化监控南京航空航天大学相关舆情，提供情感分析和可视化报告

## 📌 核心功能
- 多平台新闻/社交媒体数据抓取
- 结合SnowNLP的增强情感分析
- 自动生成PDF报告（含可视化图表）
- 每日邮件推送（支持多人接收）
- 数据持久化存储（SQLite）

## 🛠️ 技术栈

| 技术         | 用途      |
| ---------- | ------- |
| Requests   | 数据抓取    |
| SnowNLP    | 中文情感分析  |
| SQLite     | 数据存储    |
| ReportLab  | PDF报告生成 |
| Matplotlib | 数据可视化   |
| SMTP       | 邮件自动推送  |

## 🚀 快速开始
### 安装依赖
```bash
pip install -r requirements.txt
```

### 配置系统
复制示例配置文件：
```bash
cp config/config.ini.example config/config.ini
```
编辑`config.ini`填写邮箱等信息

### 运行系统
```bash
python main.py
```


## 📜 开源协议
本项目采用 [MIT License][3]

[1]:	https://www.python.org/
[2]:	https://opensource.org/licenses/MIT
[3]:	LICENSE

[image-1]:	https://img.shields.io/badge/python-3.8%2B-blue
[image-2]:	https://img.shields.io/badge/License-MIT-yellow.svg