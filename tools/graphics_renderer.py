"""
Graphics Renderer Module

This module provides functionality for rendering Genesis graphics tiles to PNG images.
Handles 4-bit planar format used by Sega Genesis/Mega Drive.

Genesis graphics are stored as 8x8 pixel tiles in 4-bit planar format:
- Each tile is 32 bytes (8 rows x 4 bytes per row)
- 4 bitplanes encode color indices (0-15)
- Requires a palette to render to RGB
"""

import sys
from pathlib import Path
from typing import List, Optional, Tuple

# Add parent directory for security_utils
sys.path.insert(0, str(Path(__file__).parent))
from security_utils import validate_output_path


class GraphicsRenderer:
    """
    Render Genesis graphics tiles to PNG images.

    Handles decoding 4-bit planar format and rendering with palettes.
    """

    TILE_SIZE = 8  # 8x8 pixels
    TILE_BYTES = 32  # 32 bytes per tile
    BITS_PER_PIXEL = 4  # 4-bit color

    def __init__(self):
        """Initialize graphics renderer."""
        try:
            from PIL import Image
            self.PIL_Image = Image
        except ImportError:
            raise ImportError(
                "Pillow (PIL) is required for graphics rendering. "
                "Install with: pip install Pillow"
            )

    def decode_tile_planar(self, tile_data: bytes) -> List[List[int]]:
        """
        Decode a Genesis tile from 4-bit planar format.

        Genesis tiles are stored as 4 bitplanes:
        - Each bitplane is 1 bit per pixel
        - 4 bitplanes = 4 bits per pixel (16 colors)
        - Stored row by row, all bitplanes for row before next row

        Args:
            tile_data: 32 bytes of tile data

        Returns:
            8x8 array of pixel indices (0-15)

        Raises:
            ValueError: If tile_data is not 32 bytes
        """
        if len(tile_data) != self.TILE_BYTES:
            raise ValueError(
                f"Tile data must be {self.TILE_BYTES} bytes, got {len(tile_data)}"
            )

        pixels = [[0 for _ in range(self.TILE_SIZE)] for _ in range(self.TILE_SIZE)]

        # Decode each row
        for row in range(self.TILE_SIZE):
            # Each row has 4 bytes (4 bitplanes)
            offset = row * 4

            for col in range(self.TILE_SIZE):
                pixel_value = 0

                # Combine bits from all 4 bitplanes
                for plane in range(4):
                    byte = tile_data[offset + plane]
                    # Get bit for this column (MSB first)
                    bit = (byte >> (7 - col)) & 1
                    # Add bit to pixel value (plane 0 = LSB)
                    pixel_value |= (bit << plane)

                pixels[row][col] = pixel_value

        return pixels

    def render_tile(
        self,
        tile_data: bytes,
        palette: List[Tuple[int, int, int]],
        scale: int = 1
    ):
        """
        Render a single tile to a PIL Image.

        Args:
            tile_data: 32 bytes of tile data
            palette: List of 16 RGB tuples
            scale: Scale factor for output image (default: 1)

        Returns:
            PIL Image object

        Raises:
            ValueError: If tile_data or palette is invalid
        """
        if len(palette) != 16:
            raise ValueError(f"Palette must have 16 colors, got {len(palette)}")

        # Decode tile to pixel indices
        pixels = self.decode_tile_planar(tile_data)

        # Create image
        size = self.TILE_SIZE * scale
        img = self.PIL_Image.new('RGB', (size, size))
        img_pixels = img.load()

        # Render pixels with palette
        for y in range(self.TILE_SIZE):
            for x in range(self.TILE_SIZE):
                color_index = pixels[y][x]
                color = palette[color_index]

                # Draw scaled pixel
                for dy in range(scale):
                    for dx in range(scale):
                        px = x * scale + dx
                        py = y * scale + dy
                        img_pixels[px, py] = color

        return img

    def render_tile_to_file(
        self,
        tile_data: bytes,
        palette: List[Tuple[int, int, int]],
        output_path: str,
        scale: int = 4
    ) -> None:
        """
        Render a tile and save to PNG file.

        Args:
            tile_data: 32 bytes of tile data
            palette: List of 16 RGB tuples
            output_path: Path to save PNG
            scale: Scale factor (default: 4 for 32x32 output)

        Raises:
            ValueError: If tile_data or palette is invalid
            IOError: If file cannot be written
        """
        # Security: Validate output path
        validate_output_path(output_path, allow_overwrite=True)

        img = self.render_tile(tile_data, palette, scale)

        try:
            img.save(output_path)
        except IOError as e:
            raise IOError(f"Failed to save tile image: {e}")

    def render_tile_sheet(
        self,
        tiles: List[bytes],
        palette: List[Tuple[int, int, int]],
        columns: int = 16,
        scale: int = 2
    ):
        """
        Render multiple tiles as a sheet.

        Args:
            tiles: List of 32-byte tile data
            palette: List of 16 RGB tuples
            columns: Number of tiles per row (default: 16)
            scale: Scale factor for each tile (default: 2)

        Returns:
            PIL Image object containing tile sheet

        Raises:
            ValueError: If tiles or palette is invalid
        """
        if not tiles:
            raise ValueError("No tiles provided")

        # Calculate sheet dimensions
        num_tiles = len(tiles)
        rows = (num_tiles + columns - 1) // columns  # Ceiling division

        tile_size = self.TILE_SIZE * scale
        sheet_width = columns * tile_size
        sheet_height = rows * tile_size

        # Create sheet image
        sheet = self.PIL_Image.new('RGB', (sheet_width, sheet_height))

        # Render each tile
        for idx, tile_data in enumerate(tiles):
            row = idx // columns
            col = idx % columns

            try:
                tile_img = self.render_tile(tile_data, palette, scale)

                # Paste tile into sheet
                x = col * tile_size
                y = row * tile_size
                sheet.paste(tile_img, (x, y))

            except ValueError:
                # Skip invalid tiles
                continue

        return sheet

    def render_tile_sheet_to_file(
        self,
        tiles: List[bytes],
        palette: List[Tuple[int, int, int]],
        output_path: str,
        columns: int = 16,
        scale: int = 2
    ) -> None:
        """
        Render tile sheet and save to PNG file.

        Args:
            tiles: List of 32-byte tile data
            palette: List of 16 RGB tuples
            output_path: Path to save PNG
            columns: Number of tiles per row (default: 16)
            scale: Scale factor (default: 2)

        Raises:
            ValueError: If tiles or palette is invalid
            IOError: If file cannot be written
        """
        # Security: Validate output path
        validate_output_path(output_path, allow_overwrite=True)

        sheet = self.render_tile_sheet(tiles, palette, columns, scale)

        try:
            sheet.save(output_path)
        except IOError as e:
            raise IOError(f"Failed to save tile sheet: {e}")

    def extract_and_render_tiles(
        self,
        rom_data: bytes,
        palette: List[Tuple[int, int, int]],
        max_tiles: int = 256,
        output_path: Optional[str] = None
    ):
        """
        Extract tiles from ROM and render as sheet.

        Args:
            rom_data: ROM file data
            palette: List of 16 RGB tuples
            max_tiles: Maximum tiles to extract (default: 256)
            output_path: Path to save sheet (optional)

        Returns:
            PIL Image object (and saves to file if output_path provided)

        Raises:
            ValueError: If palette is invalid
        """
        tiles = []

        # Extract tiles from ROM
        for i in range(0, len(rom_data) - self.TILE_BYTES, self.TILE_BYTES):
            if len(tiles) >= max_tiles:
                break

            tile_data = rom_data[i : i + self.TILE_BYTES]

            # Basic validation: check if tile has some data
            if not all(b == 0 for b in tile_data):
                tiles.append(tile_data)

        if not tiles:
            raise ValueError("No valid tiles found in ROM data")

        # Render sheet
        sheet = self.render_tile_sheet(tiles, palette)

        # Save if path provided
        if output_path:
            self.render_tile_sheet_to_file(tiles, palette, output_path)

        return sheet

    def create_tile_preview(
        self,
        tile_data: bytes,
        palette: List[Tuple[int, int, int]],
        output_path: str,
        show_grid: bool = True,
        scale: int = 8
    ) -> None:
        """
        Create a detailed tile preview with optional grid.

        Args:
            tile_data: 32 bytes of tile data
            palette: List of 16 RGB tuples
            output_path: Path to save PNG
            show_grid: Whether to show pixel grid (default: True)
            scale: Scale factor (default: 8 for 64x64 output)

        Raises:
            ValueError: If tile_data or palette is invalid
            IOError: If file cannot be written
        """
        img = self.render_tile(tile_data, palette, scale)

        if show_grid:
            from PIL import ImageDraw

            draw = ImageDraw.Draw(img)
            size = self.TILE_SIZE * scale

            # Draw grid lines
            grid_color = (128, 128, 128)  # Gray

            for i in range(1, self.TILE_SIZE):
                pos = i * scale
                # Vertical lines
                draw.line([(pos, 0), (pos, size)], fill=grid_color, width=1)
                # Horizontal lines
                draw.line([(0, pos), (size, pos)], fill=grid_color, width=1)

        # Security: Validate output path
        validate_output_path(output_path, allow_overwrite=True)

        try:
            img.save(output_path)
        except IOError as e:
            raise IOError(f"Failed to save tile preview: {e}")
