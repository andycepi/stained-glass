# SVG Template Guide

Create custom stained glass designs by editing SVG template files!

## Overview

Templates are SVG files that define the shape and layout of your stained glass pieces. You can create custom designs by editing these files in any text editor or SVG editor (like Inkscape, Adobe Illustrator, or even a simple text editor).

## Template Structure

Each template is a standard SVG file with special `data-` attributes to identify pieces:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 WIDTH HEIGHT"
     width="WIDTHin"
     height="HEIGHTin">

  <!-- Your pieces go here -->

</svg>
```

### Required Attributes

Each piece must have these attributes:

- **`data-piece-type`**: The type of piece (A, B, C, etc.)
- **`data-piece-id`**: The index of this piece within its type (0, 1, 2, etc.)

### Supported Shapes

#### Rectangles

```xml
<rect id="unique-id"
      data-piece-type="A"
      data-piece-id="0"
      x="0.5"
      y="0"
      width="1"
      height="2"
      fill="none"
      stroke="black"
      stroke-width="0.02"/>
```

**Attributes:**
- `x`, `y`: Position (in inches)
- `width`, `height`: Size (in inches)
- `fill`: Keep as "none" (colors will be added by the app)
- `stroke`: Border color
- `stroke-width`: Border thickness

## Creating a New Template

### Step 1: Start with the Basic Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 4 6"
     width="4in"
     height="6in">

  <title>My Custom Design</title>

  <!-- Pieces will go here -->

</svg>
```

### Step 2: Add Your Pieces

For each piece in your design:

1. Decide its type (A, B, C, etc.)
2. Give it a unique ID within that type (0, 1, 2, etc.)
3. Define its position and size

**Example: A simple 2x2 grid**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 2 2"
     width="2in"
     height="2in">

  <title>Simple 2x2 Grid</title>

  <!-- Top-left square -->
  <rect data-piece-type="A"
        data-piece-id="0"
        x="0"
        y="0"
        width="1"
        height="1"
        fill="none"
        stroke="black"
        stroke-width="0.02"/>

  <!-- Top-right square -->
  <rect data-piece-type="A"
        data-piece-id="1"
        x="1"
        y="0"
        width="1"
        height="1"
        fill="none"
        stroke="black"
        stroke-width="0.02"/>

  <!-- Bottom-left square -->
  <rect data-piece-type="A"
        data-piece-id="2"
        x="0"
        y="1"
        width="1"
        height="1"
        fill="none"
        stroke="black"
        stroke-width="0.02"/>

  <!-- Bottom-right square -->
  <rect data-piece-type="A"
        data-piece-id="3"
        x="1"
        y="1"
        width="1"
        height="1"
        fill="none"
        stroke="black"
        stroke-width="0.02"/>

