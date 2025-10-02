# Genesis ROM Workshop - Usage Guide

Comprehensive guide for using Genesis ROM Workshop tools.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Interactive Mode](#interactive-mode)
3. [Python API Usage](#python-api-usage)
4. [Common Tasks](#common-tasks)
5. [Translation Projects](#translation-projects)
6. [Advanced Techniques](#advanced-techniques)
7. [Troubleshooting](#troubleshooting)

---

## Getting Started

### Installation

```bash
git clone https://github.com/wesellis/APP-Genesis-ROM-Workshop-Sega-Palette-Text-Asset-Extraction.git
cd APP-Genesis-ROM-Workshop-Sega-Palette-Text-Asset-Extraction
pip install -r requirements.txt
```

### Quick Start - Interactive Mode

Run the main interface:

```bash
python grw_pipeline.py
```

Or analyze a specific ROM:

```bash
python grw_pipeline.py sonic.bin
```

### Quick Start - Python API

```python
from tools.palette_editor import PaletteEditor

editor = PaletteEditor()
palettes = editor.extract_palettes("sonic.bin")
print(f"Found {len(palettes)} palettes")
```

---

## Interactive Mode

The interactive mode provides a user-friendly menu interface.

### Menu Options

1. **Palette Editor** - Extract and modify color palettes
2. **Text Editor** - Extract and translate text strings
3. **Asset Extractor** - Extract graphics and audio
4. **ROM Analyzer** - Analyze ROM structure and headers

### Example Session

```
$ python grw_pipeline.py

🎨 Genesis ROM Workshop v1.0
Professional tools for real ROM modification
==================================================

Available tools:
1. Palette Editor - Recolor any Genesis game
2. Text Editor - Extract/replace text for translations
3. Asset Extractor - Extract graphics and audio
4. ROM Analyzer - Analyze ROM structure
5. Exit

Select tool (1-5): 1

🎨 Palette Editor
--------------------
Enter ROM path: sonic.bin
Loading ROM...
✅ Found 47 palettes
```

---

## Python API Usage

### Example 1: Extract Palettes

```python
from tools.palette_editor import PaletteEditor

editor = PaletteEditor()
palettes = editor.extract_palettes("sonic.bin", max_scan=10)

# Display first palette
for i, (r, g, b) in enumerate(palettes[0]):
    print(f"Color {i}: RGB({r}, {g}, {b})")
```

### Example 2: Modify Palette (Create Red Sonic)

```python
from tools.palette_editor import PaletteEditor

editor = PaletteEditor()
palettes = editor.extract_palettes("sonic.bin")

# Modify Sonic's palette - make blue colors red
sonic_palette = palettes[0]
modified_palette = []

for r, g, b in sonic_palette:
    if b > r and b > g:  # If primarily blue
        modified_palette.append((b, g, r))  # Swap blue to red
    else:
        modified_palette.append((r, g, b))

# Apply to ROM
output_rom = editor.apply_palette_swap(
    "sonic.bin",
    palette_index=0,
    new_palette=modified_palette,
    output_path="sonic_red.bin"
)

print(f"Created: {output_rom}")
```

### Example 3: Extract Text for Translation

```python
from tools.text_extractor import TextExtractor

extractor = TextExtractor()

# Extract all text strings
result = extractor.extract_for_translation(
    "game.bin",
    output_path="translation.json"
)

print(f"Extracted {result['strings_found']} strings")
print(f"Saved to: {result['output_file']}")

# Edit translation.json, then apply:
result = extractor.apply_translation_file(
    "game.bin",
    "translation.json",
    output_path="game_translated.bin"
)

print(f"Applied {result['applied']} translations")
```

### Example 4: Hex Editing

```python
from tools.hex_editor import HexEditor

editor = HexEditor()

# View ROM header
lines = editor.view_hex("sonic.bin", offset=0x100, length=256)
for line in lines:
    print(line)

# Search for "SEGA" signature
matches = editor.search_bytes("sonic.bin", b"SEGA")
print(f"Found 'SEGA' at: {[hex(m) for m in matches]}")

# Compare two ROMs
differences = editor.compare_roms("original.bin", "modified.bin")
print(f"Found {len(differences)} differences")
```

### Example 5: ROM Analysis

```python
from tools.rom_analyzer import ROMAnalyzer

analyzer = ROMAnalyzer()

# Analyze ROM structure
info = analyzer.analyze_rom_structure("sonic.bin")
print(f"Game: {info.name}")
print(f"Region: {info.region}")
print(f"Size: {info.size:,} bytes")
print(f"Valid Genesis header: {info.header_valid}")

# Get statistics
stats = analyzer.get_rom_statistics("sonic.bin")
print(f"Entropy: {stats['entropy']:.2f}")
print(f"Unique bytes: {stats['unique_bytes']}")

# Validate checksum
result = analyzer.validate_checksum("sonic.bin")
if result['valid']:
    print("✅ Checksum valid")
else:
    print(f"❌ Checksum mismatch")
```

---

## Common Tasks

### Task 1: Recolor a Game

**Goal:** Change the color scheme of a Genesis game.

```python
from tools.palette_editor import PaletteEditor

editor = PaletteEditor()

# 1. Extract palettes
palettes = editor.extract_palettes("game.bin")

# 2. Export palette to JSON for easy editing
editor.export_palette_to_json(palettes[0], "palette.json")

# 3. Edit palette.json in a text editor
#    Modify RGB values as desired

# 4. Import and apply
new_palette = editor.import_palette_from_json("palette.json")
editor.apply_palette_swap(
    "game.bin",
    palette_index=0,
    new_palette=new_palette,
    output_path="game_recolored.bin"
)

# 5. Test in emulator
print("✅ Load game_recolored.bin in your emulator!")
```

### Task 2: Create a Negative Color Effect

```python
from tools.palette_editor import PaletteEditor

editor = PaletteEditor()
palettes = editor.extract_palettes("game.bin")

# Invert all colors
for pal_idx, palette in enumerate(palettes[:5]):  # First 5 palettes
    inverted = [(255-r, 255-g, 255-b) for r, g, b in palette]
    editor.apply_palette_swap(
        "game.bin",
        palette_index=pal_idx,
        new_palette=inverted,
        output_path=f"game_negative_pal{pal_idx}.bin" if pal_idx == 0 else None
    )
```

### Task 3: Extract All Dialogue

```python
from tools.text_extractor import TextExtractor

extractor = TextExtractor()

# Find all text strings longer than 10 characters (likely dialogue)
strings = extractor.find_text_strings("rpg_game.bin", min_length=10)

# Filter and save dialogue only
dialogue = [s for s in strings if len(s['text']) > 15]

print(f"Found {len(dialogue)} dialogue strings")
for d in dialogue[:10]:
    print(f"[{d['offset']:08X}] {d['text']}")
```

### Task 4: Find and Replace Text

```python
from tools.text_extractor import TextExtractor

extractor = TextExtractor()

# Find all strings
strings = extractor.find_text_strings("game.bin")

# Find specific text
target = "GAME OVER"
for s in strings:
    if target in s['text']:
        print(f"Found '{target}' at offset 0x{s['offset']:X}")

        # Replace it
        extractor.replace_text_string(
            "game.bin",
            offset=s['offset'],
            old_text=target,
            new_text="TRY AGAIN",  # Same length or shorter
            output_path="game_modified.bin"
        )
        break
```

### Task 5: Compare Original vs Modified ROM

```python
from tools.hex_editor import HexEditor

editor = HexEditor()

# Compare ROMs
diffs = editor.compare_roms("original.bin", "modified.bin")

# Show changes
print(f"Total changes: {len(diffs)}\n")
for i, diff in enumerate(diffs[:20], 1):
    offset = diff['offset']
    old = diff['rom1_byte']
    new = diff['rom2_byte']
    print(f"{i}. 0x{offset:08X}: {old} → {new}")

# Create patch file
patch_file = editor.create_patch(
    "original.bin",
    "modified.bin",
    "changes.patch.json"
)
print(f"\nPatch file created: {patch_file}")
```

---

## Translation Projects

### Complete Translation Workflow

#### Step 1: Extract Text

```python
from tools.text_extractor import TextExtractor

extractor = TextExtractor()
result = extractor.extract_for_translation(
    "japanese_game.bin",
    output_path="japanese_to_english.json"
)

print(f"Extracted {result['strings_found']} strings to translate")
```

This creates a JSON file like:

```json
{
  "rom_file": "japanese_game.bin",
  "total_strings": 150,
  "strings": [
    {
      "id": 0,
      "original": "HELLO WORLD",
      "translation": "",
      "offset": "0x12000",
      "length": 11,
      "encoding": "ascii"
    }
  ]
}
```

#### Step 2: Translate

Edit `japanese_to_english.json` and fill in translations:

```json
{
  "id": 0,
  "original": "HELLO WORLD",
  "translation": "BONJOUR",
  "offset": "0x12000",
  "length": 11,
  "encoding": "ascii"
}
```

**Important:** Translation must be ≤ original length!

#### Step 3: Apply Translations

```python
result = extractor.apply_translation_file(
    "japanese_game.bin",
    "japanese_to_english.json",
    output_path="game_english.bin"
)

print(f"Applied: {result['applied']}")
print(f"Skipped: {result['skipped']} (too long or empty)")
print(f"Total: {result['total']}")
```

#### Step 4: Verify

```python
from tools.hex_editor import HexEditor

editor = HexEditor()

# Check the first translation location
lines = editor.view_hex("game_english.bin", offset=0x12000, length=64)
for line in lines:
    print(line)
```

---

## Advanced Techniques

### Batch Process Multiple Palettes

```python
from tools.palette_editor import PaletteEditor

editor = PaletteEditor()
palettes = editor.extract_palettes("game.bin")

# Apply same modification to all palettes
for i, palette in enumerate(palettes):
    # Increase brightness by 20%
    brightened = [
        (min(255, int(r*1.2)), min(255, int(g*1.2)), min(255, int(b*1.2)))
        for r, g, b in palette
    ]

    editor.apply_palette_swap(
        "game.bin",
        palette_index=i,
        new_palette=brightened,
        output_path="game_bright.bin" if i == 0 else None
    )

print(f"Brightened {len(palettes)} palettes")
```

### Create Grayscale Version

```python
from tools.palette_editor import PaletteEditor

def rgb_to_gray(r, g, b):
    """Convert RGB to grayscale using standard luminance formula."""
    gray = int(0.299 * r + 0.587 * g + 0.114 * b)
    return (gray, gray, gray)

editor = PaletteEditor()
palettes = editor.extract_palettes("sonic.bin")

# Convert all palettes to grayscale
for i, palette in enumerate(palettes):
    gray_palette = [rgb_to_gray(r, g, b) for r, g, b in palette]

    editor.apply_palette_swap(
        "sonic.bin",
        palette_index=i,
        new_palette=gray_palette,
        output_path="sonic_gray.bin" if i == 0 else None
    )
```

### Search and Replace Multiple Strings

```python
from tools.text_extractor import TextExtractor

translations = {
    "START": "BEGIN",
    "OPTIONS": "CONFIG",
    "EXIT": "QUIT"
}

extractor = TextExtractor()
strings = extractor.find_text_strings("game.bin")

rom_path = "game.bin"
for old_text, new_text in translations.items():
    for s in strings:
        if s['text'] == old_text:
            extractor.replace_text_string(
                rom_path,
                s['offset'],
                old_text,
                new_text,
                output_path=rom_path  # Overwrite
            )
            print(f"Replaced '{old_text}' → '{new_text}'")
            rom_path = rom_path  # Use modified ROM for next iteration
```

---

## Troubleshooting

### Problem: "No palettes found"

**Cause:** ROM might use non-standard palette locations.

**Solution:**
```python
# Try full ROM scan (slower)
palettes = editor.extract_palettes("game.bin", max_scan=None)
```

### Problem: "Text too long for replacement"

**Cause:** New text exceeds original string length.

**Solution:** Use abbreviations or shorter translations:
```python
# Instead of "CONFIGURATION" use "CONFIG"
# Instead of "CONTINUE GAME" use "CONTINUE"
```

### Problem: "Invalid checksum after modification"

**Cause:** Some games verify checksums.

**Solution:** Recalculate checksum or patch checksum verification.
```python
# Future feature: auto-update checksums
```

### Problem: "Emulator crashes with modified ROM"

**Causes:**
1. Critical code was modified
2. ROM size changed
3. Header corruption

**Solutions:**
- Only modify palette/text data
- Never change ROM size
- Verify header at 0x100

### Problem: "Colors look wrong"

**Cause:** Genesis uses 9-bit color (3-bit per channel).

**Solution:** Colors are less precise than modern RGB:
- RGB(255, 0, 0) becomes RGB(255, 0, 0) ✓
- RGB(200, 0, 0) becomes RGB(182, 0, 0) (rounded)

---

## Tips and Best Practices

### 1. Always Backup Original ROMs

```bash
cp original.bin original.bin.backup
```

### 2. Test Changes in Emulator

After each modification, test in Genesis emulator:
- Kega Fusion
- Genesis Plus GX
- BlastEm

### 3. Use Version Control

```bash
git init
git add .
git commit -m "Initial ROM state"
# Make changes
git commit -m "Applied red Sonic palette"
```

### 4. Document Your Changes

Create a changelog:
```
CHANGES.md
==========
- Palette 0: Changed Sonic blue to red
- Offset 0x12000: "START" → "BEGIN"
- Palette 3: Brightened by 20%
```

### 5. Validate Before Distribution

```python
from tools.rom_analyzer import ROMAnalyzer

analyzer = ROMAnalyzer()
info = analyzer.analyze_rom_structure("modified.bin")

if info.header_valid:
    print("✅ Header valid")
else:
    print("❌ Header corrupted - do not distribute!")
```

---

## Legal and Ethical Considerations

⚠️ **IMPORTANT:**

1. **Only use legally obtained ROMs** - You must own the original game
2. **Don't distribute copyrighted ROMs** - Share patches, not ROMs
3. **Respect original creators** - Give credit where due
4. **Educational purposes** - Learn and preserve, don't pirate

### Sharing Your Work

Share patches instead of modified ROMs:

```python
from tools.hex_editor import HexEditor

editor = HexEditor()
patch_file = editor.create_patch(
    "original.bin",
    "modified.bin",
    "my_translation.patch.json"
)

# Distribute only the patch file!
```

---

## Getting Help

- **Documentation:** `README.md`, `API_REFERENCE.md`
- **Examples:** `examples/` directory
- **Issues:** GitHub Issues
- **Genesis Documentation:** sega-16.com, plutiedev.com

---

## Next Steps

1. Try the examples in `examples/` directory
2. Read the `API_REFERENCE.md` for detailed API docs
3. Experiment with your favorite Genesis games
4. Join the ROM hacking community!

Happy ROM hacking! 🎮
