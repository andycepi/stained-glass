#!/usr/bin/env python3
"""
Test script for SVG template system
"""

import sys
import os
sys.path.insert(0, '/home/user/stained-glass')

from template_parser import load_template
from algorithm_only import PieceType, ColorDistribution, generate_blue_shades


def test_template_loading():
    """Test loading SVG templates"""
    print("Testing Template Loading")
    print("=" * 80)

    templates_dir = '/home/user/stained-glass/templates'

    # Test tennis court template
    print("\n1. Tennis Court Template:")
    tennis_court = load_template(os.path.join(templates_dir, 'tennis_court.svg'))
    print(f"   Dimensions: {tennis_court['width']}\" × {tennis_court['height']}\"")
    print(f"   Piece types: {tennis_court['piece_types']}")
    print(f"   Total pieces: {len(tennis_court['pieces'])}")

    # Test simple grid template
    print("\n2. Simple Grid Template:")
    simple_grid = load_template(os.path.join(templates_dir, 'simple_grid.svg'))
    print(f"   Dimensions: {simple_grid['width']}\" × {simple_grid['height']}\"")
    print(f"   Piece types: {simple_grid['piece_types']}")
    print(f"   Total pieces: {len(simple_grid['pieces'])}")

    print("\n✓ All templates loaded successfully!")
    return True


def test_template_with_algorithm():
    """Test template integration with color distribution algorithm"""
    print("\n" + "=" * 80)
    print("Testing Template Integration with Algorithm")
    print("=" * 80)

    # Load template
    template = load_template('/home/user/stained-glass/templates/simple_grid.svg')

    # Create piece types from template
    piece_types = []
    for piece_type_name, count in sorted(template['piece_types'].items()):
        # For simplicity, use 1x1 dimensions (actual dimensions don't affect color distribution)
        pt = PieceType(piece_type_name, count, 1.0, 1.0)
        piece_types.append(pt)

    print(f"\nPiece types created:")
    for pt in piece_types:
        print(f"  {pt}")

    # Generate blue palette
    num_colors = 10
    blue_palette = generate_blue_shades(num_colors)

    # Calculate distribution
    num_finished = 5
    result = ColorDistribution.calculate_distribution(
        piece_types, num_colors, num_finished, blue_palette
    )

    if 'error' in result:
        print(f"\n✗ Error: {result['error']}")
        return False

    print(f"\nDistribution Results:")
    print(f"  Total pieces per finished item: {result['total_pieces_per_item']}")
    print(f"  Min pieces per color: {result['min_pieces_per_color']}")
    print(f"  Max pieces per color: {result['max_pieces_per_color']}")
    print(f"  Variance: {result['max_pieces_per_color'] - result['min_pieces_per_color']}")

    # Show first template
    print(f"\nSample Template (Piece #1):")
    template_1 = result['templates'][0]
    for piece_type_name in sorted(template_1.keys()):
        colors = template_1[piece_type_name]
        print(f"  {piece_type_name}: {colors}")

    # Verify no color repeats
    all_colors = []
    for colors_list in template_1.values():
        all_colors.extend(colors_list)

    if len(all_colors) == len(set(all_colors)):
        print(f"\n✓ No color repeats in finished piece!")
    else:
        print(f"\n✗ Color repeats detected!")
        return False

    print("\n✓ Template integration test passed!")
    return True


def test_piece_ordering():
    """Test that pieces are ordered correctly"""
    print("\n" + "=" * 80)
    print("Testing Piece Ordering")
    print("=" * 80)

    template = load_template('/home/user/stained-glass/templates/tennis_court.svg')

    print("\nPiece order:")
    for piece in template['pieces']:
        print(f"  {piece.piece_type}[{piece.piece_id}]: "
              f"({piece.x}, {piece.y}) → ({piece.x + piece.width}, {piece.y + piece.height})")

    # Verify pieces are sorted by type and ID
    prev_type = None
    prev_id = -1

    for piece in template['pieces']:
        if piece.piece_type == prev_type:
            if piece.piece_id <= prev_id:
                print(f"\n✗ Pieces not properly ordered!")
                return False
        prev_type = piece.piece_type
        prev_id = piece.piece_id

    print("\n✓ Pieces are properly ordered!")
    return True


if __name__ == "__main__":
    try:
        success = True
        success = test_template_loading() and success
        success = test_template_with_algorithm() and success
        success = test_piece_ordering() and success

        print("\n" + "=" * 80)
        if success:
            print("✓ All template tests passed!")
        else:
            print("✗ Some template tests failed")
        print("=" * 80)

    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
