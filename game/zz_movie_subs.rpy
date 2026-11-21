# -*- coding: utf-8 -*-
# 冒頭ムービーの焼き込み中国語字幕への日本語オーバーレイ（**D案・2026-11-21 に変更**）
#
#   方針（計画書 §6.8 の A案 → §6.17 で D案へ変更・ユーザー決定）:
#     - 動画ファイル（movie/LoveSong.webm = op）は一切変更しない。
#     - MOD 側で `image op` を再定義し、Movie の上に**日本語テキストだけを重ねる（黒帯なし）**。
#       置き場所は**焼き込み中国語の直上 y=914**（歌詞の焼き込みは y≈991..1044 に実測。
#       44px の本文＋縁取りで 914..978 になり、中国語と隙間なく重ならない）。
#       （.rpy はパス順に init されるため、zz_movie_subs.rpy の定義は後勝ち。
#         本体の定義は rpy/pic.rpy:69）
#     - **焼き込み中国語は隠さない**（D案の狙いは映像を伏せないこと。二重表示になる）。
#     - 取り消しは game/zz_movie_subs.rpy を消すだけ（追加ファイルのみ・本体無変更）。
#     - 黒帯へ戻すには下の `MOVIE_BAND = True` にする（生成器 work/_scratch/movie/gen_subs_rpy.py）。
#
#   実測（2026-11-20／2026-11-21 追記）:
#     - op = movie/LoveSong.webm 86.266 秒 / 1920x1080。
#       使われ方は rpy/scripts/script.rpy:120 の `scene op onlayer background`
#       ＋直後の `$ renpy.pause(85, hard=True)`（会話なしの固定窓）。
#     - 焼き込み字幕の行域: **y≈985..1050**（tools/subgeo.py でフルフレーム実測:
#       t=21.0 で y=991..1044 / t=13.5・45.0 でも下端は 1044 前後）。
#     - **上部の空き（D案の実測）**: `tools/subgeo.py --top` を work/shots/movie の19枚に実行 →
#       t=24.0・26.0 に text rows y=153..276（画面 px／ game y≈124..223）＝クレジット
#       （剧本／分鏡 の2行）。t=28.0 以降は行が立たない（右側の単発クレジットは列のみ検出）。
#       → 日本語テロップは **game y=30 段**に置けばクレジット（124..223）と重ならない。
#     - 旧A案の黒帯（y=955..1065・#000000f2）は**焼き込みを隠すため**に入れていた
#       （90% `#000000e6` では白文字が読めた実測あり）。D案では帯を置かない。
#     - 中央寄せ: Text に `xalign=0.5` を入れても Composite の子は左上に出た（実測）→
#       `Position(Text(...), xanchor=0.5)` で 960 位置に置く。
#     - op の歌テロップは 12.4〜71.8 秒の 19 行だけ（work/_scratch/movie/segs2_op.tsv で区間実測）。
#       72.4 秒以降はスタッフクレジット（`视频 Gusaya` 等・右側）で歌詞ではないため伏せない。
#     - ED（movie/ED.webm 98.4秒）には**焼き込みの歌字幕が無い**（下部帯中央の文字インク量が
#       0〜49秒で 0、50秒以降は右側のスタッフクレジット列とイラスト縁取りと判明）。
#       → ED は再定義しない（伏せる対象が無い＝クレジットもそのまま読める）。ED 曲名は
#       画面表記の実測で《MoeMoe》（混音 FEI）。
#
#   実装の形（Ren'Py 8.5 での実測で確定・詳細は gen_subs_rpy.py の docstring）:
#     - 黒帯は `Composite((1920, 110), (0,0), Solid("#000000e6"))`
#       （`Solid(幅, 高さ, color=…)` は TypeError、`Window(xsize=…)` はレンダリングで落ちる）
#     - 字幕ブロックは 1920x1080 の Composite に帯と Text を乗せたもの
#     - ATL の `contains` は**子の差し替え**なので、動画は別の層（Composite の下）に置く。
#       字幕の出入りは `time` ＋ `contains 字幕ブロック / contains Null()` で切り替える。
#
#   ※ このファイルは work/_scratch/movie/gen_subs_rpy.py が
#     work/_scratch/movie/op_lyrics.tsv（転写台帳＝秒数と訳の権威）から生成した。

