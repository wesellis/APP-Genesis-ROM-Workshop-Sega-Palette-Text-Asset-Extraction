#!/usr/bin/env python3
"""
Example: Hex Editing and ROM Comparison

This example demonstrates how to:
1. View ROM data in hex format
2. Search for byte patterns
3. Compare two ROMs
4. Create patch files
"""

from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.hex_editor import HexEditor


def view_hex_data(rom_path: str, offset: int = 0x100, length: int = 256):
    """Display ROM data in hex format."""
    print(f"Hex view of: {rom_path}")
    print(f"Offset: 0x{offset:X}, Length: {length} bytes")
    print("=" * 80)

    editor = HexEditor()

    try:
        lines = editor.view_hex(rom_path, offset=offset, length=length)
        for line in lines:
            print(line)

    except Exception as e:
        print(f"❌ Error: {e}")


def search_for_pattern(rom_path: str, pattern_hex: str):
    """Search for a byte pattern in ROM."""
    print(f"Searching for pattern: {pattern_hex}")
    print("=" * 60)

    # Convert hex string to bytes
    pattern = bytes.fromhex(pattern_hex.replace(" ", ""))

    editor = HexEditor()

    try:
        matches = editor.search_bytes(rom_path, pattern)

        if matches:
            print(f"✅ Found {len(matches)} matches:")
            for i, offset in enumerate(matches[:10]):  # Show first 10
                print(f"   {i+1}. 0x{offset:08X}")
            if len(matches) > 10:
                print(f"   ... and {len(matches) - 10} more")
        else:
            print("❌ Pattern not found")

    except Exception as e:
        print(f"❌ Error: {e}")


def compare_roms_example(rom1_path: str, rom2_path: str):
    """Compare two ROMs and show differences."""
    print(f"Comparing ROMs:")
    print(f"  ROM 1: {rom1_path}")
    print(f"  ROM 2: {rom2_path}")
    print("=" * 60)

    editor = HexEditor()

    try:
        differences = editor.compare_roms(rom1_path, rom2_path)

        if differences:
            print(f"✅ Found {len(differences)} differences\n")

            # Show first 20 differences
            for diff in differences[:20]:
                offset = diff['offset']
                byte1 = diff['rom1_byte']
                byte2 = diff['rom2_byte']
                print(f"0x{offset:08X}: {byte1} → {byte2}")

            if len(differences) > 20:
                print(f"\n... and {len(differences) - 20} more differences")
        else:
            print("✅ ROMs are identical")

    except Exception as e:
        print(f"❌ Error: {e}")


def create_patch_file_example(original_path: str, modified_path: str):
    """Create a patch file showing ROM modifications."""
    editor = HexEditor()

    try:
        patch_path = editor.create_patch(
            original_path,
            modified_path,
            output_path="workspace/rom_changes.patch.json"
        )

        print(f"✅ Created patch file: {patch_path}")
        print("   This file documents all changes made to the ROM")

    except Exception as e:
        print(f"❌ Error: {e}")


def write_bytes_example(rom_path: str):
    """Example: Write custom bytes to ROM."""
    editor = HexEditor()

    try:
        # Write "HELLO" at offset 0x1000
        custom_data = b"HELLO"

        output_path = editor.write_bytes(
            rom_path,
            offset=0x1000,
            data=custom_data,
            output_path="workspace/custom_bytes.bin"
        )

        if output_path:
            print(f"✅ Wrote {len(custom_data)} bytes at offset 0x1000")
            print(f"   Output: {output_path}")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("Genesis ROM Workshop - Hex Editing Examples")
    print("=" * 60)
    print()

    if len(sys.argv) < 2:
        print("Usage: python example_hex_editing.py <path_to_rom.bin> [command]")
        print()
        print("Commands:")
        print("  view         - View hex data (default)")
        print("  search       - Search for byte pattern")
        print("  compare ROM2 - Compare with another ROM")
        print()
        sys.exit(1)

    rom_path = sys.argv[1]
    Path("workspace").mkdir(exist_ok=True)

    # Example 1: View hex data
    print("\n🔍 Example 1: View Hex Data (ROM Header)")
    print("-" * 60)
    view_hex_data(rom_path, offset=0x100, length=256)

    # Example 2: Search for SEGA signature
    print("\n\n🔎 Example 2: Search for 'SEGA' Signature")
    print("-" * 60)
    search_for_pattern(rom_path, "53 45 47 41")  # "SEGA" in hex

    # Example 3: Write custom bytes
    print("\n\n✏️  Example 3: Write Custom Bytes")
    print("-" * 60)
    write_bytes_example(rom_path)
