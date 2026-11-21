# ============================================================
#  日本語化MOD 配線ファイル
#  1) 表示言語を japanese に固定
#  2) 同梱の DreamHanSans（中国語書体）を J 面（日本語グリフ）で描画
#  3) 名札をカタカナへ差し替え（Character の name は文字列翻訳を通らないため）
#  本体ファイルは変更しない。tl/japanese/ とこのファイルを追加するだけ。
# ============================================================

define config.language = "japanese"

# NVL の名札列は既定 200px。カタカナ 5 文字（約 230px）が折り返すため広げる。
style nvl_label:
    xsize 250
    min_width 250

init -1 python:
    for _f in (
        "font/DreamHanSans-W10.ttc",
        "font/DreamHanSans-W15.ttc",
        "font/DreamHanSans-W20.ttc",
        "font/DreamHanSans-W25.ttc",
    ):
        # TTC の 3 番目（0 始まり）が日本語面
        config.font_replacement_map[(_f, False, False)] = ("3@" + _f, False, False)

init 100 python:
    _ja_name_map = {
        "路正": "ルージョン",
        "安冉": "アンラン",
        "王子明": "ワンズミン",
        "陈教授": "チェン教授",
        "老师": "先生",
        "司机": "運転手",
        "路人": "通行人",
        "男生": "男子",
        "外卖": "配達員",
        "两人": "二人",
        "？？": "？？？",
    }
    for _v in (
        "Luzheng", "Luzheng_s",
        "Anran", "Anran_s",
        "Wang", "Wang_s",
        "Chen", "Chen_s",
        "Laoshi", "Laoshi_s",
        "Siji", "Luren", "Luren_s",
        "Nansheng", "Nansheng_s",
        "Waimai", "Al", "Weizhi",
    ):
        _o = getattr(store, _v, None)
        if _o is not None and getattr(_o, "name", None) in _ja_name_map:
            _o.name = _ja_name_map[_o.name]
