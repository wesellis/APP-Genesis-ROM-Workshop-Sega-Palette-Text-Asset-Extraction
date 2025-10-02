# Genesis ROM Workshop - Examples

Practical examples demonstrating how to use each tool in the Genesis ROM Workshop.

## Getting Started

All examples can be run from the command line:

```bash
python examples/example_palette_extraction.py path/to/rom.bin
```

## Available Examples

### 1. Palette Extraction (`example_palette_extraction.py`)

Demonstrates palette extraction, modification, and color swapping.

**Features:**
- Extract all palettes from a ROM
- Display RGB color values
- Export palettes to JSON for editing
- Import modified palettes
- Create color variations (e.g., "red Sonic")

**Usage:**
```bash
python examples/example_palette_extraction.py sonic.bin
```

**What it does:**
1. Extracts palettes and displays first 3
2. Exports first palette to `workspace/palette_0.json`
3. Creates a "red Sonic" ROM by swapping blue colors to red

**Output:**
- `workspace/palette_0.json` - Editable palette file
- `workspace/sonic_red.bin` - Modified ROM with red Sonic

---

### 2. Text Extraction (`example_text_extraction.py`)

Shows how to extract, translate, and modify text in ROMs.

**Features:**
- Find all text strings in a ROM
- Create translation files
- Replace individual strings
- Apply bulk translations

**Usage:**
```bash
python examples/example_text_extraction.py game.bin
```

**What it does:**
1. Extracts and displays first 20 text strings
2. Creates `workspace/translation.json` for manual editing
3. Replaces first string with uppercase version

**Workflow:**
1. Run script to extract text
2. Edit `workspace/translation.json`
3. Run `apply_translation_file()` to create translated ROM

---

### 3. Hex Editing (`example_hex_editing.py`)

Demonstrates low-level ROM manipulation.

**Features:**
- View ROM data in hex format
- Search for byte patterns
- Compare two ROMs
- Write custom bytes

**Usage:**
```bash
python examples/example_hex_editing.py game.bin
```

**What it does:**
1. Displays hex dump of ROM header (offset 0x100)
2. Searches for "SEGA" signature
3. Writes custom bytes to ROM

**Common patterns to search:**
- `53 45 47 41` - "SEGA" signature
- `00 FF 00 FF` - Empty/padding data
- `FF FF FF FF` - Uninitialized data

---

## Quick Reference

### Extract Palettes
```python
from tools.palette_editor import PaletteEditor

editor = PaletteEditor()
palettes = editor.extract_palettes("rom.bin")
```

### Extract Text
```python
from tools.text_extractor import TextExtractor

extractor = TextExtractor()
strings = extractor.find_text_strings("rom.bin", min_length=4)
```

### View Hex Data
```python
from tools.hex_editor import HexEditor

editor = HexEditor()
lines = editor.view_hex("rom.bin", offset=0x100, length=256)
for line in lines:
    print(line)
```

### Analyze ROM
```python
from tools.rom_analyzer import ROMAnalyzer

analyzer = ROMAnalyzer()
info = analyzer.analyze_rom_structure("rom.bin")
print(f"Game: {info.name}")
print(f"Region: {info.region}")
```

---

## Common Workflows

### Workflow 1: Change Game Colors

1. Extract palette:
   ```python
   palettes = editor.extract_palettes("game.bin")
   ```

2. Export to JSON:
   ```python
   editor.export_palette_to_json(palettes[0], "palette.json")
   ```

3. Edit `palette.json` in text editor

4. Import and apply:
   ```python
   new_pal = editor.import_palette_from_json("palette.json")
   editor.apply_palette_swap("game.bin", 0, new_pal, "game_mod.bin")
   ```

5. Test in emulator!

### Workflow 2: Translate Game Text

1. Extract for translation:
   ```python
   extractor.extract_for_translation("game.bin", "trans.json")
   ```

2. Edit `trans.json` and fill in translations

3. Apply translations:
   ```python
   extractor.apply_translation_file("game.bin", "trans.json", "game_en.bin")
   ```

4. Test in emulator!

### Workflow 3: Compare ROM Versions

```python
editor = HexEditor()
diffs = editor.compare_roms("version1.bin", "version2.bin")

# Create patch file
patch = editor.create_patch("version1.bin", "version2.bin", "changes.patch.json")
```

---

## Tips

1. **Always backup original ROMs** before modifying
2. **Test in emulator** after each change
3. **Start small** - modify one palette/string at a time
4. **Check file sizes** - ensure modifications don't exceed ROM size
5. **Validate headers** - use ROMAnalyzer to verify ROM integrity

---

## Example Projects

### Project 1: Grayscale ROM

Convert all colors to grayscale:

```python
def rgb_to_gray(r, g, b):
    gray = int(0.299 * r + 0.587 * g + 0.114 * b)
    return (gray, gray, gray)

editor = PaletteEditor()
palettes = editor.extract_palettes("sonic.bin")

for i, pal in enumerate(palettes):
    gray_pal = [rgb_to_gray(r, g, b) for r, g, b in pal]
    editor.apply_palette_swap(
        "sonic.bin", i, gray_pal,
        "sonic_gray.bin" if i == 0 else None
    )
```

### Project 2: Find All Dialogue

```python
extractor = TextExtractor()
strings = extractor.find_text_strings("rpg.bin", min_length=10)

dialogue = [s for s in strings if len(s['text']) > 20]
print(f"Found {len(dialogue)} dialogue lines:")

for d in dialogue:
    print(f"[{d['offset']:08X}] {d['text']}")
```

### Project 3: Palette Brightness Adjuster

```python
def adjust_brightness(palette, factor):
    """Increase/decrease brightness by factor (e.g., 1.2 = 20% brighter)"""
    return [
        (min(255, int(r*factor)), min(255, int(g*factor)), min(255, int(b*factor)))
        for r, g, b in palette
    ]

bright_pal = adjust_brightness(palettes[0], 1.3)  # 30% brighter
```

---

## Troubleshooting

**Q: "No palettes found"**
A: Try full ROM scan: `extract_palettes(rom, max_scan=None)`

**Q: "Text replacement too long"**
A: New text must be ≤ original length. Use abbreviations.

**Q: "Emulator crashes"**
A: Verify ROM header is intact. Don't modify code sections.

**Q: "Colors look weird"**
A: Genesis uses 9-bit color (3-bit/channel). Some precision is lost.

---

## Next Steps

1. Try modifying your favorite Genesis game
2. Read the full documentation: `../USAGE_GUIDE.md`
3. Check API reference: `../API_REFERENCE.md`
4. Join the ROM hacking community!

---

## Legal Note

⚠️ Only use ROMs you legally own. Do not distribute copyrighted materials.

For more examples and documentation, see the main README.md.
