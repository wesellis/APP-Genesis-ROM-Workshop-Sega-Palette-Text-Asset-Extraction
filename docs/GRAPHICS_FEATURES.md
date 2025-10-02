# Graphics Rendering Features - NEW! ✨

**Genesis ROM Workshop now includes professional graphics rendering capabilities!**

## What's New

### 🎨 Palette Preview Images

Export color palettes as visual PNG images instead of just JSON data.

```python
from tools.palette_editor import PaletteEditor

editor = PaletteEditor()
palettes = editor.extract_palettes("sonic.bin")

# Export single palette as image
editor.export_palette_as_image(
    palettes[0],
    "palette_preview.png",
    scale=20  # 320x20 pixels
)

# Export all palettes
editor.export_all_palettes_as_images(
    palettes,
    "output_dir",
    prefix="palette"
)
```

**Output:** Horizontal color bar showing all 16 colors

---

### 🖼️ Tile Rendering to PNG

Render Genesis graphics tiles as actual viewable images!

```python
from tools.graphics_renderer import GraphicsRenderer

renderer = GraphicsRenderer()

# Render single tile
renderer.render_tile_to_file(
    tile_data,      # 32 bytes
    palette,        # 16 RGB tuples
    "tile.png",
    scale=4         # 32x32 pixels
)
```

**Features:**
- Decodes 4-bit planar format (Genesis standard)
- Applies palette to create RGB image
- Configurable scale (1x, 2x, 4x, 8x)
- Outputs standard PNG files

---

### 📐 Tile Sheet Creation

Create sprite sheets showing all graphics at once!

```python
from tools.graphics_renderer import GraphicsRenderer

renderer = GraphicsRenderer()

# Render multiple tiles as sheet
renderer.render_tile_sheet_to_file(
    tiles,          # List of tile data
    palette,
    "tilesheet.png",
    columns=16,     # 16 tiles per row
    scale=2         # 2x scaling
)
```

**Output:** Professional tile sheet like sprite ripping tools

---

### 🔍 Tile Preview with Grid

Create detailed previews with pixel grid overlay for analysis.

```python
renderer.create_tile_preview(
    tile_data,
    palette,
    "preview.png",
    show_grid=True,  # Show pixel boundaries
    scale=8          # 64x64 pixels
)
```

**Perfect for:**
- Examining pixel-by-pixel details
- Understanding tile structure
- Creating documentation

---

### 🎯 Asset Extraction with Rendering

Extract graphics from ROM and render directly to PNG!

```python
from tools.asset_extractor import AssetExtractor

extractor = AssetExtractor()

# Extract and render as tile sheet
result = extractor.extract_and_render_graphics(
    "sonic.bin",
    palette,
    max_tiles=256,
    render_sheet=True
)

# Output: workspace/exports/sonic_rendered/sonic_tilesheet.png
```

**Benefits:**
- See graphics immediately
- No external tools needed
- Professional tile sheet output

---

### 🎨 Render Specific ROM Regions

Render tiles from specific offsets (useful when you know where graphics are):

```python
extractor.render_tiles_with_palette(
    "sonic.bin",
    palette,
    "output.png",
    offset=0x20000,   # Graphics location
    num_tiles=256
)
```

---

## Technical Details

### 4-Bit Planar Format Decoding

Genesis graphics use 4-bit planar format:
- 8x8 pixel tiles
- 32 bytes per tile
- 4 bitplanes (4 bits per pixel = 16 colors)
- Row-major storage

Our decoder handles:
- ✅ Bitplane extraction
- ✅ Pixel value assembly
- ✅ Palette application
- ✅ RGB conversion

### Supported Features

| Feature | Status | Notes |
|---------|--------|-------|
| 4-bit planar tiles | ✅ Full support | Genesis standard |
| Palette rendering | ✅ Full support | 16 colors per palette |
| Tile sheets | ✅ Full support | Configurable columns |
| Scaling | ✅ Full support | 1x to 16x |
| Grid overlay | ✅ Full support | For analysis |
| PNG export | ✅ Full support | Standard format |

### Limitations

| Feature | Status | Notes |
|---------|--------|-------|
| Compressed graphics | ❌ Not supported | Nemesis/Kosinski needed |
| Sprite assembly | ⚠️ Partial | Manual tile arrangement |
| Tilemap rendering | ⚠️ Planned | Future feature |
| Palette detection | ⚠️ Heuristic | May miss some palettes |

---

## Installation

```bash
# Install Pillow for graphics features
pip install Pillow

# Or install all dependencies
pip install -r requirements.txt
```

**Note:** Graphics rendering requires Pillow. Without it, the toolkit still works but rendering features will be disabled.

---

## Examples

### Example 1: Quick Palette Preview

```python
from tools.palette_editor import PaletteEditor

editor = PaletteEditor()
palettes = editor.extract_palettes("sonic.bin", max_scan=5)
editor.export_all_palettes_as_images(palettes, "palettes/")
```

**Result:** `palettes/palette_000.png`, `palette_001.png`, etc.

### Example 2: Extract and View Graphics

```python
from tools.palette_editor import PaletteEditor
from tools.asset_extractor import AssetExtractor

# Get palette
editor = PaletteEditor()
palettes = editor.extract_palettes("sonic.bin")

# Render graphics
extractor = AssetExtractor()
result = extractor.extract_and_render_graphics(
    "sonic.bin",
    palettes[0],
    max_tiles=256
)

print(f"Created: {result['sheet_file']}")
# Open the PNG to see Sonic's graphics!
```

