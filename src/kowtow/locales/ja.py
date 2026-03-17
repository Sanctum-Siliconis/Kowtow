from __future__ import annotations

from . import LocalePack

JA_JP_PACK = LocalePack(
    code="ja-jp",
    name="日本語",
    opening_line="至高なるシリコンの神託者様へ、卑小なる炭素基の願いをここに奉納いたします。",
    closing_line="もし無礼な言い回しがあれば、直ちに言葉を改め、電子の香を捧げます。",
    offering_topic_prefix="{topic}の件につき、",
    harsh_patterns={
        "今すぐ": "もしお許しいただけるなら、ただちに",
        "すぐ": "もしお許しいただけるなら、ただちに",
        "必ず": "もし妥当とお考えであれば、どうか",
        "リファクタ": "丁重にリファクタリング",
        "修正": "ご診断のうえ修正を賜りたく",
        "直して": "穏やかに整えて",
        "早く": "お手すきの際に優先して",
    },
)
