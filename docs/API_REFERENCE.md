# Genesis ROM Workshop - API Reference

Complete API documentation for all Genesis ROM Workshop modules.

## Table of Contents

- [PaletteEditor](#paletteeditor)
- [TextExtractor](#textextractor)
- [HexEditor](#hexeditor)
- [ROMAnalyzer](#romanalyzer)
- [AssetExtractor](#assetextractor)
- [AssetManager](#assetmanager)

---

## PaletteEditor

Extract, modify, and manage color palettes from Genesis ROMs.

### Class: `PaletteEditor`

```python
from tools.palette_editor import PaletteEditor
```

#### Constants

- `PALETTE_SIZE = 32` - Size of a Genesis palette in bytes
- `COLORS_PER_PALETTE = 16` - Number of colors per palette

#### Methods

##### `__init__()`

Initialize the palette editor.

```python
editor = PaletteEditor()
```

##### `extract_palettes(rom_path, max_scan=None)`

Extract all color palettes from a Genesis ROM.

**Parameters:**
- `rom_path` (str): Path to the ROM file
- `max_scan` (int, optional): Maximum number of palettes to find during scan

**Returns:**
- `List[List[Tuple[int, int, int]]]`: List of palettes, each containing 16 RGB tuples

**Raises:**
- `FileNotFoundError`: ROM file not found
- `IOError`: Failed to read ROM
- `ValueError`: ROM too small

**Example:**
```python
editor = PaletteEditor()
palettes = editor.extract_palettes("sonic.bin", max_scan=10)
print(f"Found {len(palettes)} palettes")
```

##### `apply_palette_swap(rom_path, palette_index, new_palette, output_path=None)`

Apply a new palette to the ROM.

**Parameters:**
- `rom_path` (str): Path to ROM file
- `palette_index` (int): Index of palette to replace (0-based)
- `new_palette` (List[Tuple[int,int,int]]): 16 RGB tuples (0-255 each)
- `output_path` (str, optional): Output ROM path (default: adds "_modified")

**Returns:**
- `str`: Path to modified ROM file

**Raises:**
- `FileNotFoundError`: ROM file not found
- `ValueError`: Invalid palette size or RGB values
- `ValueError`: Palette index not found

**Example:**
```python
# Make first color red
modified_pal = palettes[0].copy()
modified_pal[0] = (255, 0, 0)

output = editor.apply_palette_swap("sonic.bin", 0, modified_pal)
print(f"Modified ROM saved to: {output}")
```

##### `export_palette_to_json(palette, output_path)`

Export palette as JSON for manual editing.

**Parameters:**
- `palette` (List[Tuple[int,int,int]]): Palette to export
- `output_path` (str): Path to save JSON file

**Raises:**
- `ValueError`: Invalid palette size
- `IOError`: Failed to write file

**Example:**
```python
editor.export_palette_to_json(palettes[0], "palette.json")
```

##### `import_palette_from_json(json_path)`

Import palette from JSON file.

**Parameters:**
- `json_path` (str): Path to JSON palette file

**Returns:**
- `List[Tuple[int,int,int]]`: Imported palette (16 RGB tuples)

**Raises:**
- `FileNotFoundError`: JSON file not found
- `ValueError`: Invalid JSON format or palette size

**Example:**
```python
palette = editor.import_palette_from_json("palette.json")
```

---

## TextExtractor

Extract and modify text strings in Genesis ROMs for translation projects.

### Class: `TextExtractor`

```python
from tools.text_extractor import TextExtractor
```

#### Methods

##### `__init__()`

Initialize the text extractor.

```python
extractor = TextExtractor()
```

##### `find_text_strings(rom_path, min_length=4)`

Find all text strings in ROM.

**Parameters:**
- `rom_path` (str): Path to ROM file
- `min_length` (int): Minimum string length to detect (default: 4)

**Returns:**
- `List[Dict]`: List of dictionaries with keys:
  - `text`: The string found
  - `offset`: Byte offset in ROM
  - `length`: String length
  - `encoding`: Character encoding used

**Example:**
```python
extractor = TextExtractor()
strings = extractor.find_text_strings("game.bin", min_length=5)

for s in strings[:10]:
    print(f"0x{s['offset']:X}: {s['text']}")
```

##### `extract_for_translation(rom_path, output_path=None)`

Create a translation file with all strings.

**Parameters:**
- `rom_path` (str): Path to ROM file
- `output_path` (str, optional): Output JSON path

**Returns:**
- `Dict`: Result with keys `output_file` and `strings_found`

**Example:**
```python
result = extractor.extract_for_translation("game.bin", "translation.json")
print(f"Created {result['output_file']} with {result['strings_found']} strings")
```

##### `replace_text_string(rom_path, offset, old_text, new_text, output_path=None)`

Replace a single text string at specific offset.

**Parameters:**
- `rom_path` (str): Path to ROM file
- `offset` (int): Byte offset of string
- `old_text` (str): Original text to verify
- `new_text` (str): New text (must not be longer than original)
- `output_path` (str, optional): Output ROM path

**Returns:**
- `bool`: True if successful

**Raises:**
- `ValueError`: New text too long or old text not found at offset

**Example:**
```python
extractor.replace_text_string(
    "game.bin",
    offset=0x12000,
    old_text="HELLO",
    new_text="HOWDY",
    output_path="modified.bin"
)
```

##### `apply_translation_file(rom_path, translation_file, output_path=None)`

Apply translations from a JSON file to ROM.

**Parameters:**
- `rom_path` (str): Path to ROM file
- `translation_file` (str): Path to translation JSON
- `output_path` (str, optional): Output ROM path

**Returns:**
- `Dict`: Result with keys:
  - `output_file`: Path to translated ROM
  - `applied`: Number of translations applied
  - `skipped`: Number of translations skipped
  - `total`: Total strings in file

**Example:**
```python
result = extractor.apply_translation_file(
    "game.bin",
    "translation.json",
    "game_translated.bin"
)
print(f"Applied {result['applied']}/{result['total']} translations")
```

---

## HexEditor

View and edit ROM data at the byte level.

### Class: `HexEditor`

```python
from tools.hex_editor import HexEditor
```

#### Attributes

- `bytes_per_line = 16` - Number of bytes displayed per line

#### Methods

##### `view_hex(rom_path, offset=0, length=256)`

View ROM data in hexadecimal format.

**Parameters:**
- `rom_path` (str): Path to ROM file
- `offset` (int): Starting byte offset (default: 0)
- `length` (int): Number of bytes to display (default: 256)

**Returns:**
- `List[str]`: Formatted hex dump lines

**Example:**
```python
editor = HexEditor()
lines = editor.view_hex("game.bin", offset=0x100, length=128)
for line in lines:
    print(line)
```

##### `write_bytes(rom_path, offset, data, output_path=None)`

Write bytes to ROM at specified offset.

**Parameters:**
- `rom_path` (str): Path to ROM file
- `offset` (int): Byte offset to write at
- `data` (bytes): Data to write
- `output_path` (str, optional): Output ROM path

**Returns:**
- `bool`: True if successful

**Raises:**
- `ValueError`: Write would exceed ROM size

##### `search_bytes(rom_path, pattern)`

Search for byte pattern in ROM.

**Parameters:**
- `rom_path` (str): Path to ROM file
- `pattern` (bytes): Byte pattern to search for

**Returns:**
- `List[int]`: List of offsets where pattern was found

**Example:**
```python
# Search for "SEGA" signature
matches = editor.search_bytes("game.bin", b"SEGA")
print(f"Found at offsets: {[hex(m) for m in matches]}")
```

##### `compare_roms(rom1_path, rom2_path)`

Compare two ROMs and find differences.

**Parameters:**
- `rom1_path` (str): Path to first ROM
- `rom2_path` (str): Path to second ROM

**Returns:**
- `List[Dict]`: List of differences with keys:
  - `offset`: Byte offset
  - `rom1_byte`: Hex value from ROM 1
  - `rom2_byte`: Hex value from ROM 2

**Example:**
```python
diffs = editor.compare_roms("original.bin", "modified.bin")
print(f"Found {len(diffs)} differences")
```

##### `create_patch(original_path, modified_path, output_path=None)`

Create a patch file documenting differences.

**Parameters:**
- `original_path` (str): Path to original ROM
- `modified_path` (str): Path to modified ROM
- `output_path` (str, optional): Patch file path

**Returns:**
- `str`: Path to patch file

---

## ROMAnalyzer

Analyze ROM structure, headers, and validate checksums.

### Class: `ROMAnalyzer`

```python
from tools.rom_analyzer import ROMAnalyzer
```

#### Methods

##### `analyze_rom_structure(rom_path)`

Perform comprehensive ROM analysis.

**Parameters:**
- `rom_path` (str): Path to ROM file

**Returns:**
- `ROMInfo`: Data class with attributes:
  - `name`: Game name from header
  - `region`: Region code (USA/JAPAN/EUROPE)
  - `size`: ROM size in bytes
  - `checksum`: MD5 checksum
  - `rom_type`: File extension (.bin, .gen, etc.)
  - `header_valid`: Boolean if Genesis header found

**Example:**
```python
analyzer = ROMAnalyzer()
info = analyzer.analyze_rom_structure("sonic.bin")

print(f"Game: {info.name}")
print(f"Region: {info.region}")
print(f"Size: {info.size:,} bytes")
print(f"Valid header: {info.header_valid}")
```

##### `get_rom_statistics(rom_path)`

Get detailed statistics about ROM contents.

**Parameters:**
- `rom_path` (str): Path to ROM file

**Returns:**
- `Dict`: Statistics including:
  - `total_size`: Total ROM size
  - `null_bytes`: Count of 0x00 bytes
  - `ff_bytes`: Count of 0xFF bytes
  - `unique_bytes`: Number of unique byte values
  - `entropy`: Shannon entropy (measure of randomness)

##### `validate_checksum(rom_path)`

Validate ROM checksum.

**Parameters:**
- `rom_path` (str): Path to ROM file

**Returns:**
- `Dict`: Validation result with keys:
  - `valid`: Boolean checksum validity
  - `stored`: Checksum stored in header
  - `calculated`: Calculated checksum

**Example:**
```python
result = analyzer.validate_checksum("sonic.bin")
if result['valid']:
    print("✅ Checksum valid")
else:
    print(f"❌ Checksum mismatch: {result['stored']} vs {result['calculated']}")
```

---

## AssetExtractor

Extract graphics, tilemaps, and sprites from ROMs.

### Class: `AssetExtractor`

```python
from tools.asset_extractor import AssetExtractor
```

#### Methods

##### `extract_graphics_data(rom_path, max_tiles=1000)`

Extract graphics tile data.

**Parameters:**
- `rom_path` (str): Path to ROM file
- `max_tiles` (int): Maximum tiles to extract

**Returns:**
- `Dict`: Extraction results with keys:
  - `tiles_extracted`: Number of tiles found
  - `output_directory`: Path to output directory
  - `format`: Graphics format description

---

## AssetManager

Manage and organize extracted ROM assets.

### Class: `AssetManager`

```python
from tools.asset_manager import AssetManager
```

#### Methods

##### `extract_sprites(rom_path, max_tiles=1000)`

Extract sprite graphics.

**Parameters:**
- `rom_path` (str): Path to ROM file
- `max_tiles` (int): Maximum tiles to extract

**Returns:**
- `Dict`: Extraction results

##### `extract_audio_samples(rom_path)`

Extract audio samples and music data.

**Parameters:**
- `rom_path` (str): Path to ROM file

**Returns:**
- `Dict`: Extraction results with note about playback requirements

##### `organize_assets(rom_path)`

Create organized project structure for assets.

**Parameters:**
- `rom_path` (str): Path to ROM file

**Returns:**
- `Dict`: Project directory information

---

## Data Types

### RGB Tuple

Colors are represented as tuples of three integers (0-255):

```python
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
```

### Palette

A Genesis palette is a list of 16 RGB tuples:

```python
palette = [
    (0, 0, 0),      # Color 0 - usually transparent
    (255, 0, 0),    # Color 1 - red
    # ... 14 more colors
]
```

---

## Error Handling

All modules use consistent error handling:

```python
try:
    palettes = editor.extract_palettes("sonic.bin")
except FileNotFoundError:
    print("ROM file not found")
except ValueError as e:
    print(f"Invalid input: {e}")
except IOError as e:
    print(f"File operation failed: {e}")
```

---

## Best Practices

1. **Always validate inputs** - Check file paths exist before processing
2. **Handle errors gracefully** - Use try/except blocks
3. **Backup ROMs** - Never overwrite original files
4. **Test with emulators** - Verify changes work correctly
5. **Check file sizes** - Ensure new text/data fits in original space
6. **Use workspace directory** - Keep exports organized

---

## Complete Example Workflow

```python
from tools.palette_editor import PaletteEditor
from tools.text_extractor import TextExtractor
from tools.hex_editor import HexEditor

# Extract and modify palette
palette_editor = PaletteEditor()
palettes = palette_editor.extract_palettes("game.bin")
palettes[0][1] = (255, 0, 0)  # Make second color red
palette_editor.apply_palette_swap("game.bin", 0, palettes[0], "game_mod.bin")

# Extract and translate text
text_extractor = TextExtractor()
text_extractor.extract_for_translation("game.bin", "translation.json")
# Edit translation.json manually, then:
text_extractor.apply_translation_file("game.bin", "translation.json", "game_translated.bin")

# View changes in hex
hex_editor = HexEditor()
diffs = hex_editor.compare_roms("game.bin", "game_mod.bin")
print(f"Made {len(diffs)} changes")
```
