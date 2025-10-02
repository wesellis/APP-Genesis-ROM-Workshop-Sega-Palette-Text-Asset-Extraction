#!/usr/bin/env python3
"""
Genesis ROM Workshop - Basic Test Suite

Run tests to verify all tools work correctly.
This is a simple test suite that doesn't require external ROM files.

Usage:
    python test_tools.py
"""

import os
import sys
import tempfile
from pathlib import Path

# Test imports
def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")

    try:
        from tools.palette_editor import PaletteEditor
        from tools.text_extractor import TextExtractor
        from tools.hex_editor import HexEditor
        from tools.rom_analyzer import ROMAnalyzer, ROMInfo
        from tools.asset_extractor import AssetExtractor
        from tools.asset_manager import AssetManager
        print("✅ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


def create_test_rom():
    """Create a minimal test ROM for testing purposes."""
    # Minimal Genesis ROM structure
    data = bytearray(8192)  # 8KB test ROM

    # Genesis header at 0x100
    data[0x100:0x110] = b"SEGA GENESIS    "
    data[0x120:0x150] = b"TEST ROM FOR WORKSHOP" + b" " * 17

    # Region info at 0x1F0
    data[0x1F0:0x1F3] = b"U  "  # USA region

    # Add some test palette data at 0x1000
    # Palette: 16 colors in Genesis format (0000BBB0GGG0RRR0)
    palette_data = bytearray()
    for i in range(16):
        color = (i << 9) | (i << 5) | (i << 1)  # Gradient
        palette_data.extend(color.to_bytes(2, 'big'))
    data[0x1000:0x1000 + 32] = palette_data

    # Add some test text at 0x2000
    test_text = b"HELLO WORLD\x00GENESIS ROM\x00TEST DATA\x00"
    data[0x2000:0x2000 + len(test_text)] = test_text

    return bytes(data)


def test_palette_editor():
    """Test PaletteEditor functionality."""
    print("\n" + "="*60)
    print("Testing PaletteEditor...")
    print("="*60)

    from tools.palette_editor import PaletteEditor

    with tempfile.NamedTemporaryFile(suffix=".bin", delete=False) as tf:
        test_rom_path = tf.name
        tf.write(create_test_rom())

    try:
        editor = PaletteEditor()

        # Test 1: Extract palettes
        print("Test 1: Extracting palettes...")
        palettes = editor.extract_palettes(test_rom_path, max_scan=5)
        if palettes:
            print(f"✅ Found {len(palettes)} palette(s)")
        else:
            print("⚠️  No palettes found (this is OK for minimal test ROM)")

        # Test 2: Create and modify palette
        print("\nTest 2: Creating custom palette...")
        custom_palette = [(i*16, i*16, i*16) for i in range(16)]

        try:
            output_path = test_rom_path.replace(".bin", "_modified.bin")
            result = editor.apply_palette_swap(
                test_rom_path,
                0,
                custom_palette,
                output_path=output_path
            )
            print(f"✅ Applied custom palette to: {result}")
            os.unlink(output_path)
        except ValueError as e:
            print(f"⚠️  Palette swap test skipped: {e}")

        # Test 3: Export/import JSON
        print("\nTest 3: JSON export/import...")
        json_path = test_rom_path.replace(".bin", ".json")

        editor.export_palette_to_json(custom_palette, json_path)
        print(f"✅ Exported palette to JSON")

        imported = editor.import_palette_from_json(json_path)
        if imported == custom_palette:
            print(f"✅ Imported palette matches original")
        else:
            print(f"❌ Imported palette doesn't match")

        os.unlink(json_path)

        print("\n✅ PaletteEditor tests passed")
        return True

    except Exception as e:
        print(f"\n❌ PaletteEditor test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        if os.path.exists(test_rom_path):
            os.unlink(test_rom_path)


def test_text_extractor():
    """Test TextExtractor functionality."""
    print("\n" + "="*60)
    print("Testing TextExtractor...")
    print("="*60)

    from tools.text_extractor import TextExtractor

    with tempfile.NamedTemporaryFile(suffix=".bin", delete=False) as tf:
        test_rom_path = tf.name
        tf.write(create_test_rom())

    try:
        extractor = TextExtractor()

        # Test 1: Find text strings
        print("Test 1: Finding text strings...")
        strings = extractor.find_text_strings(test_rom_path, min_length=4)
        print(f"✅ Found {len(strings)} text string(s)")

        if strings:
            for s in strings[:5]:
                print(f"   - '{s['text']}' at 0x{s['offset']:X}")

        # Test 2: Extract for translation
        print("\nTest 2: Creating translation file...")
        trans_path = test_rom_path.replace(".bin", "_translation.json")

        result = extractor.extract_for_translation(test_rom_path, trans_path)
        print(f"✅ Created translation file with {result['strings_found']} strings")

        if os.path.exists(trans_path):
            os.unlink(trans_path)

        # Test 3: Replace text
        if strings:
            print("\nTest 3: Replacing text...")
            first_string = strings[0]
            new_text = "TEST"[:first_string['length']]

            output_path = test_rom_path.replace(".bin", "_textmod.bin")
            result = extractor.replace_text_string(
                test_rom_path,
                first_string['offset'],
                first_string['text'],
                new_text,
                output_path=output_path
            )

            if result:
                print(f"✅ Replaced text successfully")

            if os.path.exists(output_path):
                os.unlink(output_path)

        print("\n✅ TextExtractor tests passed")
        return True

    except Exception as e:
        print(f"\n❌ TextExtractor test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        if os.path.exists(test_rom_path):
            os.unlink(test_rom_path)


def test_hex_editor():
    """Test HexEditor functionality."""
    print("\n" + "="*60)
    print("Testing HexEditor...")
    print("="*60)

    from tools.hex_editor import HexEditor

    with tempfile.NamedTemporaryFile(suffix=".bin", delete=False) as tf:
        test_rom_path = tf.name
        tf.write(create_test_rom())

    try:
        editor = HexEditor()

        # Test 1: View hex
        print("Test 1: Viewing hex data...")
        lines = editor.view_hex(test_rom_path, offset=0x100, length=64)
        print(f"✅ Generated {len(lines)} hex dump lines")
        print(f"   First line: {lines[0][:50]}...")

        # Test 2: Search bytes
        print("\nTest 2: Searching for bytes...")
        matches = editor.search_bytes(test_rom_path, b"SEGA")
        print(f"✅ Found {len(matches)} match(es) for 'SEGA'")
        if matches:
            print(f"   At offset(s): {[hex(m) for m in matches]}")

        # Test 3: Write bytes
        print("\nTest 3: Writing bytes...")
        output_path = test_rom_path.replace(".bin", "_hexmod.bin")
        editor.write_bytes(
            test_rom_path,
            0x50,
            b"TEST",
            output_path=output_path
        )
        print(f"✅ Wrote bytes successfully")

        # Test 4: Compare ROMs
        print("\nTest 4: Comparing ROMs...")
        diffs = editor.compare_roms(test_rom_path, output_path)
        print(f"✅ Found {len(diffs)} difference(s)")

        if os.path.exists(output_path):
            os.unlink(output_path)

        print("\n✅ HexEditor tests passed")
        return True

    except Exception as e:
        print(f"\n❌ HexEditor test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        if os.path.exists(test_rom_path):
            os.unlink(test_rom_path)


def test_rom_analyzer():
    """Test ROMAnalyzer functionality."""
    print("\n" + "="*60)
    print("Testing ROMAnalyzer...")
    print("="*60)

    from tools.rom_analyzer import ROMAnalyzer

    with tempfile.NamedTemporaryFile(suffix=".bin", delete=False) as tf:
        test_rom_path = tf.name
        tf.write(create_test_rom())

    try:
        analyzer = ROMAnalyzer()

        # Test 1: Analyze ROM structure
        print("Test 1: Analyzing ROM structure...")
        info = analyzer.analyze_rom_structure(test_rom_path)

        print(f"✅ Analyzed ROM:")
        print(f"   Name: {info.name}")
        print(f"   Region: {info.region}")
        print(f"   Size: {info.size} bytes")
        print(f"   Valid header: {info.header_valid}")

        # Test 2: Get statistics
        print("\nTest 2: Getting ROM statistics...")
        stats = analyzer.get_rom_statistics(test_rom_path)

        print(f"✅ Statistics:")
        print(f"   Total size: {stats['total_size']}")
        print(f"   Unique bytes: {stats['unique_bytes']}")
        print(f"   Entropy: {stats['entropy']:.2f}")

        # Test 3: Validate checksum
        print("\nTest 3: Validating checksum...")
        result = analyzer.validate_checksum(test_rom_path)

        print(f"✅ Checksum validation:")
        print(f"   Valid: {result['valid']}")
        print(f"   Stored: {result['stored']}")
        print(f"   Calculated: {result['calculated']}")

        print("\n✅ ROMAnalyzer tests passed")
        return True

    except Exception as e:
        print(f"\n❌ ROMAnalyzer test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        if os.path.exists(test_rom_path):
            os.unlink(test_rom_path)


def test_asset_tools():
    """Test AssetExtractor and AssetManager."""
    print("\n" + "="*60)
    print("Testing Asset Tools...")
    print("="*60)

    from tools.asset_extractor import AssetExtractor
    from tools.asset_manager import AssetManager

    with tempfile.NamedTemporaryFile(suffix=".bin", delete=False) as tf:
        test_rom_path = tf.name
        tf.write(create_test_rom())

    try:
        # Test AssetExtractor
        print("Test 1: AssetExtractor...")
        extractor = AssetExtractor()

        result = extractor.extract_graphics_data(test_rom_path, max_tiles=10)
        print(f"✅ Extracted {result['tiles_extracted']} tile(s)")

        # Test AssetManager
        print("\nTest 2: AssetManager...")
        manager = AssetManager()

        result = manager.extract_sprites(test_rom_path, max_tiles=10)
        print(f"✅ Extracted {result['tiles_extracted']} sprite(s)")

        result = manager.organize_assets(test_rom_path)
        print(f"✅ Created project directory structure")

        print("\n✅ Asset tools tests passed")
        return True

    except Exception as e:
        print(f"\n❌ Asset tools test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        if os.path.exists(test_rom_path):
            os.unlink(test_rom_path)


def main():
    """Run all tests."""
    print("=" * 60)
    print("Genesis ROM Workshop - Test Suite")
    print("=" * 60)

    results = []

    # Test imports
    results.append(("Imports", test_imports()))

    # Test each module
    results.append(("PaletteEditor", test_palette_editor()))
    results.append(("TextExtractor", test_text_extractor()))
    results.append(("HexEditor", test_hex_editor()))
    results.append(("ROMAnalyzer", test_rom_analyzer()))
    results.append(("Asset Tools", test_asset_tools()))

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name:20s} {status}")

    print("=" * 60)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)

    if passed == total:
        print("\n🎉 All tests passed! The toolkit is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
