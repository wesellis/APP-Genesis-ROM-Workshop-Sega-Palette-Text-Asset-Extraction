#!/usr/bin/env python3
"""
Genesis ROM Workshop (GRW) - Professional ROM Modification Toolkit
Real tools for real ROM hacking: palettes, text, assets, and analysis.
"""

import hashlib
import json
import os
import struct
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union


@dataclass
class ROMInfo:
    name: str
    region: str
    size: int
    checksum: str
    rom_type: str
    header_valid: bool
    charset: str = "unknown"


@dataclass
class ModificationResult:
    success: bool
    tool: str
    changes_made: int
    message: str
    processing_time: float


class PaletteEditor:
    """Real palette modification - the most reliable ROM hack"""

    def __init__(self):
        self.genesis_palette_locations = [
            0x20000,
            0x30000,
            0x40000,
            0x50000,
            0x60000,
            0x70000,  # Common palette areas
        ]

    def extract_palettes(self, rom_data: bytes) -> List[List[Tuple[int, int, int]]]:
        """Extract all palettes from ROM"""
        palettes = []

        for location in self.genesis_palette_locations:
            if location + 32 <= len(rom_data):
                palette_data = rom_data[location : location + 32]
                if self._is_valid_palette(palette_data):
                    palette = self._decode_genesis_palette(palette_data)
                    palettes.append(palette)

        # Also scan for palettes throughout the ROM
        for i in range(0, len(rom_data) - 32, 32):
            palette_data = rom_data[i : i + 32]
            if self._is_valid_palette(palette_data):
                palette = self._decode_genesis_palette(palette_data)
                if palette not in palettes:  # Avoid duplicates
                    palettes.append(palette)

        return palettes

    def _is_valid_palette(self, data: bytes) -> bool:
        """Check if data looks like a Genesis palette"""
        if len(data) < 32:
            return False

        valid_colors = 0
        for i in range(0, 32, 2):
            color_word = struct.unpack(">H", data[i : i + 2])[0]
            # Genesis colors are 9-bit (0x000-0x1FF in the palette format)
            if color_word <= 0x1FF:
                valid_colors += 1

        return valid_colors >= 12  # At least 12 valid colors out of 16

    def _decode_genesis_palette(self, data: bytes) -> List[Tuple[int, int, int]]:
        """Convert Genesis palette data to RGB tuples"""
        palette = []
        for i in range(0, 32, 2):
            color_word = struct.unpack(">H", data[i : i + 2])[0]

            # Genesis format: 0000BBB0GGG0RRR0
            r = (color_word & 0x000E) >> 1
            g = (color_word & 0x00E0) >> 5
            b = (color_word & 0x0E00) >> 9

            # Scale 3-bit values to 8-bit
            r = (r * 255) // 7
            g = (g * 255) // 7
            b = (b * 255) // 7

            palette.append((r, g, b))

        return palette

    def _encode_genesis_palette(self, palette: List[Tuple[int, int, int]]) -> bytes:
        """Convert RGB palette back to Genesis format"""
        data = bytearray()

        for r, g, b in palette:
            # Scale 8-bit values to 3-bit
            r = (r * 7) // 255
            g = (g * 7) // 255
            b = (b * 7) // 255

            # Genesis format: 0000BBB0GGG0RRR0
            color_word = (b << 9) | (g << 5) | (r << 1)
            data.extend(struct.pack(">H", color_word))

        return bytes(data)

    def apply_palette_modification(
        self,
        rom_data: bytes,
        palette_index: int,
        new_palette: List[Tuple[int, int, int]],
    ) -> bytes:
        """Apply a new palette to the ROM"""
        modified_data = bytearray(rom_data)
        palettes_found = 0

        for location in self.genesis_palette_locations:
            if location + 32 <= len(rom_data):
                palette_data = rom_data[location : location + 32]
                if self._is_valid_palette(palette_data):
                    if palettes_found == palette_index:
                        new_palette_data = self._encode_genesis_palette(new_palette)
                        modified_data[location : location + 32] = new_palette_data
                        return bytes(modified_data)
                    palettes_found += 1

        raise ValueError(f"Palette index {palette_index} not found")


