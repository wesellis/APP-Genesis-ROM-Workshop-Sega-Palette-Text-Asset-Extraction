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

**Note**: This project is for learning about ROM file structure and game preservation. Always respect copyright laws and use legally obtained ROM files.
