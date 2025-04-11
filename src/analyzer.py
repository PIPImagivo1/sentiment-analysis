from snownlp import SnowNLP
import jieba.analyse

class SentimentAnalyzer:
    def __init__(self):
        # 加载南航相关领域词典（示例）
        self._load_domain_words()
        
    def _load_domain_words(self):
        """加载领域关键词（提升分析准确度）"""
        domain_words = ["航空", "发动机", "无人机", "航天", "南航", "NUAA"]
        for word in domain_words:
            SnowNLP.user_words.append(word)
            
    def _extract_keywords(self, text):
        """提取文本关键词（辅助分析）"""
        return jieba.analyse.extract_tags(text, topK=5)
        
    def analyze(self, text):
        """增强版情感分析"""
        if not text.strip():
            return 0.5, "neutral"
            
        s = SnowNLP(text)
        score = s.sentiments
        
        # 结合关键词调整分数
        keywords = self._extract_keywords(text)
        if any(kw in ["事故", "投诉", "失败"] for kw in keywords):
            score *= 0.7  # 负面词降权
        elif any(kw in ["成功", "突破", "获奖"] for kw in keywords):
            score *= 1.3  # 正面词加权
            
        score = max(0, min(1, score))  # 确保在0-1范围内
        
        # 添加标签
        if score > 0.6:
            label = "positive"
        elif score < 0.4:
            label = "negative"
        else:
            label = "neutral"
            
        return round(score, 4), label

# 批量分析函数
def batch_analyze(db):
    analyzer = SentimentAnalyzer()
    unanalyzed_data = db.get_unanalyzed_data()
    
    for _, row in unanalyzed_data.iterrows():
        # 结合标题和正文分析
        combined_text = f"{row['title']}。{row['content']}"
        score, label = analyzer.analyze(combined_text)
        db.update_analysis(row['id'], score, label)

# 执行分析
db = NewsDatabase()
batch_analyze(db)