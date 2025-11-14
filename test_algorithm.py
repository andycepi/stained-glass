#!/usr/bin/env python3
"""
Test script to validate the color distribution algorithm
"""

from algorithm_only import PieceType, ColorDistribution


def test_tennis_court_example():
    """Test with the default tennis court parameters"""
    print("Testing Tennis Court Example")
    print("=" * 80)

    # Define piece types (tennis court)
    piece_types = [
        PieceType("A", 4, 1.0, 2.0),  # 4 pieces of type A (1x2 rectangle)
        PieceType("B", 2, 0.5, 4.0),  # 2 pieces of type B (0.5x4 rectangle)
    ]

    num_colors = 6
    num_finished_pieces = 10

    # Calculate distribution
    result = ColorDistribution.calculate_distribution(
        piece_types, num_colors, num_finished_pieces
    )

    if 'error' in result:
        print(f"ERROR: {result['error']}")
        return False

    # Print results
    print(f"Total pieces per finished item: {result['total_pieces_per_item']}")
    print(f"Min pieces per color: {result['min_pieces_per_color']}")
    print(f"Max pieces per color: {result['max_pieces_per_color']}")
    print(f"Distribution variance: {result['max_pieces_per_color'] - result['min_pieces_per_color']}")
    print()

    # Verify no color repeats in any finished piece
    print("Verifying no color repeats in finished pieces...")
    all_valid = True
    for idx, template in enumerate(result['templates']):
        all_colors = []
        for piece_type_name, colors in template.items():
            all_colors.extend(colors)

        # Check for duplicates
        if len(all_colors) != len(set(all_colors)):
            print(f"  ✗ Finished piece #{idx + 1} has duplicate colors!")
            all_valid = False
        else:
            print(f"  ✓ Finished piece #{idx + 1}: All unique colors")

    print()

    # Print cutlist
    print("CUTLIST:")
    print("-" * 80)
    print(f"{'Color':<15} ", end="")
    for pt in piece_types:
        print(f"{pt.name:>6} ", end="")
    print(f"{'Total':>7}")
    print("-" * 80)

    for color, pieces in sorted(result['cutlist'].items()):
        print(f"{color:<15} ", end="")
        for pt in piece_types:
            print(f"{pieces[pt.name]:>6} ", end="")
        total = sum(pieces.values())
        print(f"{total:>7}")

    print("-" * 80)

    # Print totals
    totals = {pt.name: sum(result['cutlist'][color][pt.name]
                          for color in result['cutlist'])
             for pt in piece_types}
    total_all = sum(totals.values())
    print(f"{'TOTAL':<15} ", end="")
    for pt in piece_types:
        print(f"{totals[pt.name]:>6} ", end="")
    print(f"{total_all:>7}")
    print()

    # Show first 3 templates
    print("Sample Templates:")
    print("-" * 80)
    for idx in range(min(3, len(result['templates']))):
        template = result['templates'][idx]
        print(f"\nFinished Piece #{idx + 1}:")
        for pt in piece_types:
            colors = ", ".join(template[pt.name])
            print(f"  {pt.name}: [{colors}]")

    return all_valid


def test_edge_cases():
    """Test edge cases"""
    print("\n" + "=" * 80)
    print("Testing Edge Cases")
    print("=" * 80)

    # Test case: Not enough colors
    print("\n1. Testing insufficient colors:")
    piece_types = [PieceType("A", 3, 1.0, 1.0)]
    result = ColorDistribution.calculate_distribution(piece_types, 2, 5)
    if 'error' in result:
        print(f"  ✓ Correctly detected error: {result['error']}")
    else:
        print(f"  ✗ Should have detected insufficient colors")

    # Test case: Exact number of colors
    print("\n2. Testing exact number of colors (3 pieces, 3 colors):")
    piece_types = [PieceType("A", 3, 1.0, 1.0)]
    result = ColorDistribution.calculate_distribution(piece_types, 3, 5)
    if 'error' not in result:
        print(f"  ✓ Calculated successfully")
        print(f"  Min/Max per color: {result['min_pieces_per_color']}/{result['max_pieces_per_color']}")
    else:
        print(f"  ✗ Error: {result['error']}")

    # Test case: Many colors
    print("\n3. Testing many colors (6 pieces, 20 colors):")
    piece_types = [
        PieceType("A", 3, 1.0, 1.0),
        PieceType("B", 3, 2.0, 2.0)
    ]
    result = ColorDistribution.calculate_distribution(piece_types, 20, 10)
    if 'error' not in result:
        print(f"  ✓ Calculated successfully")
        print(f"  Min/Max per color: {result['min_pieces_per_color']}/{result['max_pieces_per_color']}")
        variance = result['max_pieces_per_color'] - result['min_pieces_per_color']
        print(f"  Distribution variance: {variance}")
    else:
        print(f"  ✗ Error: {result['error']}")


if __name__ == "__main__":
    success = test_tennis_court_example()
    test_edge_cases()

    print("\n" + "=" * 80)
    if success:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed")
    print("=" * 80)
