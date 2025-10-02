#!/usr/bin/env python3
"""
Example: Text Extraction and Translation

This example demonstrates how to:
1. Extract text strings from a Genesis ROM
2. Create a translation file
3. Modify translations
4. Apply translations back to the ROM
"""

from pathlib import Path
import sys
import json

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.text_extractor import TextExtractor


def extract_text_from_rom(rom_path: str):
    """Extract all text strings from a ROM."""
    print(f"Extracting text from: {rom_path}")
    print("=" * 60)

    extractor = TextExtractor()

    try:
        strings = extractor.find_text_strings(rom_path, min_length=4)
        print(f"✅ Found {len(strings)} text strings\n")

        # Display first 20 strings
        for i, string_info in enumerate(strings[:20]):
            offset_hex = f"0x{string_info['offset']:X}"
            text = string_info['text'][:50]  # Limit display length
            print(f"{i:3d}. [{offset_hex:8s}] {text}")

        if len(strings) > 20:
            print(f"\n... and {len(strings) - 20} more strings")

        return strings

    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def create_translation_file(rom_path: str):
    """Create a translation file for manual editing."""
    extractor = TextExtractor()

    try:
        result = extractor.extract_for_translation(
            rom_path,
            output_path="workspace/translation.json"
        )

        print(f"✅ Created translation file: {result['output_file']}")
        print(f"   Found {result['strings_found']} strings")
        print("\n   Next steps:")
        print("   1. Open translation.json in a text editor")
        print("   2. Fill in the 'translation' field for each string")
        print("   3. Run apply_translation_example to patch the ROM")

    except Exception as e:
        print(f"❌ Error: {e}")


def apply_translation_example(rom_path: str, translation_file: str):
    """Apply translations from a file to the ROM."""
    extractor = TextExtractor()

    try:
        result = extractor.apply_translation_file(
            rom_path,
            translation_file,
            output_path="workspace/translated_rom.bin"
        )

        print(f"✅ Created translated ROM: {result['output_file']}")
        print(f"   Applied: {result['applied']} translations")
        print(f"   Skipped: {result['skipped']} translations")
        print(f"   Total: {result['total']} strings")

    except Exception as e:
        print(f"❌ Error: {e}")


def replace_single_string_example(rom_path: str):
    """Example: Replace a single text string in the ROM."""
    extractor = TextExtractor()

    try:
        # Find all strings first
        strings = extractor.find_text_strings(rom_path)

        if not strings:
            print("No text strings found")
            return

        # Show first string
        first_string = strings[0]
        print(f"First string found: '{first_string['text']}'")
        print(f"At offset: 0x{first_string['offset']:X}")

        # Replace it (example: change to uppercase)
        new_text = first_string['text'].upper()[:first_string['length']]

        result = extractor.replace_text_string(
            rom_path,
            offset=first_string['offset'],
            old_text=first_string['text'],
            new_text=new_text,
            output_path="workspace/modified_text.bin"
        )

        if result:
            print(f"✅ Replaced '{first_string['text']}' with '{new_text}'")
            print(f"   Output: workspace/modified_text.bin")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("Genesis ROM Workshop - Text Extraction Examples")
    print("=" * 60)
    print()

    if len(sys.argv) < 2:
        print("Usage: python example_text_extraction.py <path_to_rom.bin>")
        print()
        print("Examples:")
        print("  python example_text_extraction.py game.bin")
        print()
        sys.exit(1)

    rom_path = sys.argv[1]
    Path("workspace").mkdir(exist_ok=True)

    # Example 1: Extract text strings
    print("\n📝 Example 1: Extract Text Strings")
    print("-" * 60)
    strings = extract_text_from_rom(rom_path)

    if strings:
        # Example 2: Create translation file
        print("\n🌍 Example 2: Create Translation File")
        print("-" * 60)
        create_translation_file(rom_path)

        # Example 3: Replace single string
        print("\n✏️  Example 3: Replace Single String")
        print("-" * 60)
        replace_single_string_example(rom_path)
