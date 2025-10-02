# Genesis ROM Workshop - Text Extractor
# For translation projects and text modification
import json
from pathlib import Path
from typing import Dict, List


class TextExtractor:
    """Extract and modify text in Genesis ROMs"""

    def __init__(self):
        self.common_text_areas = [
            (0x10000, 0x20000),  # Common text areas in Genesis ROMs
            (0x80000, 0x100000),
            (0x120000, 0x180000),
        ]

    def find_text_strings(
        self, rom_path: str, min_length: int = 4
    ) -> List[Dict[str, any]]:
        """Find all text strings in ROM with addresses"""
        with open(rom_path, "rb") as f:
            rom_data = f.read()

        strings = []

        for start, end in self.common_text_areas:
            if start >= len(rom_data):
                continue

            search_end = min(end, len(rom_data))

            # Look for ASCII text
            current_string = ""
            string_start = start

            for i in range(start, search_end):
                byte = rom_data[i]

                if 32 <= byte <= 126:  # Printable ASCII
                    if not current_string:
                        string_start = i
                    current_string += chr(byte)
                else:
                    if len(current_string) >= min_length:
                        strings.append(
                            {
                                "text": current_string,
                                "offset": string_start,
                                "length": len(current_string),
                                "encoding": "ascii",
                            }
                        )
                    current_string = ""

        return strings

    def extract_for_translation(
        self, rom_path: str, output_path: str = None
    ) -> Dict[str, any]:
        """Export text for translation projects"""
        strings = self.find_text_strings(rom_path)

        if output_path is None:
            output_path = str(
                Path(rom_path).parent / f"{Path(rom_path).stem}_translation.json"
            )

        translation_data = {
            "rom_file": rom_path,
            "total_strings": len(strings),
            "strings": [
                {
                    "id": i,
                    "original": s["text"],
                    "translation": "",  # Empty for translator to fill
                    "offset": f"0x{s['offset']:X}",
                    "length": s["length"],
                    "encoding": s["encoding"],
                }
                for i, s in enumerate(strings)
            ],
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(translation_data, f, indent=2, ensure_ascii=False)

        return {"output_file": output_path, "strings_found": len(strings)}

    def replace_text_string(
        self, rom_path: str, offset: int, old_text: str, new_text: str, output_path: str = None
    ) -> bool:
        """Replace a text string at a specific offset"""
        if len(new_text) > len(old_text):
            raise ValueError(
                f"New text is too long ({len(new_text)} > {len(old_text)})"
            )

        with open(rom_path, "rb") as f:
            rom_data = f.read()

        modified_data = bytearray(rom_data)

        # Verify the old text is at the expected location
        old_bytes = old_text.encode("ascii")
        if modified_data[offset : offset + len(old_bytes)] != old_bytes:
            raise ValueError("Old text not found at specified offset")

        # Replace with new text, padding with nulls if necessary
        new_bytes = new_text.encode("ascii")
        modified_data[offset : offset + len(old_bytes)] = new_bytes + b"\x00" * (
            len(old_bytes) - len(new_bytes)
        )

        # Save modified ROM
        if output_path is None:
            output_path = str(
                Path(rom_path).with_stem(Path(rom_path).stem + "_translated")
            )

        with open(output_path, "wb") as f:
            f.write(modified_data)

        return True

    def apply_translation_file(
        self, rom_path: str, translation_file: str, output_path: str = None
    ) -> Dict[str, any]:
        """Apply translations from a translation file to ROM"""
        with open(translation_file, "r", encoding="utf-8") as f:
            translation_data = json.load(f)

        with open(rom_path, "rb") as f:
            rom_data = f.read()

        modified_data = bytearray(rom_data)
        applied_count = 0
        skipped_count = 0

        for string_info in translation_data["strings"]:
            if not string_info["translation"]:
                skipped_count += 1
                continue

            offset = int(string_info["offset"], 16)
            original = string_info["original"]
            translation = string_info["translation"]

            if len(translation) > len(original):
                skipped_count += 1
                continue

            # Verify original text
            old_bytes = original.encode("ascii")
            if modified_data[offset : offset + len(old_bytes)] != old_bytes:
                skipped_count += 1
                continue

            # Apply translation
            new_bytes = translation.encode("ascii")
            modified_data[offset : offset + len(old_bytes)] = new_bytes + b"\x00" * (
                len(old_bytes) - len(new_bytes)
            )
            applied_count += 1

        # Save modified ROM
        if output_path is None:
            output_path = str(
                Path(rom_path).with_stem(Path(rom_path).stem + "_translated")
            )

        with open(output_path, "wb") as f:
            f.write(modified_data)

        return {
            "output_file": output_path,
            "applied": applied_count,
            "skipped": skipped_count,
            "total": len(translation_data["strings"]),
        }
