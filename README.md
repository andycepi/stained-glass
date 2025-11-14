# Stained Glass Cutlist Generator

A lightweight desktop application for creating optimized cutlists for stained glass projects.

## Features

- **Editable SVG Templates**: Create custom designs by editing simple SVG files!
- **Visual Diagrams**: See your stained glass designs with actual colors
- **10 Shades of Blue**: Beautiful gradient from light to dark blue (customizable)
- **Multi-piece type support**: Define different types of glass pieces (A, B, C, etc.) with custom dimensions
- **Smart color distribution**: Randomly generates unique color arrangements ensuring no color repeats in any finished piece
- **Optimal balancing**: Min-max algorithm for efficient distribution across colors
- **Interactive GUI**: Two-panel layout with visual templates and detailed cutlist data
- **Template Library**: Includes tennis court and simple grid examples
- **Scrollable gallery**: View multiple finished piece templates side-by-side
- **Color legend**: Visual color palette showing all available shades

## Requirements

- Python 3.6 or higher
- Tkinter (usually included with Python)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd stained-glass
```

2. Install dependencies (if needed):
```bash
pip install -r requirements.txt
```

Note: Tkinter is usually included with Python. If not available, install it:
- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **macOS**: Included with Python
- **Windows**: Included with Python

## Usage

### Running the Application

Simply run the main script:

```bash
python cutlist_app.py
```

Or make it executable and run directly:

```bash
chmod +x cutlist_app.py
./cutlist_app.py
```

### Using the Application

1. **Set the number of piece types** - How many different shapes you have (e.g., 2 for rectangles and squares)

2. **Click "Set Piece Types"** to create input fields

3. **Define each piece type**:
   - Name (A, B, C, etc.)
   - Count (how many of this type per finished piece)
   - Width (in inches)
   - Height (in inches)

4. **Set the number of colors** - How many different glass colors you have available

5. **Set the number of finished pieces** - How many complete pieces you want to make

6. **Click "Generate Cutlist"** to see your results

### Example: Tennis Court Project

The application comes pre-configured with a tennis court example:

- **Piece Type A**: 4 pieces per court (1" x 2" rectangles) - service boxes
- **Piece Type B**: 2 pieces per court (0.5" x 4" rectangles) - side lanes
- **Total pieces per court**: 6
- **Default colors**: 10 shades of blue
- **Default finished pieces**: 10

**Tennis Court Layout (Top-Down View):**
```
┌───────┬────────┬────────┬───────┐
│       │        │        │       │
│   B   │   A    │   A    │   B   │
│ 0.5x4 │  1x2   │  1x2   │ 0.5x4 │
│       ├────────┼────────┤       │
│       │   A    │   A    │       │
│       │  1x2   │  1x2   │       │
└───────┴────────┴────────┴───────┘
```

This generates:
- **Visual diagrams**: Color-coded tennis court layouts showing each piece
- **Cutlist table**: Exactly how many of each piece type to cut from each blue shade
- **Unique templates**: Each finished court has a different random color arrangement
- **Distribution statistics**: Min/max pieces per color for optimal cutting

### Output

The generated cutlist includes:

1. **Project Summary**: Overview of your project parameters
2. **Distribution Statistics**: Shows how evenly colors are distributed
3. **Cutlist Table**: Detailed breakdown of pieces to cut per color
4. **Templates**: Color arrangement for each finished piece (first 5 shown)

## Algorithm

The application uses a rotation-based algorithm to distribute colors:

1. Ensures no color appears more than once in any finished piece
2. Distributes colors as evenly as possible across all piece types
3. Minimizes the difference between the most-used and least-used colors
4. Provides clear templates showing which color goes where in each finished piece

## Example Output

```
================================================================================
STAINED GLASS CUTLIST
================================================================================

PROJECT SUMMARY:
--------------------------------------------------------------------------------
Number of finished pieces to create: 10
Number of colors available: 6
Pieces per finished item: 6

Piece Types:
  A: 4 pieces per finished item (1.0" x 2.0")
  B: 2 pieces per finished item (0.5" x 4.0")

DISTRIBUTION STATISTICS:
--------------------------------------------------------------------------------
Min pieces per color: 10
Max pieces per color: 10
Distribution variance: 0

CUTLIST (Pieces to cut per color):
--------------------------------------------------------------------------------
Color                 A      B   Total
--------------------------------------------------------------------------------
Color 1                7      3      10
Color 2                7      3      10
Color 3                6      4      10
Color 4                7      3      10
Color 5                7      3      10
Color 6                6      4      10
--------------------------------------------------------------------------------
TOTAL                 40     20      60

TEMPLATES (Color arrangement for each finished piece):
--------------------------------------------------------------------------------

Finished Piece #1:
  A: [Color 1, Color 2, Color 3, Color 4]
  B: [Color 5, Color 6]

Finished Piece #2:
  A: [Color 1, Color 2, Color 3, Color 4]
  B: [Color 5, Color 6]
...
```

## Tips

- **Minimum colors needed**: You need at least as many colors as total pieces per finished item
- **Even distribution**: The more colors you have, the more evenly distributed the cutting will be
- **Piece dimensions**: Use consistent units (inches recommended) for width and height

## Custom Templates

**Create your own designs!** The app uses editable SVG template files that you can customize:

### Using Templates

1. **Load a template**: Click "Load Template..." in the app
2. **View the design**: See your custom layout with colors
3. **Generate cutlist**: Get the cutting instructions

### Creating Custom Templates

Templates are simple SVG files. See [templates/TEMPLATE_GUIDE.md](templates/TEMPLATE_GUIDE.md) for a complete guide.

**Quick Example:**
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2 2">
  <rect data-piece-type="A" data-piece-id="0" x="0" y="0" width="1" height="1"/>
  <rect data-piece-type="A" data-piece-id="1" x="1" y="0" width="1" height="1"/>
  <rect data-piece-type="A" data-piece-id="2" x="0" y="1" width="1" height="1"/>
  <rect data-piece-type="A" data-piece-id="3" x="1" y="1" width="1" height="1"/>
</svg>
```

**Included Templates:**
- `tennis_court.svg` - Tennis court design (default)
- `simple_grid.svg` - 2×2 grid example

Edit templates with any text editor or SVG editor (Inkscape, Illustrator, etc.)!

## Visual Demo

For a detailed description of the visual output with screenshots and examples, see [VISUAL_DEMO.md](VISUAL_DEMO.md).

The visual display includes:
- Color palette legend with all 10 blue shades
- Custom design from your SVG template
- Color-coded pieces matching your cutlist
- Scrollable gallery of up to 9 templates

## Troubleshooting

**Error: "Need at least X colors"**
- You don't have enough colors to avoid repeating colors in a finished piece
- Solution: Add more colors or reduce the number of pieces per finished item

**Tkinter not found**
- Install Python with Tkinter support
- On Linux: `sudo apt-get install python3-tk`

## License

MIT License - feel free to use and modify for your stained glass projects!

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.