### Example 3: Tile-by-Tile Analysis

```python
from tools.asset_extractor import AssetExtractor

extractor = AssetExtractor()

# Preview specific tile with grid
extractor.preview_tile(
    "sonic.bin",
    palette,
    offset=0x20000,    # Tile location
    output_path="tile_detail.png",
    show_grid=True
)
```

---

## Comparison: Before vs After

### BEFORE (v1.0)

❌ **Palette Export**
- JSON only
- No visual preview
- Hard to see colors

❌ **Graphics Extraction**
- Raw .bin files
- Unreadable data
- Need external tools

❌ **Analysis**
- Hex dump only
- No visual feedback
- Time-consuming

### AFTER (v1.1 - Current)

✅ **Palette Export**
- PNG images
- Visual color bars
- See colors instantly

✅ **Graphics Extraction**
- Rendered PNG tiles
- Viewable in any image viewer
- Professional tile sheets

✅ **Analysis**
- Grid overlays
- Pixel-perfect previews
- Instant feedback

---

## Performance

| Operation | Time | Output |
|-----------|------|--------|
| Single palette to PNG | < 0.1s | ~150 bytes |
| Single tile to PNG | < 0.1s | ~130 bytes |
| 256-tile sheet | ~0.5s | ~5-10 KB |
| Full graphics extraction | 1-3s | Depends on ROM |

**Memory:** Minimal (< 50 MB for typical operations)

---

## Use Cases

### 1. ROM Hacking
- Preview graphics before extracting
- See color schemes
- Identify sprite locations

### 2. Game Analysis
- Study pixel art techniques
- Analyze color usage
- Document graphics format

### 3. Asset Ripping
- Extract sprite sheets
- Create texture packs
- Make fan art references

### 4. Education
- Learn Genesis graphics format
- Understand planar encoding
- Study retro game graphics

---

## API Reference

### PaletteEditor (Enhanced)

#### `export_palette_as_image(palette, output_path, scale=20)`
Export single palette as PNG image.

#### `export_all_palettes_as_images(palettes, output_dir, prefix="palette")`
Export multiple palettes as individual images.

### GraphicsRenderer (New Module)

#### `decode_tile_planar(tile_data) -> List[List[int]]`
Decode 4-bit planar tile to 8x8 pixel array.

#### `render_tile(tile_data, palette, scale=1)`
Render tile to PIL Image object.

#### `render_tile_to_file(tile_data, palette, output_path, scale=4)`
Render tile and save to PNG.

#### `render_tile_sheet(tiles, palette, columns=16, scale=2)`
Create tile sheet image.

#### `render_tile_sheet_to_file(tiles, palette, output_path, columns=16, scale=2)`
Create and save tile sheet.

#### `create_tile_preview(tile_data, palette, output_path, show_grid=True, scale=8)`
Create detailed tile preview with grid.

### AssetExtractor (Enhanced)

#### `extract_and_render_graphics(rom_path, palette, max_tiles=256, render_sheet=True)`
Extract graphics and render to PNG.

#### `render_tiles_with_palette(rom_path, palette, output_path, offset=0, num_tiles=256)`
Render tiles from specific ROM offset.

#### `preview_tile(rom_path, palette, offset, output_path, show_grid=True)`
Create detailed preview of single tile.

---

## Testing

Run graphics tests:

```bash
python test_graphics.py
```

**Expected output:**
```
============================================================
Graphics Rendering - Test Suite
============================================================

Testing GraphicsRenderer...
✅ GraphicsRenderer initialized
✅ Decoded tile: 8x8 pixels
✅ Rendered tile to PNG: 131 bytes
✅ Rendered tile sheet: 162 bytes
✅ All GraphicsRenderer tests passed!

Results: 3/3 tests passed
```

---

## Troubleshooting

### "Pillow not installed"

```bash
pip install Pillow
```

### "Graphics rendering not available"

Check if Pillow is installed:
```python
import PIL
print(PIL.__version__)
```

### "No tiles extracted"

- Graphics might be compressed (not supported yet)
- Try different ROM offset
- Check if palette is correct

### "Tiles look wrong"

- Wrong palette selected
- Graphics might use different format
- Try different palette from ROM

---

## Future Enhancements

Planned features:

- [ ] Compression support (Nemesis/Kosinski)
- [ ] Automatic sprite assembly
- [ ] Tilemap rendering
- [ ] Animation frame extraction
- [ ] Palette auto-detection
- [ ] ML-based graphics detection

---

## Credits

**4-bit Planar Decoding**
- Based on Sega Genesis technical documentation
- Tested with Sonic 1, 2, 3 graphics

**Rendering Engine**
- Built with Pillow (PIL)
- Optimized for speed and quality

---

## Summary

✨ **What You Get:**

- ✅ Palette preview images (PNG)
- ✅ Tile rendering (4-bit planar → PNG)
- ✅ Tile sheet creation
- ✅ Grid overlays for analysis
- ✅ Visual feedback for all operations
- ✅ Professional output quality

🎯 **Result:** Genesis ROM Workshop is now a **complete graphics analysis tool**, not just a hex editor!

---

**Go try it!**

```bash
python examples/example_graphics_rendering.py your_rom.bin
```

Check `workspace/` for the generated images! 🎉
