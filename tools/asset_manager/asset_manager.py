# Genesis ROM Workshop - Asset Manager
# Extract and manage game assets
from pathlib import Path
from typing import Dict


class AssetManager:
    """Professional asset extraction and management"""

    def __init__(self):
        self.output_dir = Path("workspace/exports")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def extract_sprites(self, rom_path: str, max_tiles: int = 1000) -> Dict[str, any]:
        """Extract all sprite graphics from ROM"""
        with open(rom_path, "rb") as f:
            rom_data = f.read()

        rom_name = Path(rom_path).stem
        graphics_dir = self.output_dir / f"{rom_name}_graphics"
        graphics_dir.mkdir(exist_ok=True)

        # Genesis graphics are usually 8x8 tiles, 32 bytes each (4-bit planar format)
        tile_count = 0

        for i in range(0, len(rom_data) - 32, 32):
            tile_data = rom_data[i : i + 32]

            # Heuristic: if the tile has some variation, it might be graphics
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

    def extract_audio_samples(self, rom_path: str) -> Dict[str, any]:
        """Extract audio samples and music data"""
        with open(rom_path, "rb") as f:
            rom_data = f.read()

        rom_name = Path(rom_path).stem
        audio_dir = self.output_dir / f"{rom_name}_audio"
        audio_dir.mkdir(exist_ok=True)

        # Look for YM2612 FM synthesis data and PSG data
        # This is a basic implementation - real audio extraction is complex
        sample_count = 0

        # Search for potential FM synthesis parameters
        # YM2612 register patterns (simplified detection)
        for i in range(0, len(rom_data) - 128):
            chunk = rom_data[i : i + 128]

            if self._looks_like_audio_data(chunk):
                sample_file = audio_dir / f"audio_{sample_count:04d}.bin"
                with open(sample_file, "wb") as f:
                    f.write(chunk)
                sample_count += 1

                # Limit extraction
                if sample_count >= 100:
                    break

        return {
            "samples_extracted": sample_count,
            "output_directory": str(audio_dir),
            "note": "Audio data requires specialized tools for playback",
        }

    def organize_assets(self, rom_path: str) -> Dict[str, any]:
        """Organize all extracted assets into a project structure"""
        rom_name = Path(rom_path).stem
        project_dir = self.output_dir / f"{rom_name}_project"
        project_dir.mkdir(exist_ok=True)

        # Create organized directory structure
        (project_dir / "graphics").mkdir(exist_ok=True)
        (project_dir / "audio").mkdir(exist_ok=True)
        (project_dir / "palettes").mkdir(exist_ok=True)
        (project_dir / "text").mkdir(exist_ok=True)

        return {
            "project_directory": str(project_dir),
            "directories_created": ["graphics", "audio", "palettes", "text"],
        }

    def _looks_like_graphics(self, data: bytes) -> bool:
        """Heuristic to detect graphics data"""
        if len(data) != 32:
            return False

        # Check for patterns typical of 4-bit planar graphics
        non_zero_bytes = sum(1 for b in data if b != 0)

        # Graphics usually have some variation but aren't completely random
        if non_zero_bytes < 8 or non_zero_bytes > 28:
            return False

        # Check for repeating patterns (common in tile graphics)
        return True

    def _looks_like_audio_data(self, data: bytes) -> bool:
        """Heuristic to detect potential audio/FM synthesis data"""
        if len(data) < 128:
            return False

        # Look for patterns typical of YM2612 register writes
        # This is a simplified heuristic
        register_like_values = sum(
            1 for i in range(0, len(data), 2) if data[i] < 0xB8 and data[i + 1] < 0xFF
        )

        return register_like_values > 30

    def export_asset_manifest(self, rom_path: str, output_path: str = None) -> str:
        """Create a manifest of all extracted assets"""
        import json

        rom_name = Path(rom_path).stem

        if output_path is None:
            output_path = str(self.output_dir / f"{rom_name}_manifest.json")

        manifest = {
            "rom_file": rom_path,
            "rom_name": rom_name,
            "assets": {
                "graphics": str(self.output_dir / f"{rom_name}_graphics"),
                "audio": str(self.output_dir / f"{rom_name}_audio"),
            },
        }

        with open(output_path, "w") as f:
            json.dump(manifest, f, indent=2)

        return output_path
