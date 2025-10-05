#!/usr/bin/env python3
"""
あみだくじ生成ツールの動作確認スクリプト
"""

import tempfile
from pathlib import Path

from amidakuji_generator.core import generate_amidakuji_data, render_to_pdf


def test_basic_functionality():
    """基本機能のテスト"""
    print("=== あみだくじ生成ツール 動作確認 ===")
    
    try:
        # 1. データ生成テスト
        print("1. あみだくじデータ生成テスト...")
        data = generate_amidakuji_data(
            vertical_lines=5,
            min_horizontal_bars=3,
            max_horizontal_bars=10
        )
        print(f"   ✓ 縦棒: {data['vertical_lines']}")
        print(f"   ✓ 横棒: {data['horizontal_bars_total']}")
        print(f"   ✓ データ構造: {len(data['horizontal_bars'])}個の横棒")
        
        # 2. PDF生成テスト
        print("\n2. PDF生成テスト...")
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            output_path = tmp.name
        
        render_to_pdf(data, output_path)
        
        if Path(output_path).exists():
            size = Path(output_path).stat().st_size
            print(f"   ✓ PDFファイル生成成功: {size} bytes")
            Path(output_path).unlink()  # 一時ファイルを削除
        else:
            print("   ✗ PDFファイル生成失敗")
            return False
        
        # 3. エラーハンドリングテスト
        print("\n3. エラーハンドリングテスト...")
        try:
            generate_amidakuji_data(1, 0, 5)  # 無効な縦棒数
            print("   ✗ エラーハンドリング失敗")
            return False
        except ValueError:
            print("   ✓ 無効入力の適切な検出")
        
        print("\n=== 全テスト成功！ ===")
        return True
        
    except Exception as e:
        print(f"\n✗ エラー発生: {e}")
        return False


if __name__ == "__main__":
    success = test_basic_functionality()
    exit(0 if success else 1)