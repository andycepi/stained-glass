# SVG Helper Script

Quick tool to add piece attributes to SVG files exported from Illustrator or other editors.

## The Problem

When you export an SVG from Illustrator, it **doesn't preserve** the `data-piece-type` and `data-piece-id` attributes that the app needs to identify pieces.

## The Solution

Use this helper script to interactively add attributes to your SVG shapes!

## Usage

```bash
python svg_helper.py your_design.svg
```

The script will:
1. Load your SVG file
2. Find all shapes (rectangles, paths, etc.)
3. Ask you to assign a piece type and ID to each shape
4. Save the annotated SVG as `your_design_annotated.svg`

## Example Session

```
$ python svg_helper.py my_design.svg

Found 6 shapes in the SVG file.

For each shape, enter the piece type (A, B, C, etc.) and piece ID (0, 1, 2, etc.)
Or press Enter to skip a shape.

--- Shape 1/6 (rect) ---
  Position: (0.5, 0)  Size: 1 × 2
  ID: rect1
  Piece type (A/B/C/etc. or Enter to skip): A
  Piece ID (default: 0):
  ✓ Added: data-piece-type="A" data-piece-id="0"

--- Shape 2/6 (rect) ---
  Position: (1.5, 0)  Size: 1 × 2
  ID: rect2
  Piece type (A/B/C/etc. or Enter to skip): A
  Piece ID (default: 1):
  ✓ Added: data-piece-type="A" data-piece-id="1"

...

✓ Annotated SVG saved to: my_design_annotated.svg

Piece types found:
  Type A: 4 pieces
  Type B: 2 pieces
```

## Tips

- **Piece IDs auto-increment**: When you specify a type (like "A"), the script automatically suggests the next ID
- **Press Enter for defaults**: Just press Enter to use the suggested piece ID
- **Skip unwanted shapes**: Press Enter without typing anything to skip shapes you don't want as pieces
- **Load the annotated file**: Use `my_design_annotated.svg` in the app

## Manual Alternative

If you prefer, you can edit the SVG in a text editor:

```xml
<!-- Add these attributes to each shape -->
<rect x="0.5" y="0" width="1" height="2"
      data-piece-type="A"
      data-piece-id="0"/>
```

## For Advanced Users: Batch Mode

You can also use the script programmatically in Python:

```python
from svg_helper import batch_annotate

# Define pieces in order they appear in the SVG
pieces = [
    ('A', 0), ('A', 1), ('A', 2), ('A', 3),  # 4 A pieces
    ('B', 0), ('B', 1)                        # 2 B pieces
]

batch_annotate('design.svg', pieces)
```

## Supported Shape Types

The script recognizes:
- `<rect>` - Rectangles
- `<path>` - Paths
- `<circle>` - Circles
- `<ellipse>` - Ellipses
- `<polygon>` - Polygons

## What It Does

1. Parses your SVG file
2. Finds all shape elements
3. Adds `data-piece-type` and `data-piece-id` attributes
4. Saves to a new file (preserves original)

## Troubleshooting

**"Error: File not found"**
- Check the file path
- Make sure you're in the right directory

**"Shape not showing in app"**
- Verify the attributes were added: open the annotated SVG in a text editor
- Check for typos in attribute names
- Ensure piece IDs start at 0 and are sequential

## Quick Workflow

1. **Design in Illustrator** → Create your layout
2. **Export as SVG** → File → Save As → SVG
3. **Run helper script** → `python svg_helper.py design.svg`
4. **Load in app** → Use `design_annotated.svg`

Done!
