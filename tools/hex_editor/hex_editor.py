# Genesis ROM Workshop - Hex Editor
# View and edit ROM bytes directly
from pathlib import Path
from typing import List, Optional


class HexEditor:
    """Professional hex viewing and editing for Genesis ROMs"""

    def __init__(self):
        self.bytes_per_line = 16

    def view_hex(
        self, rom_path: str, offset: int = 0, length: int = 256
    ) -> List[str]:
        """View ROM data in hex format"""
        with open(rom_path, "rb") as f:
            f.seek(offset)
            data = f.read(length)

        lines = []
        for i in range(0, len(data), self.bytes_per_line):
            chunk = data[i : i + self.bytes_per_line]
            addr = offset + i

            # Format: ADDRESS | HEX BYTES | ASCII
            hex_part = " ".join(f"{b:02X}" for b in chunk)
            hex_part = hex_part.ljust(self.bytes_per_line * 3)

            ascii_part = "".join(
                chr(b) if 32 <= b <= 126 else "." for b in chunk
            )

            line = f"{addr:08X} | {hex_part} | {ascii_part}"
            lines.append(line)

        return lines

    def write_bytes(
        self, rom_path: str, offset: int, data: bytes, output_path: str = None
    ) -> bool:
        """Write bytes to ROM at specified offset"""
        with open(rom_path, "rb") as f:
            rom_data = f.read()

        if offset + len(data) > len(rom_data):
            raise ValueError("Write would exceed ROM size")

        modified_data = bytearray(rom_data)
        modified_data[offset : offset + len(data)] = data

        if output_path is None:
            output_path = str(
                Path(rom_path).with_stem(Path(rom_path).stem + "_hexedited")
            )

        with open(output_path, "wb") as f:
            f.write(modified_data)

        return True

    def search_bytes(self, rom_path: str, pattern: bytes) -> List[int]:
        """Search for byte pattern in ROM"""
        with open(rom_path, "rb") as f:
            rom_data = f.read()

        matches = []
        pattern_len = len(pattern)

        for i in range(len(rom_data) - pattern_len + 1):
            if rom_data[i : i + pattern_len] == pattern:
                matches.append(i)

        return matches

    def compare_roms(self, rom1_path: str, rom2_path: str) -> List[dict]:
        """Compare two ROMs and find differences"""
        with open(rom1_path, "rb") as f:
            data1 = f.read()

        with open(rom2_path, "rb") as f:
            data2 = f.read()

        differences = []
        max_len = max(len(data1), len(data2))

        for i in range(max_len):
            byte1 = data1[i] if i < len(data1) else None
            byte2 = data2[i] if i < len(data2) else None

            if byte1 != byte2:
                differences.append(
                    {
                        "offset": i,
                        "rom1_byte": f"{byte1:02X}" if byte1 is not None else "EOF",
                        "rom2_byte": f"{byte2:02X}" if byte2 is not None else "EOF",
                    }
                )

                # Limit to first 1000 differences
                if len(differences) >= 1000:
                    break

        return differences

    def create_patch(
        self, original_path: str, modified_path: str, output_path: str = None
    ) -> str:
        """Create a simple patch file showing differences"""
        import json

        differences = self.compare_roms(original_path, modified_path)

        if output_path is None:
            output_path = str(
                Path(modified_path).with_suffix(".patch.json")
            )

        patch_data = {
            "original_rom": original_path,
            "modified_rom": modified_path,
            "total_changes": len(differences),
            "changes": differences[:100],  # Limit to first 100 for readability
        }

        with open(output_path, "w") as f:
            json.dump(patch_data, f, indent=2)

        return output_path

    def dump_region(
        self, rom_path: str, start_offset: int, end_offset: int, output_path: str
    ) -> bool:
        """Dump a specific region of ROM to a file"""
        with open(rom_path, "rb") as f:
            f.seek(start_offset)
            data = f.read(end_offset - start_offset)

        with open(output_path, "wb") as f:
            f.write(data)

        return True
