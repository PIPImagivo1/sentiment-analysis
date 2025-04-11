import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

class ReportGenerator:
    def __init__(self, db_path):
        self.db = NewsDatabase(db_path)
        self.styles = getSampleStyleSheet()
        
    def generate_plots(self):
        """生成统计图表"""
        df = pd.read_sql('SELECT * FROM news', self.db.conn)
        
        # 情感分布图
        plt.figure(figsize=(10, 4))
        df['sentiment_label'].value_counts().plot.bar(color=['green', 'gray', 'red'])
        plt.title('情感分布')
        plt.savefig('sentiment_dist.png')
        
        # 关键词词云（需安装wordcloud库）
        self._generate_wordcloud(df)
        
    def _generate_wordcloud(self, df):
        """生成词云图"""
        from wordcloud import WordCloud
        text = ' '.join(df['title'] + ' ' + df['content'].str[:100])
        wc = WordCloud(font_path='simhei.ttf', width=800, height=400).generate(text)
        wc.to_file('wordcloud.png')
        
    def generate_pdf(self):
        """生成PDF报告"""
        doc = SimpleDocTemplate("daily_report.pdf", pagesize=A4)
        elements = []
        
        # 标题
        elements.append(Paragraph("南航舆情日报", self.styles['Title']))
        elements.append(Spacer(1, 12))
        
        # 统计摘要
        stats = self._get_stats()
        elements.append(Paragraph(stats, self.styles['BodyText']))
        
        # 插入图表
        elements.append(Image('sentiment_dist.png', width=400, height=200))
        elements.append(Image('wordcloud.png', width=500, height=250))
        
        doc.build(elements)
        return "daily_report.pdf"
        
    def _get_stats(self):
        """生成统计文本"""
        df = pd.read_sql('''
            SELECT 
                COUNT(*) as total,
                AVG(sentiment_score) as avg_score,
                SUM(CASE WHEN sentiment_label='positive' THEN 1 ELSE 0 END) as pos_count
            FROM news
            WHERE date(publish_time) >= date('now', '-7 days')
        ''', self.db.conn)
        
        return f"""
        统计周期: 最近7天
        总新闻量: {df.iloc[0]['total']}
        平均情感分数: {df.iloc[0]['avg_score']:.2f}
        正面新闻占比: {df.iloc[0]['pos_count']/df.iloc[0]['total']:.1%}
        """

# 使用示例
report = ReportGenerator('nuaa_news.db')
report.generate_plots()
report.generate_pdf()