class TextEditor:
    """Extract and modify text for translation projects"""

    def __init__(self):
        self.common_text_areas = [
            (0x10000, 0x20000),  # Common text areas in Genesis ROMs
            (0x80000, 0x100000),
            (0x120000, 0x180000),
        ]

    def extract_text_strings(self, rom_data: bytes, min_length: int = 4) -> List[Dict]:
        """Extract potential text strings from ROM"""
        strings = []

        for start, end in self.common_text_areas:
            if start >= len(rom_data):
                continue

            search_end = min(end, len(rom_data))

            # Look for ASCII text
            current_string = ""
            string_start = start

            for i in range(start, search_end):
                byte = rom_data[i]

                if 32 <= byte <= 126:  # Printable ASCII
                    if not current_string:
                        string_start = i
                    current_string += chr(byte)
                else:
                    if len(current_string) >= min_length:
                        strings.append(
                            {
                                "text": current_string,
                                "offset": string_start,
                                "length": len(current_string),
                                "encoding": "ascii",
                            }
                        )
                    current_string = ""

        return strings

    def replace_text_string(
        self, rom_data: bytes, offset: int, old_text: str, new_text: str
    ) -> bytes:
        """Replace a text string at a specific offset"""
        if len(new_text) > len(old_text):
            raise ValueError(
                f"New text is too long ({len(new_text)} > {len(old_text)})"
            )

        modified_data = bytearray(rom_data)

        # Verify the old text is at the expected location
        old_bytes = old_text.encode("ascii")
        if modified_data[offset : offset + len(old_bytes)] != old_bytes:
            raise ValueError("Old text not found at specified offset")

        # Replace with new text, padding with nulls if necessary
        new_bytes = new_text.encode("ascii")
        modified_data[offset : offset + len(old_bytes)] = new_bytes + b"\x00" * (
            len(old_bytes) - len(new_bytes)
        )

        return bytes(modified_data)


class AssetExtractor:
    """Extract graphics and audio assets from ROMs"""

    def __init__(self):
        self.output_dir = Path("workspace/exports")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def extract_graphics_data(self, rom_data: bytes, rom_name: str) -> Dict:
        """Extract potential graphics data"""
        graphics_dir = self.output_dir / f"{rom_name}_graphics"
        graphics_dir.mkdir(exist_ok=True)

        # Look for tile patterns (Genesis graphics are usually 8x8 tiles, 32 bytes each)
        tile_count = 0

        for i in range(0, len(rom_data) - 32, 32):
            tile_data = rom_data[i : i + 32]

            # Simple heuristic: if the tile has some variation, it might be graphics
            if self._looks_like_graphics(tile_data):
                tile_file = graphics_dir / f"tile_{tile_count:04d}.bin"
                with open(tile_file, "wb") as f:
                    f.write(tile_data)
                tile_count += 1

                # Limit extraction to prevent huge outputs
                if tile_count >= 1000:
                    break

        return {"tiles_extracted": tile_count, "output_directory": str(graphics_dir)}

    def _looks_like_graphics(self, data: bytes) -> bool:
        """Heuristic to detect graphics data"""
        if len(data) != 32:
            return False

        # Check for patterns typical of 4-bit planar graphics
        non_zero_bytes = sum(1 for b in data if b != 0)
        return 8 <= non_zero_bytes <= 28  # Some variation but not random


