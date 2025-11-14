#!/usr/bin/env python3
"""
SVG Attribute Helper

This script helps add piece attributes to SVG files exported from
Illustrator or other tools that don't preserve custom data attributes.
"""

import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def add_piece_attributes(svg_path: str, output_path: str = None):
    """
    Interactive script to add data-piece-type and data-piece-id attributes
    to shapes in an SVG file.

    Args:
        svg_path: Path to input SVG file
        output_path: Path to output SVG file (defaults to input_annotated.svg)
    """
    if output_path is None:
        svg_file = Path(svg_path)
        output_path = svg_file.parent / f"{svg_file.stem}_annotated{svg_file.suffix}"

    # Parse SVG
    tree = ET.parse(svg_path)
    root = tree.getroot()

    # Find namespace
    if '}' in root.tag:
        namespace = root.tag.split('}')[0] + '}'
    else:
        namespace = ''

    # Find all rect and path elements
    shapes = []
    for elem in root.iter():
        tag = elem.tag.split('}')[-1]
        if tag in ['rect', 'path', 'circle', 'ellipse', 'polygon']:
            shapes.append(elem)

    print(f"Found {len(shapes)} shapes in the SVG file.")
    print("\nFor each shape, enter the piece type (A, B, C, etc.) and piece ID (0, 1, 2, etc.)")
    print("Or press Enter to skip a shape.\n")

    piece_types_count = {}

    for idx, shape in enumerate(shapes):
        tag = shape.tag.split('}')[-1]

        # Show shape info
        print(f"\n--- Shape {idx + 1}/{len(shapes)} ({tag}) ---")

        if tag == 'rect':
            x = shape.get('x', '?')
            y = shape.get('y', '?')
            w = shape.get('width', '?')
            h = shape.get('height', '?')
            print(f"  Position: ({x}, {y})  Size: {w} × {h}")

        shape_id = shape.get('id', 'none')
        print(f"  ID: {shape_id}")

        # Ask for piece type
        piece_type = input("  Piece type (A/B/C/etc. or Enter to skip): ").strip().upper()

        if not piece_type:
            print("  Skipped.")
            continue

        # Auto-increment piece ID for this type
        if piece_type not in piece_types_count:
            piece_types_count[piece_type] = 0

        piece_id = input(f"  Piece ID (default: {piece_types_count[piece_type]}): ").strip()

        if not piece_id:
            piece_id = str(piece_types_count[piece_type])

        # Add attributes
        shape.set('data-piece-type', piece_type)
        shape.set('data-piece-id', piece_id)

        # Update count
        piece_types_count[piece_type] = max(piece_types_count[piece_type], int(piece_id) + 1)

        print(f"  ✓ Added: data-piece-type=\"{piece_type}\" data-piece-id=\"{piece_id}\"")

    # Save annotated SVG
    tree.write(output_path, encoding='utf-8', xml_declaration=True)

    print(f"\n✓ Annotated SVG saved to: {output_path}")
    print(f"\nPiece types found:")
    for ptype, count in sorted(piece_types_count.items()):
        print(f"  Type {ptype}: {count} pieces")


def batch_annotate(svg_path: str, piece_definitions: list):
    """
    Batch annotate shapes based on a list of piece definitions.

    Args:
        svg_path: Path to input SVG file
        piece_definitions: List of (piece_type, piece_id) tuples in order

    Example:
        batch_annotate('design.svg', [
            ('A', 0), ('A', 1), ('A', 2), ('A', 3),
            ('B', 0), ('B', 1)
        ])
    """
    output_path = Path(svg_path).parent / f"{Path(svg_path).stem}_annotated.svg"

    # Parse SVG
    tree = ET.parse(svg_path)
    root = tree.getroot()

    # Find all rect and path elements
    shapes = []
    for elem in root.iter():
        tag = elem.tag.split('}')[-1]
        if tag in ['rect', 'path', 'circle', 'ellipse', 'polygon']:
            shapes.append(elem)

    print(f"Found {len(shapes)} shapes")
    print(f"Annotating with {len(piece_definitions)} piece definitions")

    if len(shapes) != len(piece_definitions):
        print(f"Warning: Number of shapes ({len(shapes)}) doesn't match "
              f"number of definitions ({len(piece_definitions)})")

    # Annotate shapes
    for idx, (shape, (piece_type, piece_id)) in enumerate(zip(shapes, piece_definitions)):
        shape.set('data-piece-type', piece_type)
        shape.set('data-piece-id', str(piece_id))
        print(f"  Shape {idx + 1}: {piece_type}[{piece_id}]")

    # Save
    tree.write(output_path, encoding='utf-8', xml_declaration=True)
    print(f"\n✓ Annotated SVG saved to: {output_path}")


if __name__ == "__main__":
    print("=" * 80)
    print("SVG Attribute Helper for Stained Glass Templates")
    print("=" * 80)

    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python svg_helper.py <svg-file>")
        print("\nExample:")
        print("  python svg_helper.py design.svg")
        print("\nThis will interactively add piece attributes to each shape.")
        sys.exit(1)

    svg_path = sys.argv[1]

    if not Path(svg_path).exists():
        print(f"Error: File not found: {svg_path}")
        sys.exit(1)

    try:
        add_piece_attributes(svg_path)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