</svg>
```

This creates a 2"×2" design with 4 type A pieces.

### Step 3: Test Your Template

1. Save your SVG file in the `templates/` directory
2. Open the Stained Glass Cutlist Generator
3. Click "Load Template..." and select your file
4. Verify the piece counts are correct
5. Generate a cutlist to see your design with colors!

## Tips and Best Practices

### Coordinate System

- The `viewBox` defines the coordinate system
- Units are in inches by default
- Origin (0,0) is at the top-left corner
- X increases to the right
- Y increases downward

### Piece Numbering

- Number pieces consistently (0, 1, 2, 3, ...)
- Don't skip numbers
- The order doesn't matter, but consistency helps

**Good:**
```
Type A: pieces 0, 1, 2, 3
Type B: pieces 0, 1
```

**Bad:**
```
Type A: pieces 0, 2, 5, 7  ← Skipped numbers!
Type B: pieces 1, 2        ← Should start at 0!
```

### Dimensions

- Use consistent units throughout
- Keep stroke-width small (0.01 - 0.03) relative to your pieces
- The viewBox should match your actual dimensions

### Visual Aids (Optional)

You can add decorative elements (not pieces) without the `data-piece-type` attribute:

```xml
<!-- Reference lines (won't be treated as pieces) -->
<line x1="0" y1="2" x2="4" y2="2"
      stroke="gray"
      stroke-width="0.01"
      stroke-dasharray="0.1,0.05"/>

<!-- Text labels -->
<text x="1" y="0.5" font-size="0.2">Center</text>
```

## Example Templates

### Checkerboard (4×4)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 4 4"
     width="4in"
     height="4in">

  <title>Checkerboard Pattern</title>

  <!-- 16 squares in a 4x4 grid -->
  <!-- Row 1 -->
  <rect data-piece-type="A" data-piece-id="0"  x="0" y="0" width="1" height="1" fill="none" stroke="black" stroke-width="0.02"/>
  <rect data-piece-type="A" data-piece-id="1"  x="1" y="0" width="1" height="1" fill="none" stroke="black" stroke-width="0.02"/>
  <rect data-piece-type="A" data-piece-id="2"  x="2" y="0" width="1" height="1" fill="none" stroke="black" stroke-width="0.02"/>
  <rect data-piece-type="A" data-piece-id="3"  x="3" y="0" width="1" height="1" fill="none" stroke="black" stroke-width="0.02"/>

  <!-- Row 2 -->
  <rect data-piece-type="A" data-piece-id="4"  x="0" y="1" width="1" height="1" fill="none" stroke="black" stroke-width="0.02"/>
  <rect data-piece-type="A" data-piece-id="5"  x="1" y="1" width="1" height="1" fill="none" stroke="black" stroke-width="0.02"/>
  <rect data-piece-type="A" data-piece-id="6"  x="2" y="1" width="1" height="1" fill="none" stroke="black" stroke-width="0.02"/>
  <rect data-piece-type="A" data-piece-id="7"  x="3" y="1" width="1" height="1" fill="none" stroke="black" stroke-width="0.02"/>

  <!-- Row 3 -->
  <rect data-piece-type="A" data-piece-id="8"  x="0" y="2" width="1" height="1" fill="none" stroke="black" stroke-width="0.02"/>
  <rect data-piece-type="A" data-piece-id="9"  x="1" y="2" width="1" height="1" fill="none" stroke="black" stroke-width="0.02"/>
  <rect data-piece-type="A" data-piece-id="10" x="2" y="2" width="1" height="1" fill="none" stroke="black" stroke-width="0.02"/>
  <rect data-piece-type="A" data-piece-id="11" x="3" y="2" width="1" height="1" fill="none" stroke="black" stroke-width="0.02"/>

  <!-- Row 4 -->
  <rect data-piece-type="A" data-piece-id="12" x="0" y="3" width="1" height="1" fill="none" stroke="black" stroke-width="0.02"/>
  <rect data-piece-type="A" data-piece-id="13" x="1" y="3" width="1" height="1" fill="none" stroke="black" stroke-width="0.02"/>
  <rect data-piece-type="A" data-piece-id="14" x="2" y="3" width="1" height="1" fill="none" stroke="black" stroke-width="0.02"/>
  <rect data-piece-type="A" data-piece-id="15" x="3" y="3" width="1" height="1" fill="none" stroke="black" stroke-width="0.02"/>

</svg>
```

### Window Frame

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 6 8"
     width="6in"
     height="8in">

  <title>Window Frame</title>

  <!-- Frame (Type B) -->
  <rect data-piece-type="B" data-piece-id="0" x="0"   y="0" width="6"   height="0.5" fill="none" stroke="black" stroke-width="0.02"/>
  <rect data-piece-type="B" data-piece-id="1" x="0"   y="7.5" width="6"   height="0.5" fill="none" stroke="black" stroke-width="0.02"/>
  <rect data-piece-type="B" data-piece-id="2" x="0"   y="0.5" width="0.5" height="7"   fill="none" stroke="black" stroke-width="0.02"/>
  <rect data-piece-type="B" data-piece-id="3" x="5.5" y="0.5" width="0.5" height="7"   fill="none" stroke="black" stroke-width="0.02"/>

  <!-- Glass panes (Type A - 2x3 grid) -->
  <rect data-piece-type="A" data-piece-id="0" x="0.5"   y="0.5"   width="2.5" height="2.33" fill="none" stroke="black" stroke-width="0.02"/>
  <rect data-piece-type="A" data-piece-id="1" x="3"     y="0.5"   width="2.5" height="2.33" fill="none" stroke="black" stroke-width="0.02"/>
  <rect data-piece-type="A" data-piece-id="2" x="0.5"   y="2.83"  width="2.5" height="2.34" fill="none" stroke="black" stroke-width="0.02"/>
  <rect data-piece-type="A" data-piece-id="3" x="3"     y="2.83"  width="2.5" height="2.34" fill="none" stroke="black" stroke-width="0.02"/>
  <rect data-piece-type="A" data-piece-id="4" x="0.5"   y="5.17"  width="2.5" height="2.33" fill="none" stroke="black" stroke-width="0.02"/>
  <rect data-piece-type="A" data-piece-id="5" x="3"     y="5.17"  width="2.5" height="2.33" fill="none" stroke="black" stroke-width="0.02"/>

</svg>
```

## Editing with SVG Editors

### Adobe Illustrator (Recommended Workflow)

**Problem**: Illustrator doesn't easily preserve custom `data-*` attributes.

**Solution**: Design in Illustrator, then add attributes in a text editor.

**Steps:**
1. Create your design in Illustrator
2. File → Save As → SVG
3. Open the saved SVG in a text editor
4. Add `data-piece-type` and `data-piece-id` to each shape
5. Save and load in the app

**Quick tip**: Use our helper script!
```bash
python svg_helper.py your_design.svg
```

This script will interactively guide you through adding attributes to each shape.

### Inkscape (Free - Best for Templates)

**Inkscape preserves custom attributes!** This is the easiest SVG editor for templates.

1. Create your shapes using the rectangle tool
2. Select each shape
3. Open XML Editor (Edit → XML Editor)
4. Click on the shape's node
5. Add custom attributes:
   - Click "Add" at bottom
   - Name: `data-piece-type`, Value: `A`
   - Click "Add" again
   - Name: `data-piece-id`, Value: `0`
6. Save as "Plain SVG"

### Text Editor (Most Reliable!)

**Best method**: Just edit the SVG file directly in any text editor. The XML structure is simple and human-readable.

Works with any text editor:
- VS Code (recommended - has XML syntax highlighting)
- Notepad++
- Sublime Text
- Even plain Notepad!

## Troubleshooting

### "Found 0 pieces" (Most Common Issue!)

**Cause**: The SVG doesn't have `data-piece-type` and `data-piece-id` attributes.

**This happens when:**
- You exported from Illustrator/Photoshop without adding attributes
- You used "Save As" instead of editing the XML
- Your SVG editor stripped out the custom attributes

**Solution 1 - Use Helper Script (Easiest):**
```bash
python svg_helper.py your_design.svg
```
Follow the prompts to add attributes to each shape.

**Solution 2 - Manual Edit:**
1. Open your SVG in a text editor
2. Find each `<rect>` or shape you want as a piece
3. Add these attributes:
   ```xml
   data-piece-type="A"
   data-piece-id="0"
   ```

**Example Fix:**
```xml
<!-- Before (from Illustrator) -->
<rect x="0.5" y="0" width="1" height="2"/>

<!-- After (add attributes) -->
<rect x="0.5" y="0" width="1" height="2"
      data-piece-type="A"
      data-piece-id="0"/>
```

### "Could not load template"

- Check that the file is valid XML
- Ensure all tags are properly closed
- Verify the SVG namespace is present: `xmlns="http://www.w3.org/2000/svg"`

### Pieces not appearing correctly

- Verify coordinates are within the viewBox
- Check that width and height are positive numbers
- Ensure piece IDs are sequential (0, 1, 2, ...)
- Check attribute spelling: `data-piece-type` (lowercase, hyphenated)

## Advanced: Multiple Piece Types

You can have as many piece types as you want:

```xml
<!-- Type A pieces (squares) -->
<rect data-piece-type="A" data-piece-id="0" .../>
<rect data-piece-type="A" data-piece-id="1" .../>

<!-- Type B pieces (rectangles) -->
<rect data-piece-type="B" data-piece-id="0" .../>
<rect data-piece-type="B" data-piece-id="1" .../>

<!-- Type C pieces (different size) -->
<rect data-piece-type="C" data-piece-id="0" .../>
```

Just make sure to configure the piece counts in the app to match your template!

## Need Help?

- Check the included `tennis_court.svg` for a working example
- Test your template by loading it in the app
- The app will tell you how many pieces of each type it found

Happy designing!
