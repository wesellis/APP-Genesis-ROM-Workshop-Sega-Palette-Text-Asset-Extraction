# Genesis ROM Workshop - Asset Extractor
# Extract graphics and audio assets from ROMs
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Import graphics renderer
sys.path.insert(0, str(Path(__file__).parent.parent))
try:
    from graphics_renderer import GraphicsRenderer
    GRAPHICS_AVAILABLE = True
except ImportError:
    GRAPHICS_AVAILABLE = False


class AssetExtractor:
    """Extract graphics, audio, and other assets from ROMs"""

    def __init__(self):
        self.output_dir = Path("workspace/exports")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize graphics renderer if available
        if GRAPHICS_AVAILABLE:
            try:
                self.renderer = GraphicsRenderer()
                self.rendering_enabled = True
            except ImportError:
                self.rendering_enabled = False
        else:
            self.rendering_enabled = False

    def extract_graphics_data(
        self, rom_path: str, max_tiles: int = 1000
    ) -> Dict:
        """Extract potential graphics data"""
        with open(rom_path, "rb") as f:
            rom_data = f.read()

        rom_name = Path(rom_path).stem
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
                if tile_count >= max_tiles:
                    break

        return {
            "tiles_extracted": tile_count,
            "output_directory": str(graphics_dir),
            "format": "8x8_4bpp_planar",
        }

    def extract_tilemaps(self, rom_path: str) -> Dict:
        """Extract potential tilemap data"""
        with open(rom_path, "rb") as f:
            rom_data = f.read()

        rom_name = Path(rom_path).stem
        tilemap_dir = self.output_dir / f"{rom_name}_tilemaps"
        tilemap_dir.mkdir(exist_ok=True)

        # Tilemaps are usually 2-byte entries
        # Format: PCCVHTTTTTTTTTTT (Priority, Palette, VFlip, HFlip, Tile index)
        tilemap_count = 0

        for i in range(0, len(rom_data) - 128, 128):
            chunk = rom_data[i : i + 128]

            if self._looks_like_tilemap(chunk):
                tilemap_file = tilemap_dir / f"tilemap_{tilemap_count:04d}.bin"
                with open(tilemap_file, "wb") as f:
                    f.write(chunk)
                tilemap_count += 1

                if tilemap_count >= 100:
                    break

        return {
            "tilemaps_extracted": tilemap_count,
            "output_directory": str(tilemap_dir),
        }

    def extract_sprites(self, rom_path: str) -> Dict:
        """Extract sprite metadata and graphics"""
        with open(rom_path, "rb") as f:
            rom_data = f.read()

        rom_name = Path(rom_path).stem
        sprite_dir = self.output_dir / f"{rom_name}_sprites"
        sprite_dir.mkdir(exist_ok=True)

        # Genesis sprites use a specific format
        # This is a simplified extraction
        sprite_count = 0

        for i in range(0, len(rom_data) - 64, 64):
            chunk = rom_data[i : i + 64]

            if self._looks_like_sprite_data(chunk):
                sprite_file = sprite_dir / f"sprite_{sprite_count:04d}.bin"
                with open(sprite_file, "wb") as f:
                    f.write(chunk)
                sprite_count += 1

                if sprite_count >= 200:
                    break

        return {
            "sprites_extracted": sprite_count,
            "output_directory": str(sprite_dir),
        }

    def _looks_like_graphics(self, data: bytes) -> bool:
        """Heuristic to detect graphics data"""
        if len(data) != 32:
            return False

        # Check for patterns typical of 4-bit planar graphics
        non_zero_bytes = sum(1 for b in data if b != 0)
        return 8 <= non_zero_bytes <= 28  # Some variation but not random

    def _looks_like_tilemap(self, data: bytes) -> bool:
        """Heuristic to detect tilemap data"""
        if len(data) < 128:
            return False

        # Check if data looks like 2-byte tilemap entries
        valid_entries = 0
        for i in range(0, len(data), 2):
            if i + 1 < len(data):
                entry = (data[i] << 8) | data[i + 1]
                # Check if it looks like a valid tilemap entry
                # Genesis tilemap entries are typically < 0x8000 for normal tiles
                if entry < 0xFFFF:
                    valid_entries += 1

        return valid_entries > 32

    def _looks_like_sprite_data(self, data: bytes) -> bool:
        """Heuristic to detect sprite metadata"""
        if len(data) < 64:
            return False

        # Simplified check for sprite-like patterns
        # Real sprite detection would be more sophisticated
        non_zero = sum(1 for b in data if b != 0)
        return 16 <= non_zero <= 48

    def create_graphics_index(self, rom_path: str) -> str:
        """Create an index of all extracted graphics"""
        import json

        rom_name = Path(rom_path).stem
        index_path = self.output_dir / f"{rom_name}_graphics_index.json"

        graphics_info = {
            "rom": rom_path,
            "graphics": self.extract_graphics_data(rom_path),
            "tilemaps": self.extract_tilemaps(rom_path),
            "sprites": self.extract_sprites(rom_path),
        }

        with open(index_path, "w") as f:
            json.dump(graphics_info, f, indent=2)

        return str(index_path)

    def extract_and_render_graphics(
        self,
        rom_path: str,
        palette: List[Tuple[int, int, int]],
        max_tiles: int = 256,
        render_sheet: bool = True
    ) -> Dict:
        """
        Extract graphics and render to PNG images.

        Args:
            rom_path: Path to ROM file
            palette: List of 16 RGB tuples for rendering
            max_tiles: Maximum tiles to extract (default: 256)
            render_sheet: If True, create tile sheet; if False, individual tiles

        Returns:
            Dictionary with extraction results

        Raises:
            ImportError: If Pillow is not installed
            ValueError: If palette is invalid
        """
        if not self.rendering_enabled:
            raise ImportError(
                "Graphics rendering not available. Install Pillow: pip install Pillow"
            )

        with open(rom_path, "rb") as f:
            rom_data = f.read()

        rom_name = Path(rom_path).stem
        graphics_dir = self.output_dir / f"{rom_name}_rendered"
        graphics_dir.mkdir(exist_ok=True)

        # Extract tiles
        tiles = []
        for i in range(0, len(rom_data) - 32, 32):
            if len(tiles) >= max_tiles:
                break

            tile_data = rom_data[i : i + 32]
            if self._looks_like_graphics(tile_data):
                tiles.append(tile_data)

        if not tiles:
            return {
                "tiles_extracted": 0,
                "output_directory": str(graphics_dir),
                "message": "No graphics data found"
            }

        # Render tiles
        if render_sheet:
            # Create single tile sheet
            sheet_path = graphics_dir / f"{rom_name}_tilesheet.png"
            self.renderer.render_tile_sheet_to_file(
                tiles, palette, str(sheet_path), columns=16, scale=2
            )

            return {
                "tiles_extracted": len(tiles),
                "output_directory": str(graphics_dir),
                "sheet_file": str(sheet_path),
                "format": "PNG tile sheet"
            }
        else:
            # Render individual tiles
            for idx, tile_data in enumerate(tiles):
                tile_path = graphics_dir / f"tile_{idx:04d}.png"
                self.renderer.render_tile_to_file(
                    tile_data, palette, str(tile_path), scale=4
                )

            return {
                "tiles_extracted": len(tiles),
                "output_directory": str(graphics_dir),
                "format": "Individual PNG tiles"
            }

    def render_tiles_with_palette(
        self,
        rom_path: str,
        palette: List[Tuple[int, int, int]],
        output_path: str,
        offset: int = 0,
        num_tiles: int = 256
    ) -> None:
        """
        Render tiles from specific ROM offset with given palette.

        Args:
            rom_path: Path to ROM file
            palette: List of 16 RGB tuples
            output_path: Output PNG path
            offset: Starting offset in ROM (default: 0)
            num_tiles: Number of tiles to render (default: 256)

        Raises:
            ImportError: If Pillow is not installed
            ValueError: If parameters are invalid
        """
        if not self.rendering_enabled:
            raise ImportError(
                "Graphics rendering not available. Install Pillow: pip install Pillow"
            )

        with open(rom_path, "rb") as f:
            f.seek(offset)
            rom_data = f.read(num_tiles * 32)

        # Extract tiles
        tiles = []
        for i in range(0, len(rom_data), 32):
            if len(tiles) >= num_tiles:
                break
            if i + 32 <= len(rom_data):
                tiles.append(rom_data[i : i + 32])

        # Render sheet
        self.renderer.render_tile_sheet_to_file(
            tiles, palette, output_path, columns=16, scale=2
        )

    def preview_tile(
        self,
        rom_path: str,
        palette: List[Tuple[int, int, int]],
        offset: int,
        output_path: str,
        show_grid: bool = True
    ) -> None:
        """
        Create a detailed preview of a single tile.

        Args:
            rom_path: Path to ROM file
            palette: List of 16 RGB tuples
            offset: Offset of tile in ROM
            output_path: Output PNG path
            show_grid: Show pixel grid overlay (default: True)

        Raises:
            ImportError: If Pillow is not installed
            ValueError: If parameters are invalid
        """
        if not self.rendering_enabled:
            raise ImportError(
                "Graphics rendering not available. Install Pillow: pip install Pillow"
            )

        with open(rom_path, "rb") as f:
            f.seek(offset)
            tile_data = f.read(32)

        if len(tile_data) != 32:
            raise ValueError(f"Could not read tile at offset 0x{offset:X}")

        self.renderer.create_tile_preview(
            tile_data, palette, output_path,
            show_grid=show_grid, scale=8
        )
