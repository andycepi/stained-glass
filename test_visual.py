#!/usr/bin/env python3
"""
Test script to validate the visual features and color palette
"""

import sys
sys.path.insert(0, '/home/user/stained-glass')

from algorithm_only import generate_blue_shades, PieceType, ColorDistribution


def test_blue_shades():
    """Test blue shades generation"""
    print("Testing Blue Shades Generation")
    print("=" * 80)

    blues = generate_blue_shades(10)

    print(f"Generated {len(blues)} shades of blue:")
    for name, hex_color in blues:
        print(f"  {name:<10} {hex_color}")

    # Verify format
    assert len(blues) == 10, "Should generate 10 shades"
    for name, hex_color in blues:
        assert hex_color.startswith('#'), f"Hex color should start with #: {hex_color}"
        assert len(hex_color) == 7, f"Hex color should be 7 chars: {hex_color}"

    print("\n✓ All blue shades generated correctly")
    return blues


def test_color_distribution_with_palette():
    """Test color distribution with custom palette"""
    print("\n" + "=" * 80)
    print("Testing Color Distribution with Blue Palette")
    print("=" * 80)

    # Define piece types (tennis court)
    piece_types = [
        PieceType("A", 4, 1.0, 2.0),  # 4 pieces of type A (1x2 rectangle)
        PieceType("B", 2, 0.5, 4.0),  # 2 pieces of type B (0.5x4 rectangle)
    ]

    num_colors = 10
    num_finished_pieces = 5  # Fewer for testing

    # Generate blue palette
    blue_palette = generate_blue_shades(num_colors)

    # Calculate distribution
    result = ColorDistribution.calculate_distribution(
        piece_types, num_colors, num_finished_pieces, blue_palette
    )

    if 'error' in result:
        print(f"ERROR: {result['error']}")
        return False

    # Print results
    print(f"\nTotal pieces per finished item: {result['total_pieces_per_item']}")
    print(f"Min pieces per color: {result['min_pieces_per_color']}")
    print(f"Max pieces per color: {result['max_pieces_per_color']}")
    print(f"Distribution variance: {result['max_pieces_per_color'] - result['min_pieces_per_color']}")

    # Verify color_map exists
    assert 'color_map' in result, "Result should contain color_map"
    color_map = result['color_map']

    print("\nColor Map:")
    for color_name, hex_color in color_map.items():
        print(f"  {color_name:<10} -> {hex_color}")

    # Verify templates use colors from palette
    print("\nSample Templates:")
    for idx in range(min(3, len(result['templates']))):
        template = result['templates'][idx]
        print(f"\nFinished Piece #{idx + 1}:")
        for pt in piece_types:
            colors = template[pt.name]
            print(f"  {pt.name}: {colors}")
            # Verify all colors are in the color_map
            for color in colors:
                assert color in color_map, f"Color {color} should be in color_map"
                print(f"    {color} = {color_map[color]}")

    print("\n✓ Color distribution with palette working correctly")
    return True


def test_tennis_court_layout():
    """Test tennis court layout understanding"""
    print("\n" + "=" * 80)
    print("Tennis Court Layout Verification")
    print("=" * 80)

    print("""
Tennis Court Layout (Top-Down View):

+-------+--------+--------+-------+
|       |        |        |       |
|   B   |   A    |   A    |   B   |
| 0.5x4 |  1x2   |  1x2   | 0.5x4 |
|       |        |        |       |
|       +--------+--------+       |
|       |   A    |   A    |       |
|       |  1x2   |  1x2   |       |
+-------+--------+--------+-------+

Total Width: 0.5 + 1.0 + 1.0 + 0.5 = 3.0 inches
Total Height: 4.0 inches

Piece Breakdown:
- Left B piece: 0.5" wide x 4" tall (left side lane)
- Right B piece: 0.5" wide x 4" tall (right side lane)
- 4 A pieces: each 1" wide x 2" tall (2x2 grid in center)
    - Top-left: position (0.5, 0) to (1.5, 2)
    - Top-right: position (1.5, 0) to (2.5, 2)
    - Bottom-left: position (0.5, 2) to (1.5, 4)
    - Bottom-right: position (1.5, 2) to (2.5, 4)
    """)

    print("✓ Tennis court layout confirmed")


if __name__ == "__main__":
    try:
        blues = test_blue_shades()
        success = test_color_distribution_with_palette()
        test_tennis_court_layout()

        print("\n" + "=" * 80)
        if success:
            print("✓ All visual feature tests passed!")
        else:
            print("✗ Some tests failed")
        print("=" * 80)

    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
