import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
from urllib.parse import urlparse
import time
import random
from datetime import datetime, timedelta

class NUAA_Spider:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Encoding": "gzip, deflate"
        }
        self.session = requests.Session()
        
    def fetch_article_content(self, url):
        """抓取正文内容（适配常见新闻网站）"""
        try:
            domain = urlparse(url).netloc
            resp = self.session.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(resp.text, 'lxml')
            
            # 针对不同网站的正文提取规则
            if 'sina.com.cn' in domain:
                content = ' '.join([p.get_text() for p in soup.select('.article p')])
            elif '163.com' in domain:
                content = ' '.join([p.get_text() for p in soup.select('.post_text p')])
            else:  # 通用规则
                content = ' '.join([p.get_text() for p in soup.find_all('p')])
            
            return content[:2000]  # 限制长度避免数据库过大
        except Exception as e:
            print(f"正文抓取失败 {url}: {str(e)}")
            return ""

    def search_news(self, keywords):
        """改进的搜狗新闻搜索"""
        news_data = []
        
        for keyword in keywords:
            print(f"搜索关键词: {keyword}")
            url = f"https://news.sogou.com/news?query={quote(keyword)}&time=7"
            
            try:
                time.sleep(random.uniform(1, 3))
                resp = self.session.get(url, headers=self.headers, timeout=15)
                soup = BeautifulSoup(resp.text, 'lxml')
                
                for article in soup.select('.vrwrap'):
                    title = article.select_one('h3 a').get_text(strip=True)
                    link = article.select_one('h3 a')['href']
                    
                    # 抓取正文（新增）
                    content = self.fetch_article_content(link)
                    
                    news_data.append({
                        'keyword': keyword,
                        'title': title,
                        'url': link,
                        'content': content,  # 新增字段
                        'publish_time': self.parse_time(article),
                        'source': self.parse_source(article),
                        'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
                    
            except Exception as e:
                print(f"搜索出错 {keyword}: {str(e)}")
                
        return pd.DataFrame(news_data).drop_duplicates(subset=['title', 'url'])

    @staticmethod
    def parse_time(article):
        """标准化时间解析"""
        # 实现原有时间解析逻辑...
        pass

    @staticmethod
    def parse_source(article):
        """来源解析"""
        # 实现原有来源解析逻辑...
        pass

# 使用示例
spider = NUAA_Spider()
df_news = spider.search_news(["****", "****"])