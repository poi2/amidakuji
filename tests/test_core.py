"""
amidakuji_generator.core モジュールのテスト
"""

import tempfile
from pathlib import Path

import pytest

from amidakuji_generator.core import generate_amidakuji_data, render_to_pdf


class TestGenerateAmidakujiData:
    """generate_amidakuji_data 関数のテストクラス"""

    def test_basic_generation(self) -> None:
        """基本的なあみだくじ生成のテスト"""
        result = generate_amidakuji_data(
            vertical_lines=5,
            min_horizontal_bars=3,
            max_horizontal_bars=10
        )

        # 期待されるキーが存在することを確認
        assert "vertical_lines" in result
        assert "horizontal_bars_total" in result
        assert "horizontal_bars" in result

        # 値の範囲チェック
        assert result["vertical_lines"] == 5
        assert 3 <= result["horizontal_bars_total"] <= 10
        assert len(result["horizontal_bars"]) == result["horizontal_bars_total"]

    def test_horizontal_bars_structure(self) -> None:
        """横棒データ構造のテスト"""
        result = generate_amidakuji_data(
            vertical_lines=4,
            min_horizontal_bars=2,
            max_horizontal_bars=5
        )

        # 各横棒が正しい構造を持つことを確認
        for bar in result["horizontal_bars"]:
            assert "y_level" in bar
            assert "left_line_index" in bar
            assert isinstance(bar["y_level"], int)
            assert isinstance(bar["left_line_index"], int)
            assert 0 <= bar["left_line_index"] < result["vertical_lines"] - 1

    def test_invalid_vertical_lines(self) -> None:
        """無効な縦棒数に対するエラーテスト"""
        with pytest.raises(ValueError, match="縦棒の本数は2以上である必要があります"):
            generate_amidakuji_data(
                vertical_lines=1,
                min_horizontal_bars=0,
                max_horizontal_bars=5
            )

    def test_invalid_horizontal_bars_range(self) -> None:
        """無効な横棒数範囲に対するエラーテスト"""
        with pytest.raises(ValueError, match="最小本数は最大本数以下である必要があります"):
            generate_amidakuji_data(
                vertical_lines=5,
                min_horizontal_bars=10,
                max_horizontal_bars=5
            )

    def test_negative_horizontal_bars(self) -> None:
        """負の横棒数に対するエラーテスト"""
        with pytest.raises(ValueError, match="横棒の最小本数は0以上である必要があります"):
            generate_amidakuji_data(
                vertical_lines=5,
                min_horizontal_bars=-1,
                max_horizontal_bars=5
            )

    def test_zero_horizontal_bars(self) -> None:
        """横棒数が0の場合のテスト"""
        result = generate_amidakuji_data(
            vertical_lines=3,
            min_horizontal_bars=0,
            max_horizontal_bars=0
        )

        assert result["vertical_lines"] == 3
        assert result["horizontal_bars_total"] == 0
        assert len(result["horizontal_bars"]) == 0


class TestRenderToPdf:
    """render_to_pdf 関数のテストクラス"""

    def test_pdf_generation(self) -> None:
        """PDFファイル生成のテスト"""
        # テスト用のあみだくじデータを生成
        amidakuji_data = generate_amidakuji_data(
            vertical_lines=4,
            min_horizontal_bars=2,
            max_horizontal_bars=5
        )

        # 一時ファイルを使用してPDF生成をテスト
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_file:
            output_path = tmp_file.name

        try:
            # PDF生成（例外が発生しないことを確認）
            render_to_pdf(amidakuji_data, output_path)

            # ファイルが作成されたことを確認
            assert Path(output_path).exists()
            assert Path(output_path).stat().st_size > 0

        finally:
            # テスト後にファイルを削除
            Path(output_path).unlink(missing_ok=True)

    def test_output_directory_creation(self) -> None:
        """出力ディレクトリが存在しない場合のテスト"""
        amidakuji_data = generate_amidakuji_data(
            vertical_lines=3,
            min_horizontal_bars=1,
            max_horizontal_bars=3
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "subdir" / "test.pdf"

            # PDF生成（例外が発生しないことを確認）
            render_to_pdf(amidakuji_data, str(output_path))

            # ファイルが作成されたことを確認
            assert output_path.exists()
            assert output_path.stat().st_size > 0