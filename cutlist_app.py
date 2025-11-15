#!/usr/bin/env python3
"""
Stained Glass Cutlist Generator
A lightweight desktop app for creating cutlists for stained glass projects
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, Canvas, filedialog
from typing import List, Dict, Tuple, Optional
import random
import os
from template_parser import load_template, TemplatePiece


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
        self.root.geometry("1600x900")

        # Set default values (tennis court example)
        self.piece_types = []
        self.color_palette = generate_blue_shades(10)  # 10 shades of blue by default
        self.current_result = None
        self.template_data = None  # Loaded SVG template
        self.template_path = None

        # Try to load default template
        default_template = os.path.join(os.path.dirname(__file__), 'templates', 'tennis_court.svg')
        if os.path.exists(default_template):
            try:
                self.template_data = load_template(default_template)
                self.template_path = default_template
            except Exception as e:
                print(f"Warning: Could not load default template: {e}")

        # Create main container
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text="Stained Glass Cutlist Generator",
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        # Left sidebar for controls (compact)
        sidebar = ttk.Frame(main_frame, width=300)
        sidebar.grid(row=1, column=0, sticky=(tk.W, tk.N, tk.S), padx=(0, 10))
        sidebar.grid_propagate(False)

        # Input section (compact)
        input_frame = ttk.LabelFrame(sidebar, text="Settings", padding="8")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N), pady=(0, 5))

        # Number of piece types
        ttk.Label(input_frame, text="Piece types:", font=('Arial', 8)).grid(row=0, column=0, sticky=tk.W, pady=2)
        self.num_types_var = tk.IntVar(value=2)
        ttk.Entry(input_frame, textvariable=self.num_types_var, width=8).grid(row=0, column=1, sticky=tk.W, padx=3)
        ttk.Button(input_frame, text="Set", command=self.create_piece_type_inputs, width=6).grid(row=0, column=2, padx=2)

        # Piece types container
        self.piece_types_frame = ttk.Frame(input_frame)
        self.piece_types_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=3)

        # Number of colors
        ttk.Label(input_frame, text="Colors:", font=('Arial', 8)).grid(row=2, column=0, sticky=tk.W, pady=2)
        self.num_colors_var = tk.IntVar(value=10)
        ttk.Entry(input_frame, textvariable=self.num_colors_var, width=8).grid(row=2, column=1, sticky=tk.W, padx=3, columnspan=2)

        # Number of finished pieces
        ttk.Label(input_frame, text="Finished pieces:", font=('Arial', 8)).grid(row=3, column=0, sticky=tk.W, pady=2)
        self.num_finished_var = tk.IntVar(value=10)
        ttk.Entry(input_frame, textvariable=self.num_finished_var, width=8).grid(row=3, column=1, sticky=tk.W, padx=3, columnspan=2)

        # Template selection
        ttk.Label(input_frame, text="Template:", font=('Arial', 8)).grid(row=4, column=0, sticky=tk.W, pady=2)
        self.template_label = ttk.Label(input_frame, text="tennis_court.svg", foreground='blue', font=('Arial', 8))
        self.template_label.grid(row=5, column=0, columnspan=3, sticky=tk.W, pady=(0, 2))
        ttk.Button(input_frame, text="Load Template...", command=self.load_template, width=15).grid(row=6, column=0, columnspan=3, pady=2)

        # Calculate button (prominent)
        ttk.Button(input_frame, text="Generate Cutlist", command=self.generate_cutlist,
                  style='Accent.TButton').grid(row=7, column=0, columnspan=3, pady=(8, 0), sticky=(tk.W, tk.E))

        # Cutlist data section (compact, collapsible)
        cutlist_frame = ttk.LabelFrame(sidebar, text="Cutlist Data", padding="5")
        cutlist_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(5, 0))
        sidebar.rowconfigure(1, weight=1)

        # Results text area (smaller, compact)
        text_container = ttk.Frame(cutlist_frame)
        text_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        cutlist_frame.columnconfigure(0, weight=1)
        cutlist_frame.rowconfigure(0, weight=1)

        self.results_text = scrolledtext.ScrolledText(text_container, width=35, height=20,
                                                      font=('Courier', 7), wrap=tk.NONE)
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        text_container.columnconfigure(0, weight=1)
        text_container.rowconfigure(0, weight=1)

        # Horizontal scrollbar for long lines
        h_scrollbar = ttk.Scrollbar(text_container, orient=tk.HORIZONTAL, command=self.results_text.xview)
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.results_text.configure(xscrollcommand=h_scrollbar.set)

        # Export buttons (compact)
        button_frame = ttk.Frame(cutlist_frame)
        button_frame.grid(row=1, column=0, pady=(3, 0))
        ttk.Button(button_frame, text="Export...",
                  command=self.export_cutlist, width=12).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Copy",
                  command=self.copy_to_clipboard, width=12).pack(side=tk.LEFT, padx=2)

        # Store full output for export
        self.full_output_text = ""

        # Main visual display (large, prominent)
        visual_frame = ttk.LabelFrame(main_frame, text="Visual Design Preview", padding="10")
        visual_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.rowconfigure(1, weight=1)
        main_frame.columnconfigure(1, weight=10)  # Give most space to visual

        # Canvas with scrollbar for visual templates
        canvas_container = ttk.Frame(visual_frame)
        canvas_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        visual_frame.columnconfigure(0, weight=1)
        visual_frame.rowconfigure(0, weight=1)

        self.visual_canvas = Canvas(canvas_container, bg='white')
        v_scrollbar = ttk.Scrollbar(canvas_container, orient=tk.VERTICAL, command=self.visual_canvas.yview)
        h_scrollbar_canvas = ttk.Scrollbar(canvas_container, orient=tk.HORIZONTAL, command=self.visual_canvas.xview)
        self.visual_canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar_canvas.set)

        self.visual_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar_canvas.grid(row=1, column=0, sticky=(tk.W, tk.E))
        canvas_container.columnconfigure(0, weight=1)
        canvas_container.rowconfigure(0, weight=1)

        # Initialize with default tennis court values
        self.create_piece_type_inputs()

    def create_piece_type_inputs(self):
        """Create input fields for each piece type"""
        # Clear existing widgets
        for widget in self.piece_types_frame.winfo_children():
            widget.destroy()

        self.piece_type_vars = []
        num_types = self.num_types_var.get()

        # Header (compact)
        ttk.Label(self.piece_types_frame, text="T", font=('Arial', 7, 'bold')).grid(row=0, column=0, padx=2)
        ttk.Label(self.piece_types_frame, text="#", font=('Arial', 7, 'bold')).grid(row=0, column=1, padx=2)
        ttk.Label(self.piece_types_frame, text="W", font=('Arial', 7, 'bold')).grid(row=0, column=2, padx=2)
        ttk.Label(self.piece_types_frame, text="H", font=('Arial', 7, 'bold')).grid(row=0, column=3, padx=2)

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

            ttk.Entry(self.piece_types_frame, textvariable=name_var, width=4, font=('Arial', 8)).grid(row=i+1, column=0, padx=2, pady=1)
            ttk.Entry(self.piece_types_frame, textvariable=count_var, width=4, font=('Arial', 8)).grid(row=i+1, column=1, padx=2, pady=1)
            ttk.Entry(self.piece_types_frame, textvariable=width_var, width=5, font=('Arial', 8)).grid(row=i+1, column=2, padx=2, pady=1)
            ttk.Entry(self.piece_types_frame, textvariable=height_var, width=5, font=('Arial', 8)).grid(row=i+1, column=3, padx=2, pady=1)

            self.piece_type_vars.append((name_var, count_var, width_var, height_var))

    def load_template(self):
        """Load a custom SVG template"""
        filename = filedialog.askopenfilename(
            title="Select SVG Template",
            filetypes=[("SVG files", "*.svg"), ("All files", "*.*")],
            initialdir=os.path.join(os.path.dirname(__file__), 'templates')
        )

        if filename:
            try:
                self.template_data = load_template(filename)
                self.template_path = filename
                template_name = os.path.basename(filename)
                self.template_label.config(text=template_name)
                messagebox.showinfo("Success", f"Template loaded: {template_name}\n\n"
                                             f"Found {len(self.template_data['pieces'])} pieces:\n" +
                                             "\n".join(f"  Type {k}: {v} pieces"
                                                      for k, v in sorted(self.template_data['piece_types'].items())))
            except Exception as e:
                messagebox.showerror("Error", f"Could not load template:\n{str(e)}")

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

        # Templates - Show ALL templates
        output.append("TEMPLATES (Color arrangement for each finished piece):")
        output.append("-" * 80)

        for idx, template in enumerate(result['templates']):  # Show ALL templates
            output.append(f"\nFinished Piece #{idx + 1}:")
            for pt in piece_types:
                colors = ", ".join(template[pt.name])
                output.append(f"  {pt.name}: [{colors}]")

        output.append("")
        output.append("=" * 80)
        output.append(f"Total finished pieces: {len(result['templates'])}")
        output.append("=" * 80)

        # Store full output for export
        self.full_output_text = "\n".join(output)

        # Insert into text widget
        self.results_text.insert(tk.END, self.full_output_text)

    def export_cutlist(self):
        """Export cutlist to a text file"""
        if not self.full_output_text:
            messagebox.showwarning("No Data", "Generate a cutlist first before exporting.")
            return

        # Ask for save location
        filename = filedialog.asksaveasfilename(
            title="Export Cutlist",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile="stained_glass_cutlist.txt"
        )

        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.full_output_text)
                messagebox.showinfo("Success", f"Cutlist exported to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not export file:\n{str(e)}")

    def copy_to_clipboard(self):
        """Copy cutlist to clipboard"""
        if not self.full_output_text:
            messagebox.showwarning("No Data", "Generate a cutlist first before copying.")
            return

        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.full_output_text)
            messagebox.showinfo("Success", "Cutlist copied to clipboard!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not copy to clipboard:\n{str(e)}")

    def draw_from_template(self, canvas: Canvas, x: int, y: int, color_template: Dict,
                          color_map: Dict, scale: int = 70) -> Tuple[int, int]:
        """
        Draw a piece from SVG template with colored pieces.

        Args:
            canvas: The canvas to draw on
            x, y: Top-left position
            color_template: Color assignments for this piece (e.g., {'A': ['Blue 1', 'Blue 2'], 'B': [...]})
            color_map: Map of color names to hex values
            scale: Pixels per inch

        Returns:
            (width, height) of the drawn template in pixels
        """
        if not self.template_data:
            # Fallback to default drawing if no template
            return (150, 200)

        template_pieces = self.template_data['pieces']
        template_width = self.template_data['width']
        template_height = self.template_data['height']

        # Draw border
        border_width = int(template_width * scale)
        border_height = int(template_height * scale)
        canvas.create_rectangle(x, y, x + border_width, y + border_height,
                              outline='black', width=2)

        # Draw each piece from template
        for piece in template_pieces:
            piece_type = piece.piece_type
            piece_id = piece.piece_id

            # Get color for this piece
            colors_for_type = color_template.get(piece_type, [])
            if piece_id < len(colors_for_type):
                color_name = colors_for_type[piece_id]
                fill_color = color_map.get(color_name, '#cccccc')
            else:
                fill_color = '#cccccc'

            if piece.shape == 'rect':
                # Draw rectangle
                canvas.create_rectangle(
                    x + int(piece.x * scale),
                    y + int(piece.y * scale),
                    x + int((piece.x + piece.width) * scale),
                    y + int((piece.y + piece.height) * scale),
                    fill=fill_color, outline='black', width=1
                )

                # Add label (larger font for better visibility)
                center_x = x + int((piece.x + piece.width / 2) * scale)
                center_y = y + int((piece.y + piece.height / 2) * scale)
                canvas.create_text(
                    center_x, center_y,
                    text=piece_type,
                    font=('Arial', 16, 'bold'),
                    fill='white'
                )

        return (border_width, border_height)

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

        # Drawing parameters (larger for prominent display)
        scale = 70  # pixels per inch (increased from 50 for better visibility)
        margin = 30
        spacing = 40
        templates_per_row = 3

        # Get template dimensions
        if self.template_data:
            template_width = self.template_data['width']
            template_height = self.template_data['height']
        else:
            template_width = 3.0
            template_height = 4.0

        y_offset = margin
        x_offset = margin

        # Draw color legend first
        legend_y = y_offset
        self.visual_canvas.create_text(
            x_offset, legend_y,
            text="Color Palette:", font=('Arial', 14, 'bold'),
            anchor='nw'
        )
        legend_y += 30

        # Draw color swatches (larger for better visibility)
        for idx, (color_name, hex_color) in enumerate(self.color_palette):
            swatch_x = x_offset + (idx % 5) * 120
            swatch_y = legend_y + (idx // 5) * 30

            self.visual_canvas.create_rectangle(
                swatch_x, swatch_y,
                swatch_x + 25, swatch_y + 25,
                fill=hex_color, outline='black', width=2
            )
            self.visual_canvas.create_text(
                swatch_x + 30, swatch_y + 12,
                text=color_name, font=('Arial', 10),
                anchor='w'
            )

        # Update y_offset after legend
        y_offset = legend_y + ((len(self.color_palette) - 1) // 5 + 1) * 30 + spacing

        # Draw ALL templates (not just first 9)
        num_templates = len(templates)

        for idx in range(num_templates):
            template = templates[idx]

            # Calculate position
            col = idx % templates_per_row
            row = idx // templates_per_row

            piece_width_px = int(template_width * scale)
            piece_height_px = int(template_height * scale)

            x = margin + col * (piece_width_px + spacing + 50)
            y = y_offset + row * (piece_height_px + spacing + 40)

            # Draw title (larger for better visibility)
            self.visual_canvas.create_text(
                x, y - 25,
                text=f"Piece #{idx + 1}",
                font=('Arial', 12, 'bold'),
                anchor='nw'
            )

            # Draw from template
            width, height = self.draw_from_template(
                self.visual_canvas, x, y, template, color_map, scale
            )

        # Update scroll region to fit ALL templates
        total_rows = (num_templates - 1) // templates_per_row + 1
        piece_height_px = int(template_height * scale)
        piece_width_px = int(template_width * scale)
        total_width = margin + templates_per_row * (piece_width_px + spacing + 50) + margin
        total_height = y_offset + total_rows * (piece_height_px + spacing + 40) + margin
        self.visual_canvas.configure(scrollregion=(0, 0, total_width, total_height))


def main():
    """Main entry point"""
    root = tk.Tk()
    app = CutlistApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
