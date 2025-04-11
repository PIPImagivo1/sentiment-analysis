class NewsDatabase:
    def __init__(self, db_path='nuaa_news.db'):
        self.conn = sqlite3.connect(db_path)
        self._init_table()
        
    def _init_table(self):
        """优化后的表结构"""
        self.conn.execute('''CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT,
            title TEXT UNIQUE,
            url TEXT,
            content TEXT,
            publish_time DATETIME,
            source TEXT,
            crawl_time DATETIME,
            sentiment_score REAL,
            sentiment_label TEXT,
            is_analyzed INTEGER DEFAULT 0
        )''')
        self.conn.commit()
        
    def save_data(self, df):
        """批量插入数据"""
        df.to_sql('temp', self.conn, if_exists='replace')
        
        # 使用SQL合并数据（避免重复）
        self.conn.execute('''
            INSERT OR IGNORE INTO news 
            (keyword, title, url, content, publish_time, source, crawl_time)
            SELECT keyword, title, url, content, publish_time, source, crawl_time
            FROM temp
        ''')
        self.conn.commit()
        
    def get_unanalyzed_data(self):
        """获取待分析数据"""
        return pd.read_sql('SELECT * FROM news WHERE is_analyzed=0', self.conn)

    def update_analysis(self, record_id, score, label):
        """更新分析结果"""
        self.conn.execute('''
            UPDATE news SET 
            sentiment_score=?,
            sentiment_label=?,
            is_analyzed=1 
            WHERE id=?
        ''', (score, label, record_id))
        self.conn.commit()
        
    def __del__(self):
        self.conn.close()

# 使用示例
db = NewsDatabase()
db.save_data(df_news)