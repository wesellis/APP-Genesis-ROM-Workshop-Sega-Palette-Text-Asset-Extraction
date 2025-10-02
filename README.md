# Genesis ROM Workshop

A Python toolkit for analyzing and extracting assets from Sega Genesis/Mega Drive ROM files.

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Stars](https://img.shields.io/github/stars/wesellis/APP-Genesis-ROM-Workshop-Sega-Palette-Text-Asset-Extraction?style=flat-square)](https://github.com/wesellis/APP-Genesis-ROM-Workshop-Sega-Palette-Text-Asset-Extraction/stargazers)
[![Last Commit](https://img.shields.io/github/last-commit/wesellis/APP-Genesis-ROM-Workshop-Sega-Palette-Text-Asset-Extraction?style=flat-square)](https://github.com/wesellis/APP-Genesis-ROM-Workshop-Sega-Palette-Text-Asset-Extraction/commits)

## Overview

Genesis ROM Workshop (GRW) is a collection of tools for working with Sega Genesis ROM files. It can extract color palettes, text strings, and other assets for analysis or modification. This project is intended for educational purposes, game preservation research, and translation projects.

**✨ NEW!** Now includes professional graphics rendering capabilities - extract and view Genesis tiles as PNG images!

## Features

- **Palette Extraction**: Extract color palettes from ROM files
- **Palette Preview Images**: ✨ NEW! Export palettes as visual PNG images
- **Graphics Rendering**: ✨ NEW! Render Genesis tiles to viewable PNG files
- **Tile Sheet Creation**: ✨ NEW! Create professional sprite sheets
- **Text Extraction**: Find and export text strings
- **Asset Analysis**: Basic ROM structure analysis
- **Hex Editing Tools**: Simple hex viewer and editor
- **Asset Management**: Organize extracted assets
- **Batch Processing**: Process multiple ROM files

## Requirements

- Python 3.8 or higher
- Basic understanding of ROM file structure
- ROM files for analysis (not included)

## Installation

```bash
git clone https://github.com/wesellis/genesis-rom-workshop.git
cd genesis-rom-workshop
pip install -r requirements.txt
```

**Graphics Rendering Requirements:**
```bash
# Required for palette previews and tile rendering
pip install Pillow
```

## Graphics Rendering ✨ NEW!

The toolkit now includes professional graphics rendering capabilities! Extract Genesis graphics and **see them as actual PNG images** instead of raw binary data.

### Quick Start: Graphics Demo

```bash
# Run the complete graphics demo
python examples/example_graphics_rendering.py your_rom.bin
```

This will create:
- **Palette preview images** - See actual colors, not hex values
- **Rendered tile sheets** - Professional sprite sheets like sprite ripping tools
- **Individual tiles** - Pixel-perfect previews with optional grid overlay

### What You Get

**Before (old version):**
- ❌ Raw `.bin` files (unreadable)
- ❌ JSON palette files (hard to visualize colors)
- ❌ Need external tools to view graphics

**After (current version):**
- ✅ PNG images you can open in any image viewer
- ✅ Visual palette color bars
- ✅ Professional tile sheets
- ✅ Pixel grids for analysis
- ✅ Everything self-contained!

See [GRAPHICS_FEATURES.md](docs/GRAPHICS_FEATURES.md) for complete documentation.

## Usage

### Basic Analysis

```bash
# Analyze a ROM file
python grw_pipeline.py analyze game.bin --output-dir ./analysis

# Extract palettes only
python grw_pipeline.py extract-palettes game.bin --format png

# Extract text strings
python grw_pipeline.py extract-text game.bin --output text.json
```

### Working with Tools

Each tool directory contains specialized utilities:

- **palette_editor**: Extract and modify color palettes
- **text_extractor**: Find and export text strings
- **hex_editor**: View and edit ROM bytes
- **asset_extractor**: Extract graphics and assets
- **rom_analyzer**: Analyze ROM structure

### Example: Palette Extraction with Visual Preview

```python
from tools.palette_editor import PaletteEditor

editor = PaletteEditor()
palettes = editor.extract_palettes('sonic.bin')

# Export as JSON
editor.export_palettes(palettes, 'palettes/')

# NEW! Export as visual PNG images
editor.export_palette_as_image(palettes[0], 'palette_preview.png')
editor.export_all_palettes_as_images(palettes, 'palettes/')
```

### Example: Graphics Rendering

```python
from tools.palette_editor import PaletteEditor
from tools.asset_extractor import AssetExtractor

# Extract palette
editor = PaletteEditor()
palettes = editor.extract_palettes('sonic.bin')

# NEW! Extract and render graphics as viewable PNG images
extractor = AssetExtractor()
result = extractor.extract_and_render_graphics(
    'sonic.bin',
    palettes[0],
    max_tiles=256
)

# Creates professional tile sheet PNG!
print(f"Tile sheet created: {result['sheet_file']}")
```

### Example: Text Extraction

```python
from tools.text_extractor import TextExtractor

extractor = TextExtractor()
strings = extractor.find_text('game.bin')
extractor.export_strings(strings, 'text.json')
```

## Project Structure

```
genesis-rom-workshop/
├── grw_pipeline.py           # Main CLI interface
├── requirements.txt          # Python dependencies
├── LICENSE                   # MIT License
├── README.md                 # This file
│
├── tools/                    # Core toolkit modules
│   ├── palette_editor/       # Palette extraction tools
│   ├── graphics_renderer.py  # ✨ Graphics rendering engine
│   ├── text_extractor/       # Text finding tools
│   ├── hex_editor/           # Hex editing utilities
│   ├── asset_extractor/      # Asset extraction with rendering
│   ├── rom_analyzer/         # ROM analysis tools
│   ├── asset_manager/        # Asset organization
│   └── security_utils.py     # Security validation
│
├── examples/                 # Example scripts and demos
│   ├── example_graphics_rendering.py  # Graphics demo
│   ├── example_palette_extraction.py
│   ├── example_text_extraction.py
│   └── example_hex_editing.py
│
├── tests/                    # Test suites
│   ├── test_graphics.py      # Graphics rendering tests
│   └── test_tools.py         # Core tools tests
│
├── docs/                     # Documentation
│   ├── GRAPHICS_FEATURES.md  # Graphics rendering guide
│   ├── USAGE_GUIDE.md        # Usage instructions
│   ├── API_REFERENCE.md      # API documentation
│   ├── SECURITY_HARDENING.md # Security documentation
│   └── ...
│
└── workspace/                # Working directory
    ├── backups/              # ROM backups
    ├── exports/              # Extracted assets
    └── projects/             # Project files
```

## Technical Details

### Dependencies

- **Pillow (PIL)**: ✨ REQUIRED for graphics rendering and palette image exports
- **NumPy**: Binary data processing (optional)
- **Python standard library**: struct, pathlib, json, hashlib

### Graphics Format Support

The toolkit includes a professional 4-bit planar graphics decoder for Genesis tiles:
- **Tile Format**: 8x8 pixels, 32 bytes per tile
- **Color Depth**: 4-bit (16 colors per palette)
- **Encoding**: Planar bitplane format (Genesis standard)
- **Output**: PNG images with configurable scaling (1x to 16x)
- **Features**: Grid overlays, tile sheets, palette rendering

### ROM File Support

- Sega Genesis/Mega Drive (.bin, .gen, .smd)
- Sega Master System (.sms)
- Game Gear (.gg)
- Sega 32X (.32x)

Note: ROM file format detection is basic and may not work with all ROM variants.

## Known Limitations

- ROM structure varies significantly between games
- Text detection may produce false positives
- Palette extraction assumes standard VDP format
- No support for compressed data
- Limited documentation on ROM internals
- Requires manual verification of results

## Use Cases

- **ROM Hacking**: Extract and view graphics, modify palettes, create sprite sheets
- **Game Preservation**: Document ROM structure and assets for archival purposes
- **Translation Projects**: Extract text for localization work
- **Sprite Ripping**: Create professional sprite sheets and texture packs
- **Research**: Study game development techniques and pixel art
- **Education**: Learn about ROM file structure, graphics encoding, and game design
- **Asset Analysis**: Examine color palettes, tile layouts, and graphics techniques

## Legal Notice

This tool is for educational and research purposes only.

**Important**:
- This tool does NOT include ROM files
- Users must own legal copies of any ROMs they analyze
- Respect copyright laws in your jurisdiction
- Do not distribute copyrighted ROM files
- Tool is for analysis only, not piracy

ROM hacking and distribution may be illegal in your country. Use responsibly and ethically.

## Contributing

Contributions welcome! This is a learning project and improvements are appreciated.

1. Fork the repository
2. Create feature branch (`git checkout -b feature/name`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature/name`)
5. Open Pull Request

## Documentation

### User Documentation
- **[GRAPHICS_FEATURES.md](docs/GRAPHICS_FEATURES.md)**: ✨ NEW! Complete graphics rendering guide
- **[USAGE_GUIDE.md](docs/USAGE_GUIDE.md)**: Detailed usage instructions and examples
- **[API_REFERENCE.md](docs/API_REFERENCE.md)**: Complete API documentation

### Project Documentation
- **[WEEK1_IMPROVEMENTS_COMPLETE.md](docs/WEEK1_IMPROVEMENTS_COMPLETE.md)**: Graphics rendering implementation details
- **[SECURITY_HARDENING.md](docs/SECURITY_HARDENING.md)**: Security features and best practices
- **[CHANGELOG.md](docs/CHANGELOG.md)**: Version history and updates
- **[CONTRIBUTING.md](docs/CONTRIBUTING.md)**: Contribution guidelines
- **[ROADMAP.md](docs/ROADMAP.md)**: Future development plans
- **[SECURITY.md](docs/SECURITY.md)**: Security policy

## License

MIT License - see LICENSE file for details.

## Disclaimer

This is a personal educational project. The tools are provided as-is with no guarantees of accuracy or reliability. ROM file structure varies significantly between games, and results may require manual verification.

The author does not condone piracy or copyright infringement. This tool is intended solely for research, preservation, and educational purposes with legally obtained ROM files.

## Author

Wesley Ellis

---

## Project Status & Roadmap

**Completion: ~95%** ✨ **MAJOR UPDATE - Graphics Rendering Implemented!**

### What Works ✅

**Core Functionality:**
- ✅ Palette extraction and modification (full implementation)
- ✅ Palette import/export to JSON format
- ✅ **NEW!** Palette preview images (visual PNG export)
- ✅ **NEW!** Graphics tile rendering (4-bit planar decoding)
- ✅ **NEW!** Tile sheet creation (professional sprite sheets)
- ✅ **NEW!** Grid overlays for pixel analysis
- ✅ Text extraction with ASCII support
- ✅ Text replacement and translation workflow
- ✅ Translation file generation and application
- ✅ Hex viewing with address/hex/ASCII display
- ✅ Hex editing and byte writing
- ✅ ROM comparison and patch creation
- ✅ ROM analysis (header validation, checksums)
- ✅ Asset extraction (graphics, tilemaps, sprites)
- ✅ Asset organization and manifest generation
- ✅ Interactive CLI interface
- ✅ All tool modules properly packaged with __init__.py

**Tool Modules - All Implemented:**
- ✅ **palette_editor/**: Full palette extraction, modification, color swapping, and PNG export
- ✅ **graphics_renderer/**: ✨ NEW! 4-bit planar decoding and tile rendering
- ✅ **text_extractor/**: Text finding, translation export, and ROM patching
- ✅ **hex_editor/**: Hex viewing, editing, searching, and ROM comparison
- ✅ **asset_extractor/**: Graphics tile extraction with rendering support
- ✅ **rom_analyzer/**: Header analysis, checksum validation, entropy calculation
- ✅ **asset_manager/**: Sprite/audio extraction, project organization

### Known Limitations

**Still Missing:**
- ⚠️ **GUI**: Command-line only (graphical interface not implemented)
- ⚠️ **ROM Formats**: Primarily Genesis-focused, SMS/Game Gear/32X support limited
- ⚠️ **Compressed Data**: No support for compressed ROM data (Nemesis/Kosinski)
- ⚠️ **Automated Tests**: Test suite for graphics exists, full pytest coverage needed
- ⚠️ **Sprite Assembly**: Automatic multi-tile sprite composition not implemented
- ⚠️ **Audio Playback**: Audio data extraction only, no playback capability

**Areas for Enhancement:**
- Better encoding support for non-ASCII text (Japanese ROMs)
- More sophisticated graphics format detection
- Automated palette location detection
- Compression algorithm support (Nemesis, Kosinski, etc.)
- Full .smd format support improvements

### Recent Additions (Latest Update)

**Week 1 Graphics Rendering Features** ✨ (Most Recent):
1. ✅ **graphics_renderer.py** - NEW module! 4-bit planar tile decoding
2. ✅ **Palette preview images** - Export palettes as visual PNG files
3. ✅ **Tile rendering** - Render Genesis tiles to viewable PNG images
4. ✅ **Tile sheet creation** - Professional sprite sheet generation
5. ✅ **Grid overlays** - Pixel analysis with grid overlay support
6. ✅ **AssetExtractor integration** - One-step extract and render
7. ✅ **test_graphics.py** - Comprehensive test suite (3/3 tests passed)
8. ✅ **GRAPHICS_FEATURES.md** - Complete documentation

See [GRAPHICS_FEATURES.md](docs/GRAPHICS_FEATURES.md) for detailed documentation and examples.

**Previous Updates - Core Tool Implementation:**
1. ✅ **palette_editor.py** - Full palette extraction, modification, JSON import/export
2. ✅ **text_extractor.py** - Comprehensive text extraction and translation workflow
3. ✅ **asset_manager.py** - Sprite/audio extraction with heuristic detection
4. ✅ **hex_editor.py** - Complete hex viewing, editing, searching, and patching
5. ✅ **rom_analyzer.py** - Header parsing, checksum validation, statistics
6. ✅ **asset_extractor.py** - Graphics tiles, tilemaps, and sprite extraction
7. ✅ **All __init__.py files** - Proper Python package structure
8. ✅ **security_utils.py** - Comprehensive security hardening

### Future Enhancements

Priority features for future development:
1. **Compression Support** - Nemesis, Kosinski, Enigma decompression (Week 2-3)
2. **Sprite Assembly** - Automatic multi-tile sprite composition
3. **Tilemap Rendering** - Full scene/level rendering
4. **GUI Application** - User-friendly graphical interface
5. **Test Suite** - Comprehensive pytest coverage for all modules
6. **Audio Player** - YM2612/PSG playback capability
7. **Multi-ROM Format** - Better SMS/Game Gear/32X support
8. **Advanced Text Encoding** - Shift-JIS and other character sets
9. **Palette Detection** - Automated palette location finding

### Contributing

Contributions welcome! The core toolkit is complete with graphics rendering, but there's room for enhancements:
- Expand test coverage for all modules
- Implement GUI with tkinter or PyQt
- Add compression/decompression support (Nemesis, Kosinski)
- Implement sprite assembly from multiple tiles
- Add tilemap rendering capabilities
- Add audio playback capabilities (YM2612/PSG)
- Enhance documentation with more examples
- Add support for more ROM formats

---

**Note**: This project is for learning about ROM file structure and game preservation. Always respect copyright laws and use legally obtained ROM files. Many features described in the README are partially implemented or planned for future development.
