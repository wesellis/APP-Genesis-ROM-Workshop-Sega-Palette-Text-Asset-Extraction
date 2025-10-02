# Genesis ROM Workshop - Palette Editor
# Professional palette extraction and modification for Genesis ROMs
"""
Palette Editor Module

This module provides functionality for extracting, modifying, and managing
color palettes from Sega Genesis/Mega Drive ROM files.

Genesis uses 9-bit color (3 bits per channel) stored in a specific format:
0000BBB0GGG0RRR0 (16-bit word, big-endian)
"""
import json
import struct
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Add parent directory to path for security_utils import
sys.path.insert(0, str(Path(__file__).parent.parent))
from security_utils import (
    safe_read_file, safe_write_file, validate_input_path,
    validate_output_path, MAX_ROM_SIZE, MAX_JSON_SIZE, SecurityError
)


class PaletteEditor:
    """
    Professional palette modification for Genesis ROMs.

    This class handles extraction, modification, and export of Genesis color palettes.
    Palettes consist of 16 colors each, with 9-bit color depth (512 total colors).

    Attributes:
        genesis_palette_locations: Common memory locations where palettes are stored
        PALETTE_SIZE: Number of bytes in a Genesis palette (32 bytes = 16 colors * 2 bytes)
        COLORS_PER_PALETTE: Number of colors in each palette (16)
    """

    PALETTE_SIZE = 32
    COLORS_PER_PALETTE = 16

    def __init__(self):
        """Initialize PaletteEditor with common palette memory locations."""
        self.genesis_palette_locations = [
            0x20000, 0x30000, 0x40000, 0x50000, 0x60000, 0x70000
        ]

    def extract_palettes(
        self,
        rom_path: str,
        max_scan: Optional[int] = None
    ) -> List[List[Tuple[int, int, int]]]:
        """
        Extract all color palettes from Genesis ROM.

        Args:
            rom_path: Path to the ROM file
            max_scan: Maximum number of palettes to find during full scan (default: 100 for safety)

        Returns:
            List of palettes, where each palette is a list of 16 RGB tuples

        Raises:
            FileNotFoundError: If ROM file doesn't exist
            SecurityError: If file fails security validation
            IOError: If ROM file cannot be read
            ValueError: If ROM file is too small
        """
        # Security: Validate input path and read with size limits
        rom_data = safe_read_file(
            rom_path,
            max_size=MAX_ROM_SIZE,
            allowed_extensions=['.bin', '.gen', '.md', '.smd', '.32x', '.gg', '.sms']
        )

        if len(rom_data) < self.PALETTE_SIZE:
            raise ValueError(f"ROM file too small (minimum {self.PALETTE_SIZE} bytes required)")

        # Security: Default max_scan to prevent resource exhaustion
        if max_scan is None:
            max_scan = 100  # Reasonable default limit

        palettes = []
        palette_count = 0

        # Check known palette locations first
        for location in self.genesis_palette_locations:
            if location + self.PALETTE_SIZE <= len(rom_data):
                palette_data = rom_data[location : location + self.PALETTE_SIZE]
                if self._is_valid_palette(palette_data):
                    palette = self._decode_genesis_palette(palette_data)
                    if palette not in palettes:
                        palettes.append(palette)

        # Scan for additional palettes throughout the ROM
        for i in range(0, len(rom_data) - self.PALETTE_SIZE, self.PALETTE_SIZE):
            if max_scan and palette_count >= max_scan:
                break

            palette_data = rom_data[i : i + self.PALETTE_SIZE]
            if self._is_valid_palette(palette_data):
                palette = self._decode_genesis_palette(palette_data)
                if palette not in palettes:  # Avoid duplicates
                    palettes.append(palette)
                    palette_count += 1

        return palettes

    def apply_palette_swap(
        self,
        rom_path: str,
        palette_index: int,
        new_palette: List[Tuple[int, int, int]],
        output_path: Optional[str] = None,
    ) -> str:
        """
        Apply a new color palette to ROM at specified index.

        Args:
            rom_path: Path to the ROM file
            palette_index: Index of the palette to replace (0-based)
            new_palette: List of 16 RGB tuples (each value 0-255)
            output_path: Output path for modified ROM (default: adds '_modified' to filename)

        Returns:
            Path to the modified ROM file

        Raises:
            FileNotFoundError: If ROM file doesn't exist
            ValueError: If palette has wrong number of colors or invalid RGB values
            ValueError: If palette index not found in ROM
        """
        # Validation
        if len(new_palette) != self.COLORS_PER_PALETTE:
            raise ValueError(
                f"Genesis palettes must have exactly {self.COLORS_PER_PALETTE} colors, "
                f"got {len(new_palette)}"
            )

        for i, (r, g, b) in enumerate(new_palette):
            if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
                raise ValueError(
                    f"Invalid RGB values at color {i}: ({r}, {g}, {b}). "
                    f"Values must be 0-255"
                )

        # Security: Validate and read ROM with size limits
        rom_data = safe_read_file(
            rom_path,
            max_size=MAX_ROM_SIZE,
            allowed_extensions=['.bin', '.gen', '.md', '.smd', '.32x', '.gg', '.sms']
        )

        modified_data = bytearray(rom_data)
        palettes_found = 0

        # Find and replace the specified palette
        for location in self.genesis_palette_locations:
            if location + self.PALETTE_SIZE <= len(rom_data):
                palette_data = rom_data[location : location + self.PALETTE_SIZE]
                if self._is_valid_palette(palette_data):
                    if palettes_found == palette_index:
                        new_palette_data = self._encode_genesis_palette(new_palette)
                        modified_data[location : location + self.PALETTE_SIZE] = new_palette_data

                        # Determine output path
                        if output_path is None:
                            rom_path_obj = Path(rom_path)
                            output_path = str(
                                rom_path_obj.with_stem(rom_path_obj.stem + "_modified")
                            )

                        # Security: Validate output path and write safely
                        safe_write_file(output_path, modified_data, allow_overwrite=True)

                        return output_path
                    palettes_found += 1

        raise ValueError(
            f"Palette index {palette_index} not found in ROM. "
            f"Found {palettes_found} palettes in known locations."
        )

    def export_palette_to_json(
        self,
        palette: List[Tuple[int, int, int]],
        output_path: str
    ) -> None:
        """
        Export palette as JSON for editing.

        Args:
            palette: List of 16 RGB tuples
            output_path: Path to save JSON file

        Raises:
            ValueError: If palette has wrong number of colors
            IOError: If file cannot be written
        """
        if len(palette) != self.COLORS_PER_PALETTE:
            raise ValueError(
                f"Palette must have {self.COLORS_PER_PALETTE} colors, got {len(palette)}"
            )

        palette_data = {
            "format": "genesis_rgb",
            "bits_per_channel": 3,
            "total_colors": len(palette),
            "colors": [{"r": r, "g": g, "b": b, "index": i}
                      for i, (r, g, b) in enumerate(palette)],
        }

        # Security: Validate output path
        validate_output_path(output_path, allow_overwrite=True)

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(palette_data, f, indent=2)
        except IOError as e:
            raise IOError(f"Failed to write JSON file: {e}")

    def import_palette_from_json(self, json_path: str) -> List[Tuple[int, int, int]]:
        """
        Import palette from JSON file.

        Args:
            json_path: Path to JSON palette file

        Returns:
            List of 16 RGB tuples

        Raises:
            FileNotFoundError: If JSON file doesn't exist
            ValueError: If JSON format is invalid or has wrong number of colors
        """
        # Security: Validate input path with size limit for JSON
        validate_input_path(
            json_path,
            must_exist=True,
            allowed_extensions=['.json'],
            max_size=MAX_JSON_SIZE
        )

        try:
            with open(json_path, "r", encoding="utf-8") as f:
                # Security: Limit JSON file size
                json_content = f.read(MAX_JSON_SIZE)
                if len(f.read(1)) > 0:  # Check if there's more data
                    raise SecurityError(f"JSON file exceeds maximum size of {MAX_JSON_SIZE:,} bytes")

                palette_data = json.loads(json_content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")
        except IOError as e:
            raise IOError(f"Failed to read JSON file: {e}")

        if "colors" not in palette_data:
            raise ValueError("JSON file missing 'colors' field")

        colors = palette_data["colors"]
        if len(colors) != self.COLORS_PER_PALETTE:
            raise ValueError(
                f"Palette must have {self.COLORS_PER_PALETTE} colors, got {len(colors)}"
            )

        try:
            palette = [(c["r"], c["g"], c["b"]) for c in colors]
        except KeyError as e:
            raise ValueError(f"Invalid color format in JSON: missing {e}")

        # Validate RGB values
        for i, (r, g, b) in enumerate(palette):
            if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
                raise ValueError(
                    f"Invalid RGB values at color {i}: ({r}, {g}, {b})"
                )

        return palette

    def export_palette_as_image(
        self,
        palette: List[Tuple[int, int, int]],
        output_path: str,
        scale: int = 20
    ) -> None:
        """
        Export palette as a visual PNG image for easy viewing.

        Creates a horizontal color bar showing all 16 colors in the palette.

        Args:
            palette: List of 16 RGB tuples
            output_path: Path to save PNG file
            scale: Width of each color in pixels (default: 20)

        Raises:
            ValueError: If palette has wrong number of colors
            IOError: If image cannot be written
        """
        try:
            from PIL import Image
        except ImportError:
            raise ImportError(
                "Pillow (PIL) is required for image export. "
                "Install with: pip install Pillow"
            )

        if len(palette) != self.COLORS_PER_PALETTE:
            raise ValueError(
                f"Palette must have {self.COLORS_PER_PALETTE} colors, got {len(palette)}"
            )

        # Security: Validate output path
        validate_output_path(output_path, allow_overwrite=True)

        # Create image: 16 colors x scale pixels wide, scale pixels tall
        width = self.COLORS_PER_PALETTE * scale
        height = scale
        img = Image.new('RGB', (width, height))

        # Draw each color as a vertical bar
        pixels = img.load()
        for color_idx, (r, g, b) in enumerate(palette):
            for x in range(scale):
                for y in range(scale):
                    pixel_x = color_idx * scale + x
                    pixels[pixel_x, y] = (r, g, b)

        try:
            img.save(output_path)
        except IOError as e:
            raise IOError(f"Failed to save palette image: {e}")

    def export_all_palettes_as_images(
        self,
        palettes: List[List[Tuple[int, int, int]]],
        output_dir: str,
        prefix: str = "palette"
    ) -> List[str]:
        """
        Export all palettes as individual PNG images.

        Args:
            palettes: List of palettes to export
            output_dir: Directory to save images
            prefix: Filename prefix (default: "palette")

        Returns:
            List of paths to created image files

        Raises:
            IOError: If directory cannot be created or files cannot be written
        """
        from pathlib import Path

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        created_files = []

        for i, palette in enumerate(palettes):
            image_path = output_path / f"{prefix}_{i:03d}.png"
            self.export_palette_as_image(palette, str(image_path))
            created_files.append(str(image_path))

        return created_files

    def _is_valid_palette(self, data: bytes) -> bool:
        """
        Check if data looks like a valid Genesis palette.

        Args:
            data: 32 bytes of potential palette data

        Returns:
            True if data appears to be a valid palette
        """
        if len(data) < self.PALETTE_SIZE:
            return False

        valid_colors = 0
        for i in range(0, self.PALETTE_SIZE, 2):
            color_word = struct.unpack(">H", data[i : i + 2])[0]
            # Genesis colors are 9-bit (0x000-0x1FF in the palette format)
            if color_word <= 0x1FF:
                valid_colors += 1

        # At least 75% of colors should be valid (12 out of 16)
        return valid_colors >= 12

    def _decode_genesis_palette(self, data: bytes) -> List[Tuple[int, int, int]]:
        """
        Convert Genesis palette data to RGB tuples.

        Genesis uses 9-bit color in format: 0000BBB0GGG0RRR0
        Each channel is 3 bits (0-7), scaled to 8-bit (0-255)

        Args:
            data: 32 bytes of palette data

        Returns:
            List of 16 RGB tuples
        """
        palette = []
        for i in range(0, self.PALETTE_SIZE, 2):
            color_word = struct.unpack(">H", data[i : i + 2])[0]

            # Extract 3-bit color components
            r = (color_word & 0x000E) >> 1
            g = (color_word & 0x00E0) >> 5
            b = (color_word & 0x0E00) >> 9

            # Scale 3-bit values (0-7) to 8-bit (0-255)
            r = (r * 255) // 7
            g = (g * 255) // 7
            b = (b * 255) // 7

            palette.append((r, g, b))

        return palette

    def _encode_genesis_palette(self, palette: List[Tuple[int, int, int]]) -> bytes:
        """
        Convert RGB palette back to Genesis format.

        Args:
            palette: List of 16 RGB tuples

        Returns:
            32 bytes of Genesis palette data
        """
        data = bytearray()

        for r, g, b in palette:
            # Clamp values to valid range
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))

            # Scale 8-bit values (0-255) to 3-bit (0-7)
            r = (r * 7) // 255
            g = (g * 7) // 255
            b = (b * 7) // 255

            # Encode in Genesis format: 0000BBB0GGG0RRR0
            color_word = (b << 9) | (g << 5) | (r << 1)
            data.extend(struct.pack(">H", color_word))

        return bytes(data)