init python:
    MOVIE_W = 1920
    MOVIE_H = 1080
    MOVIE_BAND = False          # D案（2026-11-21・ユーザー決定）: 黒帯を置かない。True で A案へ戻す
    MOVIE_BAND_Y = 955          # （A案の名残）伏せる帯の上端 955..1065
    MOVIE_BAND_H = 110
    MOVIE_TEXT_Y = 914          # D案: 日本語は**焼き込み中国語の直上**（CN 実測 991..1044 → 44px の本文で 914..978＋縁取り）
    MOVIE_FONT = "font/DreamHanSans-W15.ttc"   # 本体同梱。zz_ja_mod.rpy が J 面へ差し替える
    MOVIE_FONT_SIZE = 44
    # 帯が無い分は縁取りで可読性を確保する（実測: 44px・白文字／黒縁 4px＋右下へ影 2px）
    MOVIE_OUTLINES = [(4, "#000000", 0, 0), (2, "#000000", 3, 3)]

    def movie_band(color="#000000f2"):
        """焼き込み字幕をおおう黒帯（サイズは Composite で与える）。"""
        return Composite((MOVIE_W, MOVIE_BAND_H), (0, 0), Solid(color))

    def movie_cap(txt):
        """日本語テキスト（D案は黒帯なし）を 1920x1080 の箱に乗せた字幕ブロック。

           中央寄せ: Composite は子 を `Position(xpos=…, xanchor=0)` で包むので、
           Text に xalign=0.5 を入れても左上に出た（実測 op_740_after）。
           自前の Fixed 箱の子は **自身の位置スタイルで置かれる**（layout.py:909
           `child.place(...)`）→ Fixed に直接 add して xalign=0.5 で中央寄せする。
           （store の `Position` は curried 版で表示要素にならない＝実測で例外）"""
        box = Fixed(xsize=MOVIE_W, ysize=MOVIE_H)
        if MOVIE_BAND:
            box.add(Composite((MOVIE_W, MOVIE_BAND_H), (0, 0),
                              Solid("#000000f2"), yoffset=MOVIE_BAND_Y))
        box.add(Text(txt, font=MOVIE_FONT, size=MOVIE_FONT_SIZE,
                     color="#ffffff", outlines=MOVIE_OUTLINES,
                     xalign=0.5, yoffset=MOVIE_TEXT_Y))
        return box


# 本体の定義（rpy/pic.rpy:69）を仕切り直して重ねる
image op_movie = Movie(play="movie/LoveSong.webm")

# op: 字幕の入り切りで字幕ブロックだけを入れ替える（contains は子の差し替え）
#     animation: 毎フレーム評価させる（time での切り替えが show 時に1回で止まるのを防ぐ）
image op_caption:
    animation
    time 12.4
    contains movie_cap("一時停止キーを押して")
    time 14.6
    contains movie_cap("夜色をあけるから、もたれていい")
    time 17.4
    contains Null()
    time 17.8
    contains movie_cap("すぐ悩まないで")
    time 20.2
    contains movie_cap("あなたが笑うとき、光がいちばん綺麗")
    time 23.2
    contains movie_cap("心はこっそり跳ねてる")
    time 25.2
    contains movie_cap("時よ、そんなに速く駆け足にならないで")
    time 28.4
    contains movie_cap("私はあなたの手を握る")
    time 31.4
    contains movie_cap("離さない、話さない、微笑む")
    time 33.4
    contains Null()
    time 39.4
    contains movie_cap("あなたが私とサビを歌ってくれる")
    time 43.6
    contains movie_cap("風が古いレコードをめくる")
    time 45.2
    contains movie_cap("陽光がまつ毛のあいだを抜けていく")
    time 47.4
    contains movie_cap("遠くから届く、ささやかな約束みたいに")
    time 50.8
    contains movie_cap("あなたに近づいて願いをかける")
    time 52.6
    contains movie_cap("見上げれば花火、見下ろせば残り火")
    time 56.2
    contains movie_cap("あなたは小さく言う。私のために心臓が鳴ってるって")
    time 60.6
    contains movie_cap("恋は、映画のように瞬く")
    time 63.2
    contains movie_cap("台詞は考えなくていい")
    time 66.0
    contains movie_cap("こうして静止したこの瞬間に")
    time 68.2
    contains movie_cap("流れていく時を、すべて留める")
    time 71.8
    contains Null()

image op = Composite((1920, 1080),
                     (0, 0), ImageReference("op_movie"),
                     (0, 0), ImageReference("op_caption"))
