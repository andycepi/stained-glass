#!/usr/bin/env python3
"""
Stained Glass Color Distribution Algorithm (without GUI dependencies)
"""

from typing import List, Dict


class PieceType:
    """Represents a type of glass piece"""
    def __init__(self, name: str, count: int, width: float, height: float):
        self.name = name
        self.count = count
        self.width = width
        self.height = height

    def __repr__(self):
        return f"{self.name}: {self.count} pieces ({self.width}x{self.height})"


class ColorDistribution:
    """Calculates optimal color distribution for glass pieces"""

    @staticmethod
    def calculate_distribution(piece_types: List[PieceType], num_colors: int,
                              num_finished_pieces: int) -> Dict:
        """
        Calculate color distribution ensuring no color repeats in a finished piece.
        Returns distribution plan and templates for each finished piece.
        """
        # Calculate total pieces per finished item
        total_pieces_per_item = sum(pt.count for pt in piece_types)

        # Check if distribution is possible
        if num_colors < total_pieces_per_item:
            return {
                'error': f"Need at least {total_pieces_per_item} colors to avoid "
                        f"repeating colors in a finished piece. You have {num_colors} colors."
            }

        # Calculate total pieces needed
        total_pieces_needed = {pt.name: pt.count * num_finished_pieces
                              for pt in piece_types}

        # Distribute colors across piece types
        # Strategy: Rotate colors through pieces to ensure even distribution
        color_names = [f"Color {i+1}" for i in range(num_colors)]

        # Create templates for each finished piece
        templates = []
        piece_type_dict = {pt.name: pt for pt in piece_types}

        for piece_idx in range(num_finished_pieces):
            template = {}
            color_offset = piece_idx * total_pieces_per_item
            piece_position = 0

            for pt in piece_types:
                template[pt.name] = []
                for i in range(pt.count):
                    color_idx = (color_offset + piece_position) % num_colors
                    template[pt.name].append(color_names[color_idx])
                    piece_position += 1

            templates.append(template)

        # Calculate cutlist (total pieces needed per color)
        cutlist = {color: {pt.name: 0 for pt in piece_types}
                  for color in color_names}

        for template in templates:
            for piece_type_name, colors in template.items():
                for color in colors:
                    cutlist[color][piece_type_name] += 1

        # Calculate statistics
        min_pieces = min(sum(pieces.values()) for pieces in cutlist.values())
        max_pieces = max(sum(pieces.values()) for pieces in cutlist.values())

        return {
            'templates': templates,
            'cutlist': cutlist,
            'total_pieces_per_item': total_pieces_per_item,
            'min_pieces_per_color': min_pieces,
            'max_pieces_per_color': max_pieces,
            'piece_types': piece_type_dict
        }
