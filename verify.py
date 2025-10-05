#!/usr/bin/env python3
"""
Amidakuji Generator Tool Verification Script
"""

import tempfile
from pathlib import Path

from amidakuji_generator.core import generate_amidakuji_data, render_to_pdf


def test_basic_functionality() -> bool:
    """Test basic functionality"""
    print("=== Amidakuji Generator Tool Verification ===")

    try:
        # 1. Data generation test
        print("1. Amidakuji data generation test...")
        data = generate_amidakuji_data(
            vertical_lines=5,
            min_horizontal_bars=3,
            max_horizontal_bars=10
        )
        print(f"   ✓ Vertical lines: {data['vertical_lines']}")
        print(f"   ✓ Horizontal bars: {data['horizontal_bars_total']}")
        print(f"   ✓ Data structure: {len(data['horizontal_bars'])} horizontal bars")

        # 2. PDF generation test
        print("\n2. PDF generation test...")
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            output_path = tmp.name

        render_to_pdf(data, output_path)

        if Path(output_path).exists():
            size = Path(output_path).stat().st_size
            print(f"   ✓ PDF file generation successful: {size} bytes")
            Path(output_path).unlink()  # Delete temporary file
        else:
            print("   ✗ PDF file generation failed")
            return False

        # 3. Error handling test
        print("\n3. Error handling test...")
        try:
            generate_amidakuji_data(1, 0, 5)  # Invalid number of vertical lines
            print("   ✗ Error handling failed")
            return False
        except ValueError:
            print("   ✓ Proper detection of invalid input")

        print("\n=== All tests successful! ===")
        return True

    except Exception as e:
        print(f"\n✗ Error occurred: {e}")
        return False


if __name__ == "__main__":
    success = test_basic_functionality()
    exit(0 if success else 1)
