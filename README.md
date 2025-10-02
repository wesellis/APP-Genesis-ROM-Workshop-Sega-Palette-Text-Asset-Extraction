# Genesis ROM Workshop

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A Python toolkit for analyzing and extracting assets from Sega Genesis/Mega Drive ROM files.

## Overview

Genesis ROM Workshop (GRW) is a collection of tools for working with Sega Genesis ROM files. It can extract color palettes, text strings, and other assets for analysis or modification. This project is intended for educational purposes, game preservation research, and translation projects.

## Features

- **Palette Extraction**: Extract color palettes from ROM files
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

### Example: Palette Extraction

```python
from tools.palette_editor import PaletteEditor

editor = PaletteEditor()
palettes = editor.extract_palettes('sonic.bin')
editor.export_palettes(palettes, 'palettes/')
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
├── tools/
│   ├── palette_editor/       # Palette extraction tools
│   ├── text_extractor/       # Text finding tools
│   ├── hex_editor/           # Hex editing utilities
│   ├── asset_extractor/      # Asset extraction
│   ├── rom_analyzer/         # ROM analysis tools
│   └── asset_manager/        # Asset organization
├── examples/                 # Example scripts
└── workspace/                # Working directory for projects
```

## Technical Details

### Dependencies

- **Pillow (PIL)**: Image handling for palette exports
- **NumPy**: Binary data processing
- **Python standard library**: struct, pathlib, json, hashlib

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

- **Game Preservation**: Document ROM structure for archival purposes
- **Translation Projects**: Extract text for localization work
- **Research**: Study game development techniques
- **Education**: Learn about ROM file structure and game design

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

- **CHANGELOG.md**: Version history and updates
- **CONTRIBUTING.md**: Contribution guidelines
- **ROADMAP.md**: Future development plans
- **SECURITY.md**: Security policy and reporting

## License

MIT License - see LICENSE file for details.

## Disclaimer

This is a personal educational project. The tools are provided as-is with no guarantees of accuracy or reliability. ROM file structure varies significantly between games, and results may require manual verification.

The author does not condone piracy or copyright infringement. This tool is intended solely for research, preservation, and educational purposes with legally obtained ROM files.

## Author

Wesley Ellis

---

## Project Status & Roadmap

**Completion: ~50%**

### What Works
- ✅ Palette extraction from Genesis ROMs (grw_pipeline.py contains functional code)
- ✅ Basic ROM file reading and structure analysis
- ✅ Genesis palette decoding (9-bit color format)
- ✅ Project structure with organized tool directories
- ✅ Basic CLI interface (grw_pipeline.py)
- ✅ ROM info extraction (name, region, size, checksum)

### Known Limitations & Missing Features

**Tool Directories Are Mostly Empty:**
- ⚠️ **palette_editor/**: Has small stub file (~900 bytes) - not full implementation
- ⚠️ **text_extractor/**: Has tiny stub (~520 bytes) - basic at best
- ⚠️ **hex_editor/**: Directory exists but functionality unknown
- ⚠️ **asset_extractor/**: Directory exists but implementation unclear
- ⚠️ **rom_analyzer/**: Directory exists but needs verification
- ⚠️ **asset_manager/**: Directory exists but likely not implemented

**Features Described But Not Fully Implemented:**
- ❌ **Palette Modification**: Extraction works, but editing/saving not verified
- ❌ **Text Extraction**: Stub exists but comprehensive text finding not confirmed
- ❌ **Hex Editor**: Mentioned in README but implementation status unknown
- ❌ **Asset Management**: Directory structure only
- ❌ **Batch Processing**: Mentioned but not verified to work

**Missing Features:**
- ⚠️ **GUI**: Command-line only
- ⚠️ **ROM Formats**: Claims to support SMS/Game Gear/32X but likely Genesis-only
- ⚠️ **Compressed Data**: No support for compressed ROM data
- ⚠️ **Testing**: No test suite
- ⚠️ **Documentation**: Limited examples and guides
- ⚠️ **Export Formats**: PNG palette export mentioned but not confirmed

**Code Quality:**
- ⚠️ **Incomplete Tools**: Most tool directories have stub files only
- ⚠️ **No Tests**: No automated tests
- ⚠️ **Limited Error Handling**: Basic validation only
- ⚠️ **No Logging**: Minimal logging or debugging support

### What Needs Work

1. **Complete Tool Implementations** - Flesh out all tool directory stubs into working tools
2. **Text Extraction** - Implement comprehensive text finding with proper encoding support
3. **Palette Editing** - Add ability to modify and save palette changes back to ROM
4. **Asset Extraction** - Implement graphics/sprite extraction
5. **Hex Editor** - Build functional hex viewing and editing interface
6. **GUI Application** - Create user-friendly graphical interface
7. **Testing Suite** - Add comprehensive tests for ROM parsing
8. **Better Documentation** - Add detailed examples for each tool
9. **Multi-Format Support** - Implement claimed SMS/Game Gear/32X support
10. **Error Handling** - Robust handling of malformed or unusual ROMs

### Current Status

This project has a **solid foundation** with working palette extraction, but most features described in the README are not fully implemented. The main grw_pipeline.py file (524 lines) contains actual functional code for palette extraction and basic ROM analysis. However, the individual tool directories mostly contain small stub files rather than complete implementations.

It's a good **starting point** for ROM analysis work, but needs significant development to become the full toolkit described in the README.

### Contributing

If you'd like to help complete this project, contributions are welcome. Priority areas:
1. Implementing text extraction with proper encoding support
2. Building out hex editor functionality
3. Creating sprite/asset extraction tools
4. Adding comprehensive tests
5. Writing detailed usage documentation

---

**Note**: This project is for learning about ROM file structure and game preservation. Always respect copyright laws and use legally obtained ROM files. Many features described in the README are partially implemented or planned for future development.
