import random
from typing import Any, Dict, List

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


def generate_amidakuji_data(
    vertical_lines: int,
    min_horizontal_bars: int,
    max_horizontal_bars: int,
) -> Dict[str, Any]:
    """
    あみだくじの抽象データ構造を生成する。

    Args:
        vertical_lines (int): 縦棒の本数 (n)。2以上である必要がある。
        min_horizontal_bars (int): 横棒の最小本数 (b_min)。
        max_horizontal_bars (int): 横棒の最大本数 (b_max)。

    Returns:
        Dict[str, Any]: あみだくじの構造を表す辞書。
        例:
        {
            "vertical_lines": 5,
            "horizontal_bars_total": 10,
            "horizontal_bars": [
                {"y_level": 2, "left_line_index": 0},...
            ]
        }

    Raises:
        ValueError: 入力パラメータが無効な場合
    """
    # 入力パラメータの検証
    if vertical_lines < 2:
        raise ValueError("縦棒の本数は2以上である必要があります")
    if min_horizontal_bars < 0:
        raise ValueError("横棒の最小本数は0以上である必要があります")
    if max_horizontal_bars < 0:
        raise ValueError("横棒の最大本数は0以上である必要があります")
    if min_horizontal_bars > max_horizontal_bars:
        raise ValueError("最小本数は最大本数以下である必要があります")

    # 横棒の総数をランダムに決定
    total_bars = random.randint(min_horizontal_bars, max_horizontal_bars)

    # 配置グリッドの定義
    height = total_bars * 2 if total_bars > 0 else 2
    num_columns = vertical_lines - 1

    # 配置候補の生成
    positions = []
    for y in range(height):
        for col in range(num_columns):
            positions.append((y, col))

    # ランダムにシャッフル
    random.shuffle(positions)

    # 選択済み位置を管理
    selected_positions = set()
    horizontal_bars = []

    # 横棒を配置
    for y, col in positions:
        if len(horizontal_bars) >= total_bars:
            break

        # 隣接する位置が既に選択されていないかチェック
        if (y, col) not in selected_positions and \
           (y, col - 1) not in selected_positions and \
           (y, col + 1) not in selected_positions:
            # 競合しない場合、横棒を追加
            horizontal_bars.append({
                "y_level": y,
                "left_line_index": col
            })
            selected_positions.add((y, col))

    return {
        "vertical_lines": vertical_lines,
        "horizontal_bars_total": len(horizontal_bars),
        "horizontal_bars": horizontal_bars
    }


def render_to_pdf(
    amidakuji_data: Dict[str, Any],
    output_path: str
) -> None:
    """
    あみだくじのデータ構造をReportLabを使用してPDFファイルにレンダリングする。

    Args:
        amidakuji_data (Dict[str, Any]): generate_amidakuji_dataから得られるデータ構造。
        output_path (str): 生成されたPDFを保存するファイルパス。
    """
    # 出力ディレクトリが存在しない場合は作成
    from pathlib import Path
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    # PDFドキュメントの初期化
    c = canvas.Canvas(output_path, pagesize=A4)
    page_width, page_height = A4

    # マージンの設定（1インチ = 72ポイント）
    margin = inch
    draw_width = page_width - 2 * margin
    draw_height = page_height - 2 * margin

    # データの取得
    n = amidakuji_data["vertical_lines"]
    horizontal_bars = amidakuji_data["horizontal_bars"]

    # 最大のy_levelを取得してレイアウトを計算
    max_y_level = max([bar["y_level"] for bar in horizontal_bars], default=0)
    levels = max_y_level + 1

    # 縦棒の間隔を計算
    if n > 1:
        line_spacing = draw_width / (n - 1)
    else:
        line_spacing = 0

    # レベル間の間隔を計算
    if levels > 1:
        level_spacing = draw_height / (levels + 2)  # 上下にラベル用のスペースを確保
    else:
        level_spacing = draw_height / 4

    # 縦棒を描画
    for i in range(n):
        x = margin + i * line_spacing
        y_top = page_height - margin - level_spacing
        y_bottom = margin + level_spacing
        c.line(x, y_top, x, y_bottom)

    # 開始ラベル（上部）を描画
    for i in range(n):
        x = margin + i * line_spacing
        y = page_height - margin - level_spacing / 2
        text = str(i + 1)
        text_width = c.stringWidth(text)
        c.drawString(x - text_width / 2, y, text)

    # あみだくじの経路をシミュレーションして結果を計算
    result_mapping = _simulate_amidakuji(amidakuji_data)

    # 終了ラベル（下部）を描画
    for i in range(n):
        x = margin + i * line_spacing
        y = margin + level_spacing / 2
        result_char = chr(ord('A') + result_mapping[i])
        text_width = c.stringWidth(result_char)
        c.drawString(x - text_width / 2, y, result_char)

    # 横棒を描画
    for bar in horizontal_bars:
        y_level = bar["y_level"]
        left_index = bar["left_line_index"]

        x1 = margin + left_index * line_spacing
        x2 = margin + (left_index + 1) * line_spacing
        y = page_height - margin - level_spacing - (y_level * level_spacing)

        c.line(x1, y, x2, y)

    # フッターに生成パラメータを表示
    footer_text = f"Generated with n={n}, bars={len(horizontal_bars)}"
    c.drawString(margin, margin / 2, footer_text)

    # PDFを保存
    c.save()


def _simulate_amidakuji(amidakuji_data: Dict[str, Any]) -> List[int]:
    """
    あみだくじの経路をシミュレーションして、各開始点の終着点を計算する。

    Args:
        amidakuji_data: あみだくじのデータ構造

    Returns:
        List[int]: 各開始点に対応する終着点のインデックス
    """
    n = amidakuji_data["vertical_lines"]
    horizontal_bars = amidakuji_data["horizontal_bars"]

    # y_levelでソートして上から順に処理
    sorted_bars = sorted(horizontal_bars, key=lambda x: x["y_level"])

    # 各線の現在位置を追跡
    positions = list(range(n))

    # 各レベルで横棒による交換を実行
    for bar in sorted_bars:
        left_index = bar["left_line_index"]
        # left_indexとleft_index+1の位置を交換
        if left_index < len(positions) - 1:
            positions[left_index], positions[left_index + 1] = \
                positions[left_index + 1], positions[left_index]

    return positions