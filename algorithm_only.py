#!/usr/bin/env python3
"""
Stained Glass Color Distribution Algorithm (without GUI dependencies)
"""

from typing import List, Dict
import random


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
        # Strategy: Generate random unique color arrangements for each finished piece
        color_names = [f"Color {i+1}" for i in range(num_colors)]

        # Create templates for each finished piece
        templates = []
        piece_type_dict = {pt.name: pt for pt in piece_types}
        used_arrangements = set()

        # Maximum attempts to prevent infinite loops
        max_attempts = num_finished_pieces * 1000
        attempts = 0

        while len(templates) < num_finished_pieces:
            if attempts >= max_attempts:
                return {
                    'error': f"Could not generate {num_finished_pieces} unique arrangements. "
                            f"Try using more colors or fewer finished pieces."
                }
            attempts += 1

            # Randomly select colors for this finished piece
            # (select total_pieces_per_item colors from num_colors available)
            color_subset = random.sample(color_names, total_pieces_per_item)

            # Shuffle the selected colors into positions
            arrangement = color_subset.copy()
            random.shuffle(arrangement)

            # Convert to tuple for hashing (to check uniqueness)
            arrangement_tuple = tuple(arrangement)

            # Check if this arrangement is unique
            if arrangement_tuple not in used_arrangements:
                used_arrangements.add(arrangement_tuple)

                # Create template from arrangement
                template = {}
                position = 0

                for pt in piece_types:
                    template[pt.name] = []
                    for i in range(pt.count):
                        template[pt.name].append(arrangement[position])
                        position += 1

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
