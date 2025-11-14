# Visual Tennis Court Demo

This document describes the visual output of the Stained Glass Cutlist Generator.

## Color Palette

The app uses 10 shades of blue by default (from light to dark):

```
Blue 1   #add8e6  ░░░░░░  (Light Blue)
Blue 2   #99c0db  ▒▒▒▒▒▒
Blue 3   #86a8d1  ▒▒▒▒▒▒
Blue 4   #7390c7  ▓▓▓▓▓▓
Blue 5   #6078bd  ▓▓▓▓▓▓
Blue 6   #4c60b3  ▓▓▓▓▓▓
Blue 7   #3948a9  ▓▓▓▓▓▓
Blue 8   #26309f  ████████
Blue 9   #131895  ████████
Blue 10  #00008b  ████████  (Dark Blue)
```

## Tennis Court Layout

Each finished piece shows a top-down view of a tennis court:

```
┌───────┬────────┬────────┬───────┐
│       │        │        │       │
│   B   │   A    │   A    │   B   │
│ (0.5" │ (1x2") │ (1x2") │ (0.5" │
│  x4") │        │        │  x4") │
│       ├────────┼────────┤       │
│       │   A    │   A    │       │
│       │ (1x2") │ (1x2") │       │
└───────┴────────┴────────┴───────┘
   ↑        ↑  ↑      ↑  ↑      ↑
  Left     Center    Center   Right
  Lane    Service   Service   Lane
          Box       Box
```

**Dimensions:**
- Total Width: 3.0 inches (0.5 + 1.0 + 1.0 + 0.5)
- Total Height: 4.0 inches
- Left B: 0.5" × 4" (side lane)
- Right B: 0.5" × 4" (side lane)
- 4× A pieces: 1" × 2" each (service boxes in 2×2 grid)

## Sample Visual Output

### Example: Piece #1

```
┌───────┬────────┬────────┬───────┐
│       │        │        │       │
│   B   │   A    │   A    │   B   │
│ Blue8 │ Blue10 │ Blue3  │ Blue6 │
│  ███  │  ████  │  ▓▓▓▓  │  ▓▓▓  │
│       ├────────┼────────┤       │
│       │   A    │   A    │       │
│       │ Blue2  │ Blue4  │       │
│       │  ▒▒▒▒  │  ▓▓▓▓  │       │
└───────┴────────┴────────┴───────┘
```

Colors used:
- Type A: Blue 10, Blue 3, Blue 2, Blue 4
- Type B: Blue 8, Blue 6

Note: No color repeats! All 6 pieces use different blues.

### Example: Piece #2

```
┌───────┬────────┬────────┬───────┐
│       │        │        │       │
│   B   │   A    │   A    │   B   │
│ Blue7 │ Blue10 │ Blue1  │ Blue8 │
│  ▓▓▓  │  ████  │  ░░░░  │  ███  │
│       ├────────┼────────┤       │
│       │   A    │   A    │       │
│       │ Blue6  │ Blue2  │       │
│       │  ▓▓▓▓  │  ▒▒▒▒  │       │
└───────┴────────┴────────┴───────┘
```

Colors used:
- Type A: Blue 10, Blue 1, Blue 6, Blue 2
- Type B: Blue 7, Blue 8

## GUI Layout

The application window is divided into three sections:

```
┌─────────────────────────────────────────────────────┐
│         Stained Glass Cutlist Generator             │
├─────────────────────────────────────────────────────┤
│  Project Parameters                                 │
│  ┌───────────────────────────────────────────────┐  │
│  │ Number of piece types: [2]  [Set Piece Types]│  │
│  │ Type  Count  Width  Height                    │  │
│  │  A      4     1.0    2.0                      │  │
│  │  B      2     0.5    4.0                      │  │
│  │ Number of colors: [10]                        │  │
│  │ Number of finished pieces: [10]               │  │
│  │        [Generate Cutlist]                     │  │
│  └───────────────────────────────────────────────┘  │
├──────────────────────┬──────────────────────────────┤
│  Visual Templates    │  Cutlist Data                │
│ ┌──────────────────┐ │ ┌──────────────────────────┐ │
│ │ Color Palette:   │ │ │ ======================= │ │
│ │ ■ Blue 1         │ │ │ STAINED GLASS CUTLIST  │ │
│ │ ■ Blue 2         │ │ │ ======================= │ │
│ │ ...              │ │ │                         │ │
│ │                  │ │ │ PROJECT SUMMARY:        │ │
│ │ Piece #1:        │ │ │ Pieces per item: 6      │ │
│ │ ┌───┬───┬───┐    │ │ │ Colors available: 10    │ │
│ │ │ B │ A │ B │    │ │ │                         │ │
│ │ │   ├─┬─┤   │    │ │ │ CUTLIST:                │ │
│ │ │   │A│A│   │    │ │ │ Color    A    B  Total  │ │
│ │ └───┴─┴─┴───┘    │ │ │ Blue 1   4    1    5    │ │
│ │                  │ │ │ Blue 2   5    0    5    │ │
│ │ Piece #2:        │ │ │ ...                     │ │
│ │ ┌───┬───┬───┐    │ │ │                         │ │
│ │ │ B │ A │ B │    │ │ │ TEMPLATES:              │ │
│ │ │   ├─┬─┤   │    │ │ │ Piece #1:               │ │
│ │ │   │A│A│   │    │ │ │  A: [Blue10, Blue3, ... │ │
│ │ └───┴─┴─┴───┘    │ │ │  B: [Blue8, Blue6]      │ │
│ └──────────────────┘ │ └──────────────────────────┘ │
└──────────────────────┴──────────────────────────────┘
```

## Features

1. **Color Legend**: Shows all available blue shades at the top
2. **Multiple Templates**: Displays up to 9 tennis courts in a 3×3 grid
3. **Scrollable**: Can scroll to see more templates
4. **Color-coded**: Each piece is filled with its assigned blue shade
5. **Labels**: Pieces are labeled with 'A' or 'B' for easy identification

## Running the Application

```bash
python cutlist_app.py
```

The visual display will show:
- Color palette legend
- Visual tennis court diagrams with actual colors
- Scrollable template gallery
- Detailed cutlist data on the right
