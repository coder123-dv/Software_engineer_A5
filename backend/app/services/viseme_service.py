"""Viseme 服务 - 文本转口型时间轴"""

from pypinyin import pinyin, Style

from app.schemas.chat import VisemeKeyframe

# 拼音韵母 → Viseme 映射 (基于OVR标准)
PINYIN_TO_VISEME = {
    # 开口音
    "a": "aa", "ai": "aa", "an": "aa", "ang": "aa", "ao": "aa",
    # 圆唇音
    "o": "oh", "ou": "oh", "ong": "oh",
    # 展唇音
    "e": "ee", "ei": "ee", "en": "ee", "eng": "ee", "er": "ee",
    # 齐齿音
    "i": "ih", "in": "ih", "ing": "ih",
    # 合口音
    "u": "ou", "un": "ou",
    # 撮口音
    "v": "ou", "ü": "ou", "vn": "ou",
    # 特殊
    "zh": "ch", "ch": "ch", "sh": "ch", "r": "rr",
    "z": "ss", "c": "ss", "s": "ss",
    "b": "pp", "p": "pp", "m": "pp",
    "f": "ff",
    "d": "dd", "t": "dd", "n": "nn", "l": "nn",
    "g": "kk", "k": "kk", "h": "kk",
    "j": "ch", "q": "ch", "x": "ch",
}

# 每个字的平均时长（秒），中文语速约 4-5 字/秒
CHAR_DURATION = 0.22


def text_to_viseme_timeline(text: str, start_time: float = 0.0) -> list[VisemeKeyframe]:
    """将中文文本转换为 Viseme 口型时间轴

    Args:
        text: 中文文本
        start_time: 起始时间偏移

    Returns:
        Viseme关键帧列表
    """
    if not text:
        return []

    timeline = []
    current_time = start_time

    # 获取拼音
    py_list = pinyin(text, style=Style.TONE3, heteronym=False)

    for i, (char, py) in enumerate(zip(text, py_list)):
        py_str = py[0] if py else ""

        # 跳过标点符号（插入静音帧）
        if not py_str or not py_str[0].isalpha():
            timeline.append(VisemeKeyframe(time=round(current_time, 3), viseme="sil", weight=0.0))
            current_time += 0.15  # 标点停顿
            continue

        # 去除声调数字
        py_clean = py_str.rstrip("12345")

        # 提取声母和韵母
        initial, final = _split_pinyin(py_clean)

        # 声母对应的 viseme（持续较短）
        if initial and initial in PINYIN_TO_VISEME:
            timeline.append(VisemeKeyframe(
                time=round(current_time, 3),
                viseme=PINYIN_TO_VISEME[initial],
                weight=0.6,
            ))
            current_time += CHAR_DURATION * 0.3

        # 韵母对应的 viseme（持续较长，权重更大）
        viseme = _get_final_viseme(final)
        timeline.append(VisemeKeyframe(
            time=round(current_time, 3),
            viseme=viseme,
            weight=0.9,
        ))
        current_time += CHAR_DURATION * 0.7

    # 末尾添加闭口帧
    timeline.append(VisemeKeyframe(time=round(current_time, 3), viseme="sil", weight=0.0))

    return timeline


def _split_pinyin(py: str) -> tuple[str, str]:
    """拆分拼音为声母和韵母"""
    initials = [
        "zh", "ch", "sh", "b", "p", "m", "f", "d", "t", "n", "l",
        "g", "k", "h", "j", "q", "x", "r", "z", "c", "s", "y", "w",
    ]
    for init in initials:
        if py.startswith(init):
            return init, py[len(init):]
    return "", py


def _get_final_viseme(final: str) -> str:
    """获取韵母对应的 viseme"""
    if not final:
        return "sil"
    # 优先匹配完整韵母
    if final in PINYIN_TO_VISEME:
        return PINYIN_TO_VISEME[final]
    # 匹配第一个元音
    for char in final:
        if char in PINYIN_TO_VISEME:
            return PINYIN_TO_VISEME[char]
    return "aa"  # 默认开口
