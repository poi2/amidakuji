#!/usr/bin/env python3
"""
あみだくじ生成CLIツール

指定されたパラメータであみだくじを生成し、PDFファイルとして出力します。
"""

import argparse
import sys
from pathlib import Path

from amidakuji_generator.core import generate_amidakuji_data, render_to_pdf


def main() -> None:
    """メイン関数：コマンドライン引数を解析してあみだくじを生成"""
    parser = argparse.ArgumentParser(
        description="あみだくじを生成してPDFとして出力します"
    )

    parser.add_argument(
        "--lines", "-l",
        type=int,
        required=True,
        help="縦棒の本数（2以上の整数）"
    )

    parser.add_argument(
        "--min-bars", "--min",
        type=int,
        required=True,
        help="横棒の最小本数（0以上の整数）"
    )

    parser.add_argument(
        "--max-bars", "--max",
        type=int,
        required=True,
        help="横棒の最大本数（0以上の整数）"
    )

    parser.add_argument(
        "--output", "-o",
        type=str,
        required=True,
        help="出力するPDFファイルのパス"
    )

    args = parser.parse_args()

    try:
        # 出力ディレクトリが存在しない場合は作成
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # あみだくじデータを生成
        print(f"あみだくじを生成中... (縦棒: {args.lines}, 横棒: {args.min_bars}-{args.max_bars})")
        amidakuji_data = generate_amidakuji_data(
            vertical_lines=args.lines,
            min_horizontal_bars=args.min_bars,
            max_horizontal_bars=args.max_bars
        )

        # PDFにレンダリング
        print(f"PDFを生成中... (出力先: {args.output})")
        render_to_pdf(amidakuji_data, args.output)

        # 結果を表示
        bars_count = amidakuji_data["horizontal_bars_total"]
        print(f"完了！{bars_count}本の横棒を持つあみだくじを {args.output} に保存しました。")

    except ValueError as e:
        print(f"エラー: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()