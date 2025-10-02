#!/usr/bin/env python3
"""
Test script for new graphics rendering features.
"""

import os
import sys
import tempfile
from pathlib import Path


def create_test_palette():
    """Create a simple test palette."""
    # Grayscale gradient palette
    palette = []
    for i in range(16):
        gray = int((i / 15) * 255)
        palette.append((gray, gray, gray))
    return palette


def create_test_tile():
    """Create a test tile with a simple pattern."""
    # Create a checkerboard pattern in 4-bit planar format
    tile_data = bytearray(32)  # 32 bytes per tile

    # Simple pattern: alternating pixels
    # Row 0-7, each row has 4 bytes (4 bitplanes)
    for row in range(8):
        offset = row * 4
        # Create checkerboard: alternate between color 0 and color 15
        if row % 2 == 0:
            tile_data[offset + 3] = 0b10101010  # Bitplane 3 (MSB)
            tile_data[offset + 2] = 0b10101010  # Bitplane 2
            tile_data[offset + 1] = 0b10101010  # Bitplane 1
            tile_data[offset + 0] = 0b10101010  # Bitplane 0 (LSB)
        else:
            tile_data[offset + 3] = 0b01010101
            tile_data[offset + 2] = 0b01010101
            tile_data[offset + 1] = 0b01010101
            tile_data[offset + 0] = 0b01010101

    return bytes(tile_data)


def test_graphics_renderer():
    """Test GraphicsRenderer class."""
    print("Testing GraphicsRenderer...")

    try:
        from tools.graphics_renderer import GraphicsRenderer
    except ImportError as e:
        print(f"❌ Failed to import GraphicsRenderer: {e}")
        return False

    try:
        renderer = GraphicsRenderer()
        print("✅ GraphicsRenderer initialized")
    except ImportError:
        print("⚠️  Pillow not installed - install with: pip install Pillow")
        return False

    # Test tile decoding
    test_tile = create_test_tile()
    test_palette = create_test_palette()

    try:
        pixels = renderer.decode_tile_planar(test_tile)
        print(f"✅ Decoded tile: {len(pixels)}x{len(pixels[0])} pixels")
    except Exception as e:
        print(f"❌ Tile decoding failed: {e}")
        return False

    # Test rendering
    try:
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tf:
            output_path = tf.name

        renderer.render_tile_to_file(test_tile, test_palette, output_path, scale=4)

        if os.path.exists(output_path):
            size = os.path.getsize(output_path)
            print(f"✅ Rendered tile to PNG: {size} bytes")
            os.unlink(output_path)
        else:
            print("❌ PNG file not created")
            return False

    except Exception as e:
        print(f"❌ Tile rendering failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Test tile sheet
    try:
        tiles = [create_test_tile() for _ in range(16)]

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tf:
            sheet_path = tf.name

        renderer.render_tile_sheet_to_file(tiles, test_palette, sheet_path)

        if os.path.exists(sheet_path):
            size = os.path.getsize(sheet_path)
            print(f"✅ Rendered tile sheet: {size} bytes")
            os.unlink(sheet_path)
        else:
            print("❌ Tile sheet not created")
            return False

    except Exception as e:
        print(f"❌ Tile sheet rendering failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    print("✅ All GraphicsRenderer tests passed!\n")
    return True


def test_palette_preview():
    """Test palette preview export."""
    print("Testing Palette Preview...")

    try:
        from tools.palette_editor import PaletteEditor
    except ImportError as e:
        print(f"❌ Failed to import PaletteEditor: {e}")
        return False

    try:
        editor = PaletteEditor()
        test_palette = create_test_palette()

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tf:
            output_path = tf.name

        editor.export_palette_as_image(test_palette, output_path, scale=20)

        if os.path.exists(output_path):
            size = os.path.getsize(output_path)
            print(f"✅ Palette preview created: {size} bytes")
            os.unlink(output_path)
        else:
            print("❌ Palette preview not created")
            return False

    except ImportError:
        print("⚠️  Pillow not installed - install with: pip install Pillow")
        return False
    except Exception as e:
        print(f"❌ Palette preview failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    print("✅ Palette preview test passed!\n")
    return True


def test_asset_extractor_integration():
    """Test AssetExtractor with graphics rendering."""
    print("Testing AssetExtractor Integration...")

    try:
        from tools.asset_extractor import AssetExtractor
    except ImportError as e:
        print(f"❌ Failed to import AssetExtractor: {e}")
        return False

    try:
        extractor = AssetExtractor()

        if not extractor.rendering_enabled:
            print("⚠️  Graphics rendering not enabled (Pillow not installed)")
            return False

        print("✅ AssetExtractor has rendering enabled")

    except Exception as e:
        print(f"❌ AssetExtractor initialization failed: {e}")
        return False

    print("✅ AssetExtractor integration test passed!\n")
    return True


def main():
    """Run all graphics tests."""
    print("=" * 60)
    print("Graphics Rendering - Test Suite")
    print("=" * 60)
    print()

    results = []

    # Test 1: GraphicsRenderer
    results.append(("GraphicsRenderer", test_graphics_renderer()))

    # Test 2: Palette Preview
    results.append(("Palette Preview", test_palette_preview()))

    # Test 3: AssetExtractor Integration
    results.append(("AssetExtractor Integration", test_asset_extractor_integration()))

    # Summary
    print("=" * 60)
    print("GRAPHICS TEST SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name:30s} {status}")

    print("=" * 60)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)

    if passed == total:
        print("\n🎉 All graphics tests passed!")
        print("\n✨ NEW FEATURES WORKING:")
        print("  ✅ Palette preview images")
        print("  ✅ Tile rendering to PNG")
        print("  ✅ Tile sheet creation")
        print("  ✅ 4-bit planar decoding")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        if any("Pillow not installed" in str(results) for results in results):
            print("\n💡 Tip: Install Pillow with: pip install Pillow")
        return 1


if __name__ == "__main__":
    sys.exit(main())
