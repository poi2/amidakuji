"""
Tests for amidakuji_generator.core module
"""

import tempfile
from pathlib import Path

import pytest

from amidakuji_generator.core import generate_amidakuji_data, render_to_pdf


class TestGenerateAmidakujiData:
    """Test class for generate_amidakuji_data function"""

    def test_basic_generation(self) -> None:
        """Test basic Amidakuji generation"""
        result = generate_amidakuji_data(
            vertical_lines=5, min_horizontal_bars=3, max_horizontal_bars=10
        )

        # Verify that expected keys exist
        assert "vertical_lines" in result
        assert "horizontal_bars_total" in result
        assert "horizontal_bars" in result

        # Check value ranges
        assert result["vertical_lines"] == 5
        assert 3 <= result["horizontal_bars_total"] <= 10
        assert len(result["horizontal_bars"]) == result["horizontal_bars_total"]

    def test_horizontal_bars_structure(self) -> None:
        """Test horizontal bars data structure"""
        result = generate_amidakuji_data(
            vertical_lines=4, min_horizontal_bars=2, max_horizontal_bars=5
        )

        # Verify that each horizontal bar has correct structure
        for bar in result["horizontal_bars"]:
            assert "y_level" in bar
            assert "left_line_index" in bar
            assert isinstance(bar["y_level"], int)
            assert isinstance(bar["left_line_index"], int)
            assert 0 <= bar["left_line_index"] < result["vertical_lines"] - 1

    def test_invalid_vertical_lines(self) -> None:
        """Test error handling for invalid number of vertical lines"""
        with pytest.raises(
            ValueError, match="Number of vertical lines must be 2 or greater"
        ):
            generate_amidakuji_data(
                vertical_lines=1, min_horizontal_bars=0, max_horizontal_bars=5
            )

    def test_invalid_horizontal_bars_range(self) -> None:
        """Test error handling for invalid horizontal bars range"""
        with pytest.raises(
            ValueError, match="Minimum must be less than or equal to maximum"
        ):
            generate_amidakuji_data(
                vertical_lines=5, min_horizontal_bars=10, max_horizontal_bars=5
            )

    def test_negative_horizontal_bars(self) -> None:
        """Test error handling for negative horizontal bars"""
        with pytest.raises(
            ValueError,
            match="Minimum number of horizontal bars must be 0 or greater",
        ):
            generate_amidakuji_data(
                vertical_lines=5, min_horizontal_bars=-1, max_horizontal_bars=5
            )

    def test_zero_horizontal_bars(self) -> None:
        """Test case when number of horizontal bars is 0"""
        result = generate_amidakuji_data(
            vertical_lines=3, min_horizontal_bars=0, max_horizontal_bars=0
        )

        assert result["vertical_lines"] == 3
        assert result["horizontal_bars_total"] == 0
        assert len(result["horizontal_bars"]) == 0


class TestRenderToPdf:
    """Test class for render_to_pdf function"""

    def test_pdf_generation(self) -> None:
        """Test PDF file generation"""
        # Generate test Amidakuji data
        amidakuji_data = generate_amidakuji_data(
            vertical_lines=4, min_horizontal_bars=2, max_horizontal_bars=5
        )

        # Use temporary file to test PDF generation
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_file:
            output_path = tmp_file.name

        try:
            # Generate PDF (verify no exceptions occur)
            render_to_pdf(amidakuji_data, output_path)

            # Verify that file was created
            assert Path(output_path).exists()
            assert Path(output_path).stat().st_size > 0

        finally:
            # Delete file after test
            Path(output_path).unlink(missing_ok=True)

    def test_output_directory_creation(self) -> None:
        """Test case when output directory doesn't exist"""
        amidakuji_data = generate_amidakuji_data(
            vertical_lines=3, min_horizontal_bars=1, max_horizontal_bars=3
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "subdir" / "test.pdf"

            # Generate PDF (verify no exceptions occur)
            render_to_pdf(amidakuji_data, str(output_path))

            # Verify that file was created
            assert output_path.exists()
            assert output_path.stat().st_size > 0
