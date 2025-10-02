#!/usr/bin/env python3
"""
Example: Palette Extraction and Modification

This example demonstrates how to:
1. Extract palettes from a Genesis ROM
2. Modify a palette
3. Export palettes to JSON for editing
4. Import modified palettes and apply them
"""

from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.palette_editor import PaletteEditor


def extract_and_display_palettes(rom_path: str):
    """Extract and display all palettes from a ROM."""
    print(f"Extracting palettes from: {rom_path}")
    print("=" * 60)

    editor = PaletteEditor()

    try:
        palettes = editor.extract_palettes(rom_path, max_scan=10)
        print(f"✅ Found {len(palettes)} palettes\n")

        # Display first 3 palettes
        for i, palette in enumerate(palettes[:3]):
            print(f"Palette {i}:")
            for j, (r, g, b) in enumerate(palette):
                hex_color = f"#{r:02X}{g:02X}{b:02X}"
                print(f"  Color {j:2d}: RGB({r:3d}, {g:3d}, {b:3d}) {hex_color}")
            print()

        return palettes

    except FileNotFoundError:
        print(f"❌ Error: ROM file not found: {rom_path}")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def export_palette_to_json_example(rom_path: str):
    """Export a palette to JSON for manual editing."""
    editor = PaletteEditor()

    try:
        palettes = editor.extract_palettes(rom_path, max_scan=5)
        if not palettes:
            print("No palettes found")
            return

        # Export first palette to JSON
        output_path = "workspace/palette_0.json"
        Path("workspace").mkdir(exist_ok=True)

        editor.export_palette_to_json(palettes[0], output_path)
        print(f"✅ Exported palette to: {output_path}")
        print("   You can now edit this JSON file to modify colors")

    except Exception as e:
        print(f"❌ Error: {e}")


def create_red_sonic_example(rom_path: str):
    """Example: Make Sonic red by swapping blue colors with red."""
    editor = PaletteEditor()

    try:
        # Extract first palette (usually Sonic's colors)
        palettes = editor.extract_palettes(rom_path, max_scan=5)
        if not palettes:
            print("No palettes found")
            return

        # Modify first palette - swap blue channel with red
        modified_palette = []
        for r, g, b in palettes[0]:
            # If color is primarily blue, make it red
            if b > r and b > g:
                modified_palette.append((b, g, r))  # Swap blue to red
            else:
                modified_palette.append((r, g, b))  # Keep original

        # Apply the modified palette
        output_rom = editor.apply_palette_swap(
            rom_path,
            palette_index=0,
            new_palette=modified_palette,
            output_path="workspace/sonic_red.bin"
        )

        print(f"✅ Created red Sonic ROM: {output_rom}")
        print("   Load this ROM in an emulator to see red Sonic!")

    except Exception as e:
        print(f"❌ Error: {e}")


def import_and_apply_json_palette(rom_path: str, json_path: str):
    """Import a palette from JSON and apply it to ROM."""
    editor = PaletteEditor()

    try:
        # Import palette from JSON
        new_palette = editor.import_palette_from_json(json_path)
        print(f"✅ Imported palette from: {json_path}")

        # Apply to ROM
        output_rom = editor.apply_palette_swap(
            rom_path,
            palette_index=0,
            new_palette=new_palette
        )

        print(f"✅ Created modified ROM: {output_rom}")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("Genesis ROM Workshop - Palette Extraction Examples")
    print("=" * 60)
    print()

    if len(sys.argv) < 2:
        print("Usage: python example_palette_extraction.py <path_to_rom.bin>")
        print()
        print("Examples:")
        print("  python example_palette_extraction.py sonic.bin")
        print()
        sys.exit(1)

    rom_path = sys.argv[1]

    # Example 1: Extract and display palettes
    print("\n📊 Example 1: Extract and Display Palettes")
    print("-" * 60)
    palettes = extract_and_display_palettes(rom_path)

    if palettes:
        # Example 2: Export to JSON
        print("\n💾 Example 2: Export Palette to JSON")
        print("-" * 60)
        export_palette_to_json_example(rom_path)

        # Example 3: Create red Sonic
        print("\n🔴 Example 3: Create Red Sonic")
        print("-" * 60)
        create_red_sonic_example(rom_path)
