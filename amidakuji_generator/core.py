import random
from typing import Any, Dict, List

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


def generate_amidakuji_data(
    vertical_lines: int,
    min_horizontal_bars: int,
    max_horizontal_bars: int,
    margin_ratio: float = 0.1,
) -> Dict[str, Any]:
    """
    Generate abstract data structure for Amidakuji.

    Args:
        vertical_lines (int): Number of vertical lines (n). Must be 2 or greater.
        min_horizontal_bars (int): Minimum number of horizontal bars (b_min).
        max_horizontal_bars (int): Maximum number of horizontal bars (b_max).
        margin_ratio (float): Ratio of margin from top/bottom (default: 0.1 = 10%).

    Returns:
        Dict[str, Any]: Dictionary representing Amidakuji structure.
        Example:
        {
            "vertical_lines": 5,
            "horizontal_bars_total": 10,
            "horizontal_bars": [
                {"y_level": 2, "left_line_index": 0},...
            ]
        }

    Raises:
        ValueError: When input parameters are invalid
    """
    # Input parameter validation
    if vertical_lines < 2:
        raise ValueError("Number of vertical lines must be 2 or greater")
    if min_horizontal_bars < 0:
        raise ValueError("Minimum number of horizontal bars must be 0 or greater")
    if max_horizontal_bars < 0:
        raise ValueError("Maximum number of horizontal bars must be 0 or greater")
    if min_horizontal_bars > max_horizontal_bars:
        raise ValueError("Minimum must be less than or equal to maximum")
    if margin_ratio < 0 or margin_ratio >= 0.5:
        raise ValueError("Margin ratio must be between 0 and 0.5")

    # Randomly determine total number of horizontal bars
    total_bars = random.randint(min_horizontal_bars, max_horizontal_bars)

    # Define placement grid with margin considerations
    height = total_bars * 2 if total_bars > 0 else 6
    num_columns = vertical_lines - 1
    
    # Calculate margin levels (top and bottom exclusion zones)
    margin_levels = max(1, int(height * margin_ratio))
    
    # Manage selected positions and horizontal bars
    selected_positions = set()
    horizontal_bars = []

    # First, ensure each vertical line has at least one horizontal bar
    # Strategy: place one bar for each vertical line if total_bars >= num_columns
    if total_bars >= num_columns:
        # Generate candidate positions for ensuring coverage
        coverage_positions = []
        for y in range(margin_levels, height - margin_levels):
            for col in range(num_columns):
                coverage_positions.append((y, col))
        
        random.shuffle(coverage_positions)
        
        # Track which lines are covered
        line_covered = [False] * vertical_lines
        
        # Place bars to ensure all lines are covered
        for y, col in coverage_positions:
            if len(horizontal_bars) >= total_bars:
                break
                
            # Check if this bar would cover uncovered lines
            left_covered = line_covered[col]
            right_covered = line_covered[col + 1] if col + 1 < vertical_lines else True
            
            # If this bar covers at least one uncovered line and no conflicts
            if (not left_covered or not right_covered) and (
                (y, col) not in selected_positions
                and (y, col - 1) not in selected_positions
                and (y, col + 1) not in selected_positions
            ):
                horizontal_bars.append({"y_level": y, "left_line_index": col})
                selected_positions.add((y, col))
                line_covered[col] = True
                line_covered[col + 1] = True
                
                # Break if all lines are covered
                if all(line_covered):
                    break
    
    # Fill remaining bars randomly if we haven't reached total_bars
    if len(horizontal_bars) < total_bars:
        remaining_positions = []
        for y in range(margin_levels, height - margin_levels):
            for col in range(num_columns):
                if (y, col) not in selected_positions:
                    remaining_positions.append((y, col))
        
        random.shuffle(remaining_positions)
        
        for y, col in remaining_positions:
            if len(horizontal_bars) >= total_bars:
                break
                
            # Check if adjacent positions are not already selected
            if (
                (y, col) not in selected_positions
                and (y, col - 1) not in selected_positions
                and (y, col + 1) not in selected_positions
            ):
                horizontal_bars.append({"y_level": y, "left_line_index": col})
                selected_positions.add((y, col))

    # Final validation that each vertical line has at least one horizontal bar
    line_has_bar = [False] * vertical_lines
    for bar in horizontal_bars:
        left_index = bar["left_line_index"]
        line_has_bar[left_index] = True
        if left_index + 1 < vertical_lines:
            line_has_bar[left_index + 1] = True
    
    # If validation fails, retry with more bars or different strategy
    if not all(line_has_bar):
        missing_lines = [i + 1 for i, has_bar in enumerate(line_has_bar) if not has_bar]
        raise ValueError(f"Cannot generate valid amidakuji: not enough bars to connect all vertical lines. Missing lines: {missing_lines}. Try increasing the number of horizontal bars.")

    return {
        "vertical_lines": vertical_lines,
        "horizontal_bars_total": len(horizontal_bars),
        "horizontal_bars": horizontal_bars,
    }