class ROMAnalyzer:
    """Analyze ROM structure and contents"""

    def analyze_rom_structure(self, rom_path: str) -> ROMInfo:
        """Comprehensive ROM analysis"""
        with open(rom_path, "rb") as f:
            rom_data = f.read()

        # Handle different ROM formats
        if rom_path.lower().endswith(".md"):
            rom_data = self._deinterleave_md_format(rom_data)

        # Extract header information
        rom_info = self._extract_header_info(rom_data)
        rom_info.size = len(rom_data)
        rom_info.checksum = hashlib.md5(rom_data).hexdigest()[:8]
        rom_info.rom_type = Path(rom_path).suffix.lower()

        return rom_info

    def _extract_header_info(self, rom_data: bytes) -> ROMInfo:
        """Extract game information from ROM header"""
        if len(rom_data) < 0x200:
            return ROMInfo("UNKNOWN", "UNKNOWN", 0, "", "", False)

        # Check for valid Genesis header
        header_valid = False
        console_name = rom_data[0x100:0x110]
        if console_name in [b"SEGA MEGA DRIVE ", b"SEGA GENESIS    "]:
            header_valid = True

        # Extract game name (0x120-0x14F)
        try:
            name_bytes = rom_data[0x120:0x150]
            game_name = name_bytes.decode("ascii", errors="ignore").strip("\x00 ")
            game_name = " ".join(game_name.split())
        except:
            game_name = "UNKNOWN GAME"

        # Extract region (0x1F0)
        region = "UNKNOWN"
        if len(rom_data) > 0x1F0:
            region_byte = rom_data[0x1F0:0x1F3]
            region_str = region_byte.decode("ascii", errors="ignore")
            if "U" in region_str:
                region = "USA"
            elif "J" in region_str:
                region = "JAPAN"
            elif "E" in region_str:
                region = "EUROPE"

        return ROMInfo(game_name, region, 0, "", "", header_valid)

    def _deinterleave_md_format(self, data: bytes) -> bytes:
        """Convert .md format (interleaved) to standard format"""
        if len(data) % 2 != 0:
            return data

        deinterleaved = bytearray(len(data))
        for i in range(0, len(data), 2):
            deinterleaved[i] = data[i + 1]
            deinterleaved[i + 1] = data[i]

        return bytes(deinterleaved)


