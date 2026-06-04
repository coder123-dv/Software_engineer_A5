"""情感分析服务 - 简单规则+LLM双模式"""

import re


# 情感词典 (简化版)
POSITIVE_WORDS = {
    "好", "棒", "美", "赞", "喜欢", "开心", "满意", "漂亮", "壮观", "震撼",
    "精彩", "有趣", "感动", "惊艳", "推荐", "舒服", "值得", "完美", "太好了",
    "不错", "厉害", "优秀", "感谢", "谢谢",
}

NEGATIVE_WORDS = {
    "差", "烂", "坑", "贵", "挤", "脏", "累", "失望", "无聊", "不好",
    "难受", "生气", "讨厌", "垃圾", "太差", "糟糕", "不满", "投诉", "退款",
    "骗人", "坑人",
}


def analyze_sentiment(text: str) -> dict:
    """分析文本情感

    Returns:
        {"score": -1.0~1.0, "label": "positive/neutral/negative"}
    """
    if not text:
        return {"score": 0.0, "label": "neutral"}

    pos_count = sum(1 for w in POSITIVE_WORDS if w in text)
    neg_count = sum(1 for w in NEGATIVE_WORDS if w in text)

    total = pos_count + neg_count
    if total == 0:
        return {"score": 0.0, "label": "neutral"}

    score = (pos_count - neg_count) / total

    if score > 0.2:
        label = "positive"
    elif score < -0.2:
        label = "negative"
    else:
        label = "neutral"

    return {"score": round(score, 2), "label": label}


def get_expression_from_sentiment(sentiment: dict) -> str:
    """根据情感判断数字人表情"""
    label = sentiment.get("label", "neutral")
    score = abs(sentiment.get("score", 0))

    if label == "positive":
        return "happy"
    elif label == "negative":
        if score > 0.5:
            return "sad"
        return "relaxed"  # 轻微负面用平静表情
    return "neutral"
