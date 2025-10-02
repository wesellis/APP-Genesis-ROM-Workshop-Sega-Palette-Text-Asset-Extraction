# Genesis ROM Workshop - ROM Analyzer
# Analyze ROM structure and contents
import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional


@dataclass
class ROMInfo:
    name: str
    region: str
    size: int
    checksum: str
    rom_type: str
    header_valid: bool
    charset: str = "unknown"


class ROMAnalyzer:
    """Comprehensive ROM analysis and structure detection"""

    def __init__(self):
        self.genesis_regions = {
            "U": "USA",
            "J": "JAPAN",
            "E": "EUROPE",
            "W": "WORLDWIDE",
        }

    def analyze_rom_structure(self, rom_path: str) -> ROMInfo:
        """Comprehensive ROM analysis"""
        with open(rom_path, "rb") as f:
            rom_data = f.read()

        # Handle different ROM formats
        if rom_path.lower().endswith(".smd"):
            rom_data = self._deinterleave_smd_format(rom_data)

        # Extract header information
        rom_info = self._extract_header_info(rom_data)
        rom_info.size = len(rom_data)
        rom_info.checksum = hashlib.md5(rom_data).hexdigest()[:8]
        rom_info.rom_type = Path(rom_path).suffix.lower()

        return rom_info

    def _extract_header_info(self, rom_data: bytes) -> ROMInfo:
        """Extract game information from ROM header"""
        if len(rom_data) < 0x200:
            return ROMInfo("UNKNOWN", "UNKNOWN", 0, "", "", False)

        # Check for valid Genesis header
        header_valid = False
        console_name = rom_data[0x100:0x110]
        if console_name in [b"SEGA MEGA DRIVE ", b"SEGA GENESIS    "]:
            header_valid = True

        # Extract game name (0x120-0x14F)
        try:
            name_bytes = rom_data[0x120:0x150]
            game_name = name_bytes.decode("ascii", errors="ignore").strip("\x00 ")
            game_name = " ".join(game_name.split())
        except:
            game_name = "UNKNOWN GAME"

        # Extract region (0x1F0)
        region = "UNKNOWN"
        if len(rom_data) > 0x1F0:
            region_byte = rom_data[0x1F0:0x1F3]
            region_str = region_byte.decode("ascii", errors="ignore")
            for code, name in self.genesis_regions.items():
                if code in region_str:
                    region = name
                    break

        return ROMInfo(game_name, region, 0, "", "", header_valid)

    def _deinterleave_smd_format(self, data: bytes) -> bytes:
        """Convert .smd format (interleaved) to standard format"""
        if len(data) < 512:
            return data

        # Skip SMD header if present
        if data[:16] == b"\x03\x00" + b"\x00" * 14 or data[8:10] == b"\xAA\xBB":
            data = data[512:]

        if len(data) % 16384 != 0:
            return data

        deinterleaved = bytearray(len(data))
        block_size = 16384

        for block in range(0, len(data), block_size):
            for i in range(8192):
                # Odd bytes in first half
                deinterleaved[block + i * 2 + 1] = data[block + i]
                # Even bytes in second half
                deinterleaved[block + i * 2] = data[block + 8192 + i]

        return bytes(deinterleaved)

    def get_rom_statistics(self, rom_path: str) -> Dict:
        """Get detailed statistics about ROM contents"""
        with open(rom_path, "rb") as f:
            rom_data = f.read()

        stats = {
            "total_size": len(rom_data),
            "null_bytes": rom_data.count(b"\x00"),
            "ff_bytes": rom_data.count(b"\xFF"),
            "unique_bytes": len(set(rom_data)),
            "entropy": self._calculate_entropy(rom_data),
        }

        return stats

    def _calculate_entropy(self, data: bytes) -> float:
        """Calculate Shannon entropy of data"""
        if not data:
            return 0.0

        import math

        byte_counts = [0] * 256
        for byte in data:
            byte_counts[byte] += 1

        entropy = 0.0
        data_len = len(data)

        for count in byte_counts:
            if count > 0:
                probability = count / data_len
                entropy -= probability * math.log2(probability)

        return entropy

    def find_header_offset(self, rom_path: str) -> Optional[int]:
        """Find the Genesis header in the ROM"""
        with open(rom_path, "rb") as f:
            rom_data = f.read()

        # Standard header location
        if len(rom_data) >= 0x200:
            console_name = rom_data[0x100:0x110]
            if console_name in [b"SEGA MEGA DRIVE ", b"SEGA GENESIS    "]:
                return 0x100

        # Search for header if not at standard location
        search_patterns = [b"SEGA MEGA DRIVE ", b"SEGA GENESIS    "]

        for pattern in search_patterns:
            offset = rom_data.find(pattern)
            if offset != -1:
                return offset

        return None

    def validate_checksum(self, rom_path: str) -> Dict:
        """Validate ROM checksum"""
        with open(rom_path, "rb") as f:
            rom_data = f.read()

        if len(rom_data) < 0x200:
            return {"valid": False, "reason": "ROM too small"}

        # Genesis checksum is at 0x18E-0x18F (big-endian)
        stored_checksum = int.from_bytes(rom_data[0x18E:0x190], "big")

        # Calculate checksum (sum of all bytes from 0x200 onwards)
        calculated = sum(rom_data[0x200:]) & 0xFFFF

        return {
            "valid": stored_checksum == calculated,
            "stored": f"0x{stored_checksum:04X}",
            "calculated": f"0x{calculated:04X}",
        }
