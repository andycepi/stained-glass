#!/usr/bin/env python3
"""
Stained Glass Cutlist Generator
A lightweight desktop app for creating cutlists for stained glass projects
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from typing import List, Dict, Tuple
import math


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


class CutlistApp:
    """Main application window"""

    def __init__(self, root):
        self.root = root
        self.root.title("Stained Glass Cutlist Generator")
        self.root.geometry("900x700")

        # Set default values (tennis court example)
        self.piece_types = []

        # Create main container
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text="Stained Glass Cutlist Generator",
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Project Parameters", padding="10")
        input_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        # Number of piece types
        ttk.Label(input_frame, text="Number of piece types:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.num_types_var = tk.IntVar(value=2)
        ttk.Entry(input_frame, textvariable=self.num_types_var, width=10).grid(row=0, column=1, sticky=tk.W, padx=5)
        ttk.Button(input_frame, text="Set Piece Types", command=self.create_piece_type_inputs).grid(row=0, column=2, padx=5)

        # Piece types container
        self.piece_types_frame = ttk.Frame(input_frame)
        self.piece_types_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)

        # Number of colors
        ttk.Label(input_frame, text="Number of colors:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.num_colors_var = tk.IntVar(value=6)
        ttk.Entry(input_frame, textvariable=self.num_colors_var, width=10).grid(row=2, column=1, sticky=tk.W, padx=5)

        # Number of finished pieces
        ttk.Label(input_frame, text="Number of finished pieces:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.num_finished_var = tk.IntVar(value=10)
        ttk.Entry(input_frame, textvariable=self.num_finished_var, width=10).grid(row=3, column=1, sticky=tk.W, padx=5)

        # Calculate button
        ttk.Button(input_frame, text="Generate Cutlist", command=self.generate_cutlist,
                  style='Accent.TButton').grid(row=4, column=0, columnspan=3, pady=10)

        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        results_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        main_frame.rowconfigure(2, weight=1)

        # Results text area
        self.results_text = scrolledtext.ScrolledText(results_frame, width=100, height=25,
                                                      font=('Courier', 9))
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)

        # Initialize with default tennis court values
        self.create_piece_type_inputs()

    def create_piece_type_inputs(self):
        """Create input fields for each piece type"""
        # Clear existing widgets
        for widget in self.piece_types_frame.winfo_children():
            widget.destroy()

        self.piece_type_vars = []
        num_types = self.num_types_var.get()

        # Header
        ttk.Label(self.piece_types_frame, text="Type", font=('Arial', 9, 'bold')).grid(row=0, column=0, padx=5)
        ttk.Label(self.piece_types_frame, text="Count", font=('Arial', 9, 'bold')).grid(row=0, column=1, padx=5)
        ttk.Label(self.piece_types_frame, text="Width", font=('Arial', 9, 'bold')).grid(row=0, column=2, padx=5)
        ttk.Label(self.piece_types_frame, text="Height", font=('Arial', 9, 'bold')).grid(row=0, column=3, padx=5)

        # Default values for tennis court
        defaults = [
            ('A', 4, 1.0, 2.0),
            ('B', 2, 0.5, 4.0)
        ]

        for i in range(num_types):
            type_name = chr(65 + i)  # A, B, C, etc.

            # Use defaults if available
            if i < len(defaults):
                default = defaults[i]
            else:
                default = (type_name, 1, 1.0, 1.0)

            name_var = tk.StringVar(value=default[0])
            count_var = tk.IntVar(value=default[1])
            width_var = tk.DoubleVar(value=default[2])
            height_var = tk.DoubleVar(value=default[3])

            ttk.Entry(self.piece_types_frame, textvariable=name_var, width=8).grid(row=i+1, column=0, padx=5, pady=2)
            ttk.Entry(self.piece_types_frame, textvariable=count_var, width=8).grid(row=i+1, column=1, padx=5, pady=2)
            ttk.Entry(self.piece_types_frame, textvariable=width_var, width=8).grid(row=i+1, column=2, padx=5, pady=2)
            ttk.Entry(self.piece_types_frame, textvariable=height_var, width=8).grid(row=i+1, column=3, padx=5, pady=2)

            self.piece_type_vars.append((name_var, count_var, width_var, height_var))

    def generate_cutlist(self):
        """Generate and display the cutlist"""
        try:
            # Collect piece type data
            piece_types = []
            for name_var, count_var, width_var, height_var in self.piece_type_vars:
                pt = PieceType(
                    name_var.get(),
                    count_var.get(),
                    width_var.get(),
                    height_var.get()
                )
                piece_types.append(pt)

            num_colors = self.num_colors_var.get()
            num_finished = self.num_finished_var.get()

            # Calculate distribution
            result = ColorDistribution.calculate_distribution(piece_types, num_colors, num_finished)

            # Display results
            self.display_results(result, piece_types, num_colors, num_finished)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def display_results(self, result: Dict, piece_types: List[PieceType],
                       num_colors: int, num_finished: int):
        """Display the calculated results"""
        self.results_text.delete(1.0, tk.END)

        if 'error' in result:
            self.results_text.insert(tk.END, f"ERROR: {result['error']}\n")
            return

        output = []
        output.append("=" * 80)
        output.append("STAINED GLASS CUTLIST")
        output.append("=" * 80)
        output.append("")

        # Project summary
        output.append("PROJECT SUMMARY:")
        output.append("-" * 80)
        output.append(f"Number of finished pieces to create: {num_finished}")
        output.append(f"Number of colors available: {num_colors}")
        output.append(f"Pieces per finished item: {result['total_pieces_per_item']}")
        output.append("")

        output.append("Piece Types:")
        for pt in piece_types:
            output.append(f"  {pt.name}: {pt.count} pieces per finished item ({pt.width}\" x {pt.height}\")")
        output.append("")

        # Distribution statistics
        output.append("DISTRIBUTION STATISTICS:")
        output.append("-" * 80)
        output.append(f"Min pieces per color: {result['min_pieces_per_color']}")
        output.append(f"Max pieces per color: {result['max_pieces_per_color']}")
        output.append(f"Distribution variance: {result['max_pieces_per_color'] - result['min_pieces_per_color']}")
        output.append("")

        # Cutlist
        output.append("CUTLIST (Pieces to cut per color):")
        output.append("-" * 80)
        output.append(f"{'Color':<15} " + " ".join(f"{pt.name:>6}" for pt in piece_types) + f" {'Total':>7}")
        output.append("-" * 80)

        for color, pieces in sorted(result['cutlist'].items()):
            piece_counts = [f"{pieces[pt.name]:>6}" for pt in piece_types]
            total = sum(pieces.values())
            output.append(f"{color:<15} " + " ".join(piece_counts) + f" {total:>7}")

        output.append("-" * 80)

        # Totals
        totals = {pt.name: sum(result['cutlist'][color][pt.name]
                              for color in result['cutlist'])
                 for pt in piece_types}
        total_all = sum(totals.values())
        piece_counts = [f"{totals[pt.name]:>6}" for pt in piece_types]
        output.append(f"{'TOTAL':<15} " + " ".join(piece_counts) + f" {total_all:>7}")
        output.append("")

        # Templates
        output.append("TEMPLATES (Color arrangement for each finished piece):")
        output.append("-" * 80)

        for idx, template in enumerate(result['templates'][:5]):  # Show first 5
            output.append(f"\nFinished Piece #{idx + 1}:")
            for pt in piece_types:
                colors = ", ".join(template[pt.name])
                output.append(f"  {pt.name}: [{colors}]")

        if len(result['templates']) > 5:
            output.append(f"\n... and {len(result['templates']) - 5} more finished pieces")

        output.append("")
        output.append("=" * 80)

        # Insert into text widget
        self.results_text.insert(tk.END, "\n".join(output))


def main():
    """Main entry point"""
    root = tk.Tk()
    app = CutlistApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
