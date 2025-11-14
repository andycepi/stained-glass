#!/usr/bin/env python3
"""
Stained Glass Cutlist Generator
A lightweight desktop app for creating cutlists for stained glass projects
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, Canvas
from typing import List, Dict, Tuple
import random


def generate_blue_shades(num_shades: int = 10) -> List[Tuple[str, str]]:
    """
    Generate shades of blue from light to dark.
    Returns list of tuples: (name, hex_color)
    """
    # Generate shades from light blue to dark blue
    blues = []
    for i in range(num_shades):
        # Interpolate between light blue (173, 216, 230) and dark blue (0, 0, 139)
        ratio = i / (num_shades - 1) if num_shades > 1 else 0

        # Light blue to dark blue gradient
        r = int(173 * (1 - ratio) + 0 * ratio)
        g = int(216 * (1 - ratio) + 0 * ratio)
        b = int(230 * (1 - ratio) + 139 * ratio)

        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        name = f"Blue {i+1}"
        blues.append((name, hex_color))

    return blues


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
                              num_finished_pieces: int,
                              color_palette: List[Tuple[str, str]] = None) -> Dict:
        """
        Calculate color distribution ensuring no color repeats in a finished piece.
        Returns distribution plan and templates for each finished piece.

        Args:
            piece_types: List of piece types
            num_colors: Number of colors to use
            num_finished_pieces: Number of finished pieces to create
            color_palette: Optional list of (name, hex_color) tuples
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

        # Use provided color palette or generate default names
        if color_palette:
            color_info = color_palette[:num_colors]
            color_names = [name for name, _ in color_info]
            color_map = {name: hex_color for name, hex_color in color_info}
        else:
            color_names = [f"Color {i+1}" for i in range(num_colors)]
            color_map = {name: None for name in color_names}

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
            'piece_types': piece_type_dict,
            'color_map': color_map  # Map of color names to hex values
        }


