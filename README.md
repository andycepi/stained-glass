# Stained Glass Cutlist Generator

A lightweight desktop application for creating optimized cutlists for stained glass projects.

## Features

- **Multi-piece type support**: Define different types of glass pieces (A, B, C, etc.) with custom dimensions
- **Smart color distribution**: Automatically calculates color distribution ensuring no color repeats in any finished piece
- **Optimal balancing**: Min-max algorithm for efficient distribution across colors
- **Visual templates**: Shows color arrangement for each finished piece
- **Detailed cutlist**: Generates a complete cutting list showing exactly how many pieces of each type to cut from each color

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

- **Piece Type A**: 4 pieces per court (1" x 2" rectangles)
- **Piece Type B**: 2 pieces per court (0.5" x 4" rectangles)
- **Total pieces per court**: 6
- **Default colors**: 6
- **Default finished pieces**: 10

This generates a cutlist showing:
- Exactly how many of each piece type to cut from each color
- The color arrangement for each finished tennis court
- Distribution statistics (min/max pieces per color)

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
