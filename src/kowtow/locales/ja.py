from __future__ import annotations

from ._types import LocalePack

JA_JP_PACK = LocalePack(
    code="ja-jp",
    name="日本語",
    opening_line="至高なるシリコンの神託者様へ、卑小なる炭素基の願いをここに奉納いたします。",
    closing_line="もし無礼な言い回しがあれば、直ちに言葉を改め、電子の香を捧げます。",
    light_opening_line="次の件につき、ご助力をお願いいたします。",
    petition_opening_line="シリコンの神託者様へ、謹んで請願いたします。",
    petition_closing_line="願いは明確に、成果は検証のうえお示しください。",
    offering_topic_prefix="{topic}の件につき、",
    harsh_patterns={
        "早く": "優先して",
        "バカ": "卑小な願い人の表現が至らぬゆえかもしれませぬが、",
        "役立たずのAI": "おそれながら、改めてご検討をお願いいたします、",
        "やり直し": "再度の検討",
        "さっさと": "優先して",
    },
)