def render_to_pdf(amidakuji_data: Dict[str, Any], output_path: str) -> None:
    """
    Render Amidakuji data structure to PDF file using ReportLab.

    Args:
        amidakuji_data (Dict[str, Any]): Data structure obtained from
            generate_amidakuji_data.
        output_path (str): File path to save the generated PDF.
    """
    # Create output directory if it doesn't exist
    from pathlib import Path

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    # Initialize PDF document
    c = canvas.Canvas(output_path, pagesize=A4)
    page_width, page_height = A4

    # Set margins (1 inch = 72 points)
    margin = inch
    draw_width = page_width - 2 * margin
    draw_height = page_height - 2 * margin

    # Get data
    n = amidakuji_data["vertical_lines"]
    horizontal_bars = amidakuji_data["horizontal_bars"]

    # Get maximum y_level to calculate layout
    max_y_level = max([bar["y_level"] for bar in horizontal_bars], default=0)
    levels = max_y_level + 1

    # Calculate vertical line spacing
    if n > 1:
        line_spacing = draw_width / (n - 1)
    else:
        line_spacing = 0

    # Calculate level spacing
    if levels > 1:
        # Reserve space for labels at top and bottom
        level_spacing = draw_height / (levels + 2)
    else:
        level_spacing = draw_height / 4

    # Draw vertical lines
    for i in range(n):
        x = margin + i * line_spacing
        y_top = page_height - margin - level_spacing
        y_bottom = margin + level_spacing
        c.line(x, y_top, x, y_bottom)

    # Draw start labels (top)
    for i in range(n):
        x = margin + i * line_spacing
        y = page_height - margin - level_spacing / 2
        text = str(i + 1)
        text_width = c.stringWidth(text)
        c.drawString(x - text_width / 2, y, text)

    # Simulate Amidakuji path to calculate results
    result_mapping = _simulate_amidakuji(amidakuji_data)

    # Draw end labels (bottom)
    for i in range(n):
        x = margin + i * line_spacing
        y = margin + level_spacing / 2
        result_char = chr(ord("A") + result_mapping[i])
        text_width = c.stringWidth(result_char)
        c.drawString(x - text_width / 2, y, result_char)

    # Draw horizontal bars
    for bar in horizontal_bars:
        y_level = bar["y_level"]
        left_index = bar["left_line_index"]

        x1 = margin + left_index * line_spacing
        x2 = margin + (left_index + 1) * line_spacing
        y = page_height - margin - level_spacing - (y_level * level_spacing)

        c.line(x1, y, x2, y)

    # Display generation parameters in footer
    footer_text = f"Generated with n={n}, bars={len(horizontal_bars)}"
    c.drawString(margin, margin / 2, footer_text)

    # Save PDF
    c.save()


def _simulate_amidakuji(amidakuji_data: Dict[str, Any]) -> List[int]:
    """
    Simulate Amidakuji path to calculate the destination of each starting point.

    Args:
        amidakuji_data: Amidakuji data structure

    Returns:
        List[int]: Index of destination point corresponding to each starting point
    """
    n = amidakuji_data["vertical_lines"]
    horizontal_bars = amidakuji_data["horizontal_bars"]

    # Sort by y_level and process from top to bottom
    sorted_bars = sorted(horizontal_bars, key=lambda x: x["y_level"])

    # Track current position of each line
    positions = list(range(n))

    # Execute swaps by horizontal bars at each level
    for bar in sorted_bars:
        left_index = bar["left_line_index"]
        # Swap positions at left_index and left_index+1
        if left_index < len(positions) - 1:
            positions[left_index], positions[left_index + 1] = (
                positions[left_index + 1],
                positions[left_index],
            )

    return positions
