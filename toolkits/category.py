from dataclasses import dataclass
from typing import List


categories = {}


@dataclass
class Category:
    cate: str
    name: List[str]
    keywords: List[str]
    idx: int


def register_conv_template(template: Category, override: bool = False):
    """Register a new conversation template."""
    assert template.cate not in categories, f"{template.cate} has been registered."

    categories[template.cate] = template


register_conv_template(
    Category(
        idx=0,
        cate="chatbot",
        name=["对话聊天", "chatbot"],
        keywords=["聊天机器人", "聊天", "机器人", "对话", "智能体", "chatbot"],
    )
)

register_conv_template(
    Category(
        idx=19,
        cate="english",
        name=["学外语", "english"],
        keywords=["学外语", "english"],
    )
)


register_conv_template(
    Category(
        idx=1,
        cate="image",
        name=["图片生成", "image"],
        keywords=["扩散", "扩散生成", "扩散模型", "绘画", "图像编辑", "绘制", "视觉", "erase", "photo"],
    )
)
register_conv_template(
    Category(
        idx=1,
        cate="person",
        name=["人像编辑", "face"],
        keywords=["人脸", "face"],
    )
)
register_conv_template(
    Category(
        idx=2,
        cate="removebg",
        name=["背景移除", "removebg"],
        keywords=["图像编辑", "removebg", "背景", "background"],
    )
)


register_conv_template(
    Category(
        idx=3,
        cate="video",
        name=["视频编辑", "video"],
        keywords=["video", "视频"],
    )
)

register_conv_template(
    Category(
        idx=4,
        cate="voice",
        name=["语音合成", "tts"],
        keywords=["voice", "声音", "语音", "语音合成", "音乐", "歌声", "audio", "music"],
    )
)
register_conv_template(
    Category(
        idx=6,
        cate="text",
        name=["文字创作", "writing"],
        keywords=["text", "写作", "write", "writing", "改写", "纠错"],
    )
)
register_conv_template(
    Category(
        idx=5,
        cate="translate",
        name=["文字翻译", "translate"],
        keywords=["translate", "翻译"],
    )
)
register_conv_template(
    Category(
        idx=6,
        cate="PowerPoint",
        name=["幻灯片", "ppt"],
        keywords=["幻灯片", "ppt", "powerpoint", "presentation", "slide"],
    )
)
register_conv_template(
    Category(
        idx=7,
        cate="excel",
        name=["表格", "excel"],
        keywords=["表格", "excel"],
    )
)

register_conv_template(
    Category(
        idx=8,
        cate="pdf",
        name=["PDF", "PDF"],
        keywords=["pdf", "pdf"],
    )
)

register_conv_template(
    Category(
        idx=10,
        cate="code",
        name=["编程助手", "code"],
        keywords=["code", "代码", "coder", "编程", "coding", "debug"],
    )
)

register_conv_template(
    Category(
        idx=9,
        cate="note",
        name=["记笔记", "note"],
        keywords=["笔记", "note"],
    )
)

register_conv_template(
    Category(
        idx=11,
        cate="design",
        name=["设计", "design"],
        keywords=["设计", "design", "logo"],
    )
)


# register_conv_template(
#     Category(
#         cate="infer",
#         name=["推理", "infer"],
#         keywords=["推理", "infer"],
#     )
# )


# register_conv_template(
#     Category(
#         cate="train",
#         name=["训练", "train"],
#         keywords=["训练", "train"],
#     )
# )

register_conv_template(
    Category(
        idx=17,
        cate="medician",
        name=["医药", "medical"],
        keywords=["医药", "medical"],
    )
)

register_conv_template(
    Category(
        idx=16,
        cate="academic",
        name=["学术", "academic"],
        keywords=["学术", "academic"],
    )
)

register_conv_template(
    Category(
        idx=13,
        cate="digital",
        name=["数字人", "digital"],
        keywords=["数字人", "digital"],
    )
)


# register_conv_template(
#     Category(
#         idx=12,
#         cate="dataset",
#         name=["数据集", "dataset"],
#         keywords=["data", "dataset"],
#     )
# )

register_conv_template(
    Category(
        idx=14,
        cate="prompt",
        name=["提示词", "prompt"],
        keywords=["提示词", "prompt"],
    )
)

register_conv_template(
    Category(
        idx=14,
        cate="detector",
        name=["AI检测器", "detector"],
        keywords=["检测器", "detector"],
    )
)

register_conv_template(
    Category(
        idx=100,
        cate="eval",
        name=["排行榜", "eval"],
        keywords=["评估", "eval", "bench", "measur"],
    )
)

register_conv_template(
    Category(
        idx=150,
        cate="other",
        name=["其它", "other"],
        keywords=[],
    )
)
