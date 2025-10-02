#!/usr/bin/env python3
"""
Example: Graphics Rendering ⭐ NEW FEATURE!

This example demonstrates the NEW graphics rendering capabilities:
1. Export palette preview images
2. Extract and render graphics tiles to PNG
3. Create tile sheets
4. Preview individual tiles with grid overlay

Requirements:
    pip install Pillow
"""

from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.palette_editor import PaletteEditor
from tools.asset_extractor import AssetExtractor


def demo_palette_preview(rom_path: str):
    """Demonstrate palette preview image export."""
    print("🎨 Demo 1: Palette Preview Images")
    print("=" * 60)

    editor = PaletteEditor()

    try:
        # Extract palettes
        palettes = editor.extract_palettes(rom_path, max_scan=10)
        print(f"✅ Found {len(palettes)} palettes\n")

        if not palettes:
            print("⚠️  No palettes found")
            return

        # Export first palette as image
        output_path = "workspace/palette_preview.png"
        Path("workspace").mkdir(exist_ok=True)

        editor.export_palette_as_image(
            palettes[0],
            output_path,
            scale=20  # 20 pixels per color = 320x20 image
        )

        print(f"✅ Created palette preview: {output_path}")
        print(f"   Open this PNG to see the palette colors!")
        print()

        # Export all palettes
        if len(palettes) > 1:
            image_files = editor.export_all_palettes_as_images(
                palettes[:5],  # First 5 palettes
                "workspace/palettes",
                prefix="palette"
            )
            print(f"✅ Exported {len(image_files)} palette images to workspace/palettes/")
            print()

        return palettes

    except ImportError:
        print("❌ Pillow not installed. Run: pip install Pillow")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def demo_tile_rendering(rom_path: str, palette):
    """Demonstrate tile rendering to PNG."""
    print("\n📐 Demo 2: Tile Rendering")
    print("=" * 60)

    if not palette:
        print("⚠️  No palette available, skipping")
        return

    extractor = AssetExtractor()

    try:
        # Extract and render graphics as tile sheet
        print("Extracting and rendering graphics...")

        result = extractor.extract_and_render_graphics(
            rom_path,
            palette,  # Use first palette
            max_tiles=256,
            render_sheet=True
        )

        print(f"✅ Extracted {result['tiles_extracted']} tiles")
        print(f"✅ Created tile sheet: {result.get('sheet_file', 'N/A')}")
        print()
        print("   Open the tile sheet PNG to see actual graphics!")
        print("   This is real rendered graphics, not just raw bytes!")
        print()

    except ImportError:
        print("❌ Pillow not installed. Run: pip install Pillow")
    except Exception as e:
        print(f"❌ Error: {e}")


def demo_specific_offset_rendering(rom_path: str, palette):
    """Demonstrate rendering tiles from specific offset."""
    print("\n🎯 Demo 3: Render Specific ROM Region")
    print("=" * 60)

    if not palette:
        print("⚠️  No palette available, skipping")
        return

    extractor = AssetExtractor()

    try:
        # Render tiles from specific offset (common graphics location)
        output_path = "workspace/tiles_at_offset.png"

        print(f"Rendering tiles from offset 0x20000...")

        extractor.render_tiles_with_palette(
            rom_path,
            palette,
            output_path,
            offset=0x20000,  # Common graphics location
            num_tiles=128
        )

        print(f"✅ Created tile sheet: {output_path}")
        print(f"   128 tiles from offset 0x20000")
        print()

    except ImportError:
        print("❌ Pillow not installed. Run: pip install Pillow")
    except Exception as e:
        print(f"❌ Error: {e}")


def demo_tile_preview(rom_path: str, palette):
    """Demonstrate detailed tile preview with grid."""
    print("\n🔍 Demo 4: Detailed Tile Preview")
    print("=" * 60)

    if not palette:
        print("⚠️  No palette available, skipping")
        return

    extractor = AssetExtractor()

    try:
        # Create detailed preview of single tile
        output_path = "workspace/tile_preview_with_grid.png"

        print(f"Creating detailed preview of tile at 0x20000...")

        extractor.preview_tile(
            rom_path,
            palette,
            offset=0x20000,
            output_path=output_path,
            show_grid=True  # Show pixel grid
        )

        print(f"✅ Created tile preview: {output_path}")
        print(f"   64x64 pixel preview with grid overlay")
        print(f"   Perfect for examining individual tiles!")
        print()

    except ImportError:
        print("❌ Pillow not installed. Run: pip install Pillow")
    except Exception as e:
        print(f"❌ Error: {e}")


def demo_comparison():
    """Show before/after comparison."""
    print("\n📊 Before vs After Comparison")
    print("=" * 60)
    print()
    print("BEFORE (old version):")
    print("  ❌ Raw .bin files (unreadable)")
    print("  ❌ No visual preview")
    print("  ❌ Needs external tools to view")
    print()
    print("AFTER (new version):")
    print("  ✅ PNG images (view in any image viewer)")
    print("  ✅ Visual palette previews")
    print("  ✅ Rendered tile sheets")
    print("  ✅ Grid overlays for analysis")
    print("  ✅ Everything self-contained!")
    print()


if __name__ == "__main__":
    print("Genesis ROM Workshop - Graphics Rendering Demo")
    print("=" * 60)
    print()
    print("⭐ NEW FEATURES:")
    print("  - Palette preview images")
    print("  - Tile rendering to PNG")
    print("  - Tile sheet creation")
    print("  - Grid overlays")
    print()

    if len(sys.argv) < 2:
        print("Usage: python example_graphics_rendering.py <path_to_rom.bin>")
        print()
        print("This will:")
        print("  1. Extract palettes and save as PNG images")
        print("  2. Render graphics tiles to viewable PNG files")
        print("  3. Create tile sheets showing all graphics")
        print("  4. Create detailed previews with pixel grids")
        print()
        print("Requirements:")
        print("  pip install Pillow")
        print()
        sys.exit(1)

    rom_path = sys.argv[1]
    Path("workspace").mkdir(exist_ok=True)

    # Demo 1: Palette previews
    palettes = demo_palette_preview(rom_path)

    # Use first palette for rendering demos
    if palettes and len(palettes) > 0:
        palette = palettes[0]

        # Demo 2: Tile rendering
        demo_tile_rendering(rom_path, palette)

        # Demo 3: Specific offset
        demo_specific_offset_rendering(rom_path, palette)

        # Demo 4: Tile preview
        demo_tile_preview(rom_path, palette)

    # Show comparison
    demo_comparison()

    print("\n" + "=" * 60)
    print("✅ Demo complete! Check workspace/ directory for images")
    print("=" * 60)
    print()
    print("Output files:")
    print("  - workspace/palette_preview.png")
    print("  - workspace/palettes/palette_*.png")
    print("  - workspace/exports/*_rendered/*_tilesheet.png")
    print("  - workspace/tiles_at_offset.png")
    print("  - workspace/tile_preview_with_grid.png")
    print()
    print("🎉 These are REAL rendered graphics, not raw bytes!")