class CutlistApp:
    """Main application window"""

    def __init__(self, root):
        self.root = root
        self.root.title("Stained Glass Cutlist Generator")
        self.root.geometry("1400x800")

        # Set default values (tennis court example)
        self.piece_types = []
        self.color_palette = generate_blue_shades(10)  # 10 shades of blue by default
        self.current_result = None

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
        self.num_colors_var = tk.IntVar(value=10)
        ttk.Entry(input_frame, textvariable=self.num_colors_var, width=10).grid(row=2, column=1, sticky=tk.W, padx=5)

        # Number of finished pieces
        ttk.Label(input_frame, text="Number of finished pieces:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.num_finished_var = tk.IntVar(value=10)
        ttk.Entry(input_frame, textvariable=self.num_finished_var, width=10).grid(row=3, column=1, sticky=tk.W, padx=5)

        # Calculate button
        ttk.Button(input_frame, text="Generate Cutlist", command=self.generate_cutlist,
                  style='Accent.TButton').grid(row=4, column=0, columnspan=3, pady=10)

        # Create two-column layout for visual display and text results
        # Left column: Visual display
        visual_frame = ttk.LabelFrame(main_frame, text="Visual Templates", padding="10")
        visual_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5, padx=(0, 5))

        # Canvas with scrollbar for visual templates
        canvas_container = ttk.Frame(visual_frame)
        canvas_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        visual_frame.columnconfigure(0, weight=1)
        visual_frame.rowconfigure(0, weight=1)

        self.visual_canvas = Canvas(canvas_container, width=600, height=600, bg='white')
        v_scrollbar = ttk.Scrollbar(canvas_container, orient=tk.VERTICAL, command=self.visual_canvas.yview)
        self.visual_canvas.configure(yscrollcommand=v_scrollbar.set)

        self.visual_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Right column: Text results
        results_frame = ttk.LabelFrame(main_frame, text="Cutlist Data", padding="10")
        results_frame.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        main_frame.rowconfigure(2, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Results text area
        self.results_text = scrolledtext.ScrolledText(results_frame, width=60, height=25,
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

            # Update color palette if num_colors changed
            if num_colors != len(self.color_palette):
                self.color_palette = generate_blue_shades(num_colors)

            # Calculate distribution
            result = ColorDistribution.calculate_distribution(
                piece_types, num_colors, num_finished, self.color_palette
            )

            # Store result for visual display
            self.current_result = result
            self.current_piece_types = piece_types

            # Display results
            self.display_results(result, piece_types, num_colors, num_finished)
            self.draw_visual_templates(result, piece_types)

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

    def draw_tennis_court(self, canvas: Canvas, x: int, y: int, template: Dict,
                         color_map: Dict, scale: int = 50) -> int:
        """
        Draw a single tennis court with colored pieces.

        Args:
            canvas: The canvas to draw on
            x, y: Top-left position
            template: Color template for this court
            color_map: Map of color names to hex values
            scale: Pixels per inch

        Returns:
            Height of the drawn court in pixels
        """
        # Tennis court layout (assuming standard tennis court piece arrangement):
        # Left B piece (0.5x4) | Center A pieces in 2x2 grid (each 1x2) | Right B piece (0.5x4)

        # Get colors for each piece
        a_colors = template.get('A', [])
        b_colors = template.get('B', [])

        # Court dimensions
        court_width = 3.0  # 0.5 + 1 + 1 + 0.5
        court_height = 4.0

        # Draw border
        border_width = int(court_width * scale)
        border_height = int(court_height * scale)
        canvas.create_rectangle(x, y, x + border_width, y + border_height,
                              outline='black', width=2)

        # Draw Left B piece (0.5 x 4)
        if len(b_colors) > 0:
            b_left_color = color_map.get(b_colors[0], '#cccccc')
            canvas.create_rectangle(
                x, y,
                x + int(0.5 * scale), y + int(4 * scale),
                fill=b_left_color, outline='black', width=1
            )
            # Label
            canvas.create_text(
                x + int(0.25 * scale), y + int(2 * scale),
                text='B', font=('Arial', 10, 'bold'), fill='white'
            )

        # Draw Right B piece (0.5 x 4)
        if len(b_colors) > 1:
            b_right_color = color_map.get(b_colors[1], '#cccccc')
            canvas.create_rectangle(
                x + int(2.5 * scale), y,
                x + int(3 * scale), y + int(4 * scale),
                fill=b_right_color, outline='black', width=1
            )
            # Label
            canvas.create_text(
                x + int(2.75 * scale), y + int(2 * scale),
                text='B', font=('Arial', 10, 'bold'), fill='white'
            )

        # Draw 4 A pieces in 2x2 grid (each 1x2)
        a_positions = [
            (0.5, 0, 1.5, 2),    # Top-left A
            (1.5, 0, 2.5, 2),    # Top-right A
            (0.5, 2, 1.5, 4),    # Bottom-left A
            (1.5, 2, 2.5, 4),    # Bottom-right A
        ]

        for idx, (x1, y1, x2, y2) in enumerate(a_positions):
            if idx < len(a_colors):
                a_color = color_map.get(a_colors[idx], '#cccccc')
                canvas.create_rectangle(
                    x + int(x1 * scale), y + int(y1 * scale),
                    x + int(x2 * scale), y + int(y2 * scale),
                    fill=a_color, outline='black', width=1
                )
                # Label
                canvas.create_text(
                    x + int((x1 + x2) / 2 * scale), y + int((y1 + y2) / 2 * scale),
                    text='A', font=('Arial', 12, 'bold'), fill='white'
                )

        return border_height

    def draw_visual_templates(self, result: Dict, piece_types: List[PieceType]):
        """Draw visual representations of the templates"""
        # Clear canvas
        self.visual_canvas.delete('all')

        if 'error' in result:
            self.visual_canvas.create_text(
                300, 300, text=result['error'],
                font=('Arial', 12), fill='red', width=500
            )
            return

        templates = result['templates']
        color_map = result['color_map']

        # Drawing parameters
        scale = 50  # pixels per inch
        margin = 20
        spacing = 30
        templates_per_row = 3

        y_offset = margin
        x_offset = margin

        # Draw color legend first
        legend_y = y_offset
        self.visual_canvas.create_text(
            x_offset, legend_y,
            text="Color Palette:", font=('Arial', 12, 'bold'),
            anchor='nw'
        )
        legend_y += 25

        # Draw color swatches
        for idx, (color_name, hex_color) in enumerate(self.color_palette):
            swatch_x = x_offset + (idx % 5) * 110
            swatch_y = legend_y + (idx // 5) * 25

            self.visual_canvas.create_rectangle(
                swatch_x, swatch_y,
                swatch_x + 20, swatch_y + 20,
                fill=hex_color, outline='black'
            )
            self.visual_canvas.create_text(
                swatch_x + 25, swatch_y + 10,
                text=color_name, font=('Arial', 9),
                anchor='w'
            )

        # Update y_offset after legend
        y_offset = legend_y + ((len(self.color_palette) - 1) // 5 + 1) * 25 + spacing

        # Draw templates (show first 9)
        max_templates = min(9, len(templates))

        for idx in range(max_templates):
            template = templates[idx]

            # Calculate position
            col = idx % templates_per_row
            row = idx // templates_per_row

            x = margin + col * (3 * scale + spacing + 50)
            y = y_offset + row * (4 * scale + spacing + 40)

            # Draw title
            self.visual_canvas.create_text(
                x, y - 20,
                text=f"Piece #{idx + 1}",
                font=('Arial', 10, 'bold'),
                anchor='nw'
            )

            # Draw court
            height = self.draw_tennis_court(
                self.visual_canvas, x, y, template, color_map, scale
            )

        # Update scroll region
        total_rows = (max_templates - 1) // templates_per_row + 1
        total_height = y_offset + total_rows * (4 * scale + spacing + 40) + margin
        self.visual_canvas.configure(scrollregion=(0, 0, 600, total_height))

        if len(templates) > max_templates:
            # Add note about more templates
            note_y = y_offset + total_rows * (4 * scale + spacing + 40)
            self.visual_canvas.create_text(
                margin, note_y,
                text=f"... and {len(templates) - max_templates} more templates",
                font=('Arial', 10, 'italic'),
                anchor='nw'
            )


def main():
    """Main entry point"""
    root = tk.Tk()
    app = CutlistApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
