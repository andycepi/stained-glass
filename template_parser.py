#!/usr/bin/env python3
"""
SVG Template Parser for Stained Glass Designs

Parses SVG templates to extract piece definitions for rendering.
"""

import xml.etree.ElementTree as ET
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class TemplatePiece:
    """Represents a single piece in the template"""
    piece_type: str  # A, B, C, etc.
    piece_id: int  # Index within that type
    shape: str  # 'rect' or 'path'
    x: float
    y: float
    width: float
    height: float
    path_data: Optional[str] = None  # For path elements


class TemplateParser:
    """Parses SVG templates to extract piece definitions"""

    def __init__(self, svg_path: str):
        """
        Initialize parser with SVG file path.

        Args:
            svg_path: Path to the SVG template file
        """
        self.svg_path = svg_path
        self.tree = None
        self.root = None
        self.viewbox_width = 0
        self.viewbox_height = 0
        self.pieces: List[TemplatePiece] = []

    def parse(self) -> Dict:
        """
        Parse the SVG template.

        Returns:
            Dictionary containing:
                - width: Template width
                - height: Template height
                - pieces: List of TemplatePiece objects
                - piece_types: Dictionary of piece type -> count
        """
        try:
            # Parse SVG
            self.tree = ET.parse(self.svg_path)
            self.root = self.tree.getroot()

            # Remove namespace if present
            if '}' in self.root.tag:
                namespace = self.root.tag.split('}')[0] + '}'
            else:
                namespace = ''

            # Get viewBox dimensions
            viewbox = self.root.get('viewBox', '0 0 3 4')
            parts = viewbox.split()
            self.viewbox_width = float(parts[2])
            self.viewbox_height = float(parts[3])

            # Parse pieces
            self.pieces = []
            piece_counts = {}

            # Find all elements with data-piece-type
            for elem in self.root.iter():
                # Get piece type from data-piece-type attribute
                piece_type = elem.get('data-piece-type')
                if not piece_type:
                    continue

                # Get piece ID
                piece_id_str = elem.get('data-piece-id', '0')
                piece_id = int(piece_id_str)

                # Track counts
                if piece_type not in piece_counts:
                    piece_counts[piece_type] = 0
                piece_counts[piece_type] = max(piece_counts[piece_type], piece_id + 1)

                # Parse shape
                tag = elem.tag.split('}')[-1]  # Remove namespace if present

                if tag == 'rect':
                    piece = TemplatePiece(
                        piece_type=piece_type,
                        piece_id=piece_id,
                        shape='rect',
                        x=float(elem.get('x', 0)),
                        y=float(elem.get('y', 0)),
                        width=float(elem.get('width', 1)),
                        height=float(elem.get('height', 1))
                    )
                    self.pieces.append(piece)

                elif tag == 'path':
                    # For paths, calculate bounding box from path data
                    path_data = elem.get('d', '')
                    # Simplified: would need full path parsing for accurate bounds
                    # For now, use transform or estimates
                    piece = TemplatePiece(
                        piece_type=piece_type,
                        piece_id=piece_id,
                        shape='path',
                        x=0,
                        y=0,
                        width=1,
                        height=1,
                        path_data=path_data
                    )
                    self.pieces.append(piece)

            # Sort pieces by type and ID for consistent ordering
            self.pieces.sort(key=lambda p: (p.piece_type, p.piece_id))

            return {
                'width': self.viewbox_width,
                'height': self.viewbox_height,
                'pieces': self.pieces,
                'piece_types': piece_counts
            }

        except Exception as e:
            raise ValueError(f"Error parsing SVG template: {e}")

    def get_piece_order(self) -> Dict[str, List[int]]:
        """
        Get the ordered list of piece IDs for each type.

        Returns:
            Dictionary mapping piece type to ordered list of piece IDs
        """
        order = {}
        for piece in self.pieces:
            if piece.piece_type not in order:
                order[piece.piece_type] = []
            order[piece.piece_type].append(piece.piece_id)
        return order


def load_template(template_path: str) -> Dict:
    """
    Load and parse an SVG template.

    Args:
        template_path: Path to SVG template file

    Returns:
        Parsed template dictionary
    """
    parser = TemplateParser(template_path)
    return parser.parse()


if __name__ == "__main__":
    # Test the parser
    import sys
    import os

    template_file = "/home/user/stained-glass/templates/tennis_court.svg"

    if os.path.exists(template_file):
        print(f"Parsing template: {template_file}")
        print("=" * 80)

        template = load_template(template_file)

        print(f"Template dimensions: {template['width']}\" × {template['height']}\"")
        print(f"\nPiece types found: {template['piece_types']}")

        print(f"\nPieces ({len(template['pieces'])} total):")
        for piece in template['pieces']:
            print(f"  {piece.piece_type}[{piece.piece_id}]: "
                  f"{piece.shape} at ({piece.x}, {piece.y}) "
                  f"size {piece.width} × {piece.height}")

        print("\n✓ Template parsed successfully!")
    else:
        print(f"Template file not found: {template_file}")
