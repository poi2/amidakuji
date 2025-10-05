#!/usr/bin/env python3
"""
Amidakuji Generator CLI Tool

Generate Amidakuji with specified parameters and output as PDF file.
"""

import argparse
import sys
from pathlib import Path

from amidakuji_generator.core import generate_amidakuji_data, render_to_pdf


def main() -> None:
    """Main function: Parse command line arguments and generate Amidakuji"""
    parser = argparse.ArgumentParser(
        description="Generate Amidakuji and output as PDF"
    )

    parser.add_argument(
        "--lines", "-l",
        type=int,
        required=True,
        help="Number of vertical lines (integer >= 2)"
    )

    parser.add_argument(
        "--min-bars", "--min",
        type=int,
        required=True,
        help="Minimum number of horizontal bars (integer >= 0)"
    )

    parser.add_argument(
        "--max-bars", "--max",
        type=int,
        required=True,
        help="Maximum number of horizontal bars (integer >= 0)"
    )

    parser.add_argument(
        "--output", "-o",
        type=str,
        required=True,
        help="Path to output PDF file"
    )

    args = parser.parse_args()

    try:
        # Create output directory if it doesn't exist
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Generate Amidakuji data
        print(
            f"Generating Amidakuji... (lines: {args.lines}, "
            f"bars: {args.min_bars}-{args.max_bars})"
        )
        amidakuji_data = generate_amidakuji_data(
            vertical_lines=args.lines,
            min_horizontal_bars=args.min_bars,
            max_horizontal_bars=args.max_bars
        )

        # Render to PDF
        print(f"Generating PDF... (output: {args.output})")
        render_to_pdf(amidakuji_data, args.output)

        # Display results
        bars_count = amidakuji_data["horizontal_bars_total"]
        print(
            f"Complete! Saved Amidakuji with {bars_count} "
            f"horizontal bars to {args.output}."
        )

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