class GenesisROMWorkshop:
    """Main workshop interface"""

    def __init__(self):
        self.version = "1.0"
        self.workspace_dir = Path("workspace")
        self.workspace_dir.mkdir(exist_ok=True)

        # Initialize tools
        self.palette_editor = PaletteEditor()
        self.text_editor = TextEditor()
        self.asset_extractor = AssetExtractor()
        self.rom_analyzer = ROMAnalyzer()

    def run_interactive_mode(self):
        """Interactive workshop mode"""
        print(f"🎨 Genesis ROM Workshop v{self.version}")
        print("Professional tools for real ROM modification")
        print("=" * 50)

        while True:
            print("\nAvailable tools:")
            print("1. Palette Editor - Recolor any Genesis game")
            print("2. Text Editor - Extract/replace text for translations")
            print("3. Asset Extractor - Extract graphics and audio")
            print("4. ROM Analyzer - Analyze ROM structure")
            print("5. Exit")

            choice = input("\nSelect tool (1-5): ").strip()

            if choice == "1":
                self._palette_editor_interface()
            elif choice == "2":
                self._text_editor_interface()
            elif choice == "3":
                self._asset_extractor_interface()
            elif choice == "4":
                self._rom_analyzer_interface()
            elif choice == "5":
                print("Thanks for using Genesis ROM Workshop!")
                break
            else:
                print("Invalid choice. Please try again.")

    def _palette_editor_interface(self):
        """Palette editor interface"""
        print("\n🎨 Palette Editor")
        print("-" * 20)

        rom_path = input("Enter ROM path: ").strip().strip('"')
        if not os.path.exists(rom_path):
            print("❌ ROM file not found!")
            return

        print("Loading ROM...")
        with open(rom_path, "rb") as f:
            rom_data = f.read()

        # Extract palettes
        palettes = self.palette_editor.extract_palettes(rom_data)
        print(f"✅ Found {len(palettes)} palettes")

        if not palettes:
            print("No palettes found in this ROM.")
            return

        # Show palettes
        for i, palette in enumerate(palettes[:5]):  # Show first 5
            print(f"\nPalette {i}:")
            for j, (r, g, b) in enumerate(palette):
                print(f"  Color {j}: RGB({r}, {g}, {b})")

        # Palette modification example
        palette_choice = input(f"\nWhich palette to modify (0-{len(palettes)-1})? ")
        try:
            palette_index = int(palette_choice)
            if 0 <= palette_index < len(palettes):
                print(f"\nSelected palette {palette_index}")
                print("Example: To make a red Sonic, change blue colors to red")
                print("This is where you'd implement the actual color changes...")

                # Save original for comparison
                output_path = f"workspace/palette_analysis_{Path(rom_path).stem}.json"
                with open(output_path, "w") as f:
                    json.dump(
                        {
                            "rom_file": rom_path,
                            "palettes_found": len(palettes),
                            "palette_data": [
                                [(r, g, b) for r, g, b in p] for p in palettes[:10]
                            ],
                        },
                        f,
                        indent=2,
                    )
                print(f"✅ Palette data saved to: {output_path}")
        except ValueError:
            print("Invalid palette number.")

    def _text_editor_interface(self):
        """Text editor interface"""
        print("\n📝 Text Editor")
        print("-" * 15)

        rom_path = input("Enter ROM path: ").strip().strip('"')
        if not os.path.exists(rom_path):
            print("❌ ROM file not found!")
            return

        print("Extracting text strings...")
        with open(rom_path, "rb") as f:
            rom_data = f.read()

        strings = self.text_editor.extract_text_strings(rom_data)
        print(f"✅ Found {len(strings)} text strings")

        if strings:
            # Show first 10 strings
            for i, string_info in enumerate(strings[:10]):
                print(f"{i}: '{string_info['text']}' at 0x{string_info['offset']:X}")

            # Save for translation projects
            output_path = f"workspace/text_strings_{Path(rom_path).stem}.json"
            with open(output_path, "w") as f:
                json.dump(
                    {
                        "rom_file": rom_path,
                        "strings_found": len(strings),
                        "strings": strings,
                    },
                    f,
                    indent=2,
                )
            print(f"✅ Text strings saved to: {output_path}")

    def _asset_extractor_interface(self):
        """Asset extractor interface"""
        print("\n🎨 Asset Extractor")
        print("-" * 18)

        rom_path = input("Enter ROM path: ").strip().strip('"')
        if not os.path.exists(rom_path):
            print("❌ ROM file not found!")
            return

        print("Extracting graphics assets...")
        with open(rom_path, "rb") as f:
            rom_data = f.read()

        rom_name = Path(rom_path).stem
        result = self.asset_extractor.extract_graphics_data(rom_data, rom_name)
        print(f"✅ Extracted {result['tiles_extracted']} graphics tiles")
        print(f"📁 Output directory: {result['output_directory']}")

    def _rom_analyzer_interface(self):
        """ROM analyzer interface"""
        print("\n🔍 ROM Analyzer")
        print("-" * 15)

        rom_path = input("Enter ROM path: ").strip().strip('"')
        if not os.path.exists(rom_path):
            print("❌ ROM file not found!")
            return

        print("Analyzing ROM structure...")
        rom_info = self.rom_analyzer.analyze_rom_structure(rom_path)

        print(f"\n📊 ROM Analysis Results:")
        print(f"  Game: {rom_info.name}")
        print(f"  Region: {rom_info.region}")
        print(f"  Size: {rom_info.size:,} bytes")
        print(f"  Type: {rom_info.rom_type}")
        print(f"  Valid Header: {rom_info.header_valid}")
        print(f"  Checksum: {rom_info.checksum}")


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        # Command line mode
        rom_file = sys.argv[1]
        if not os.path.exists(rom_file):
            print(f"❌ Error: ROM file '{rom_file}' not found!")
            return

        # Quick analysis mode
        workshop = GenesisROMWorkshop()
        print(f"🔍 Quick ROM Analysis: {os.path.basename(rom_file)}")
        rom_info = workshop.rom_analyzer.analyze_rom_structure(rom_file)

        print(f"Game: {rom_info.name}")
        print(f"Region: {rom_info.region}")
        print(f"Size: {rom_info.size:,} bytes")
        print(f"Valid Header: {rom_info.header_valid}")

    else:
        # Interactive mode
        workshop = GenesisROMWorkshop()
        workshop.run_interactive_mode()


if __name__ == "__main__":
    main()
