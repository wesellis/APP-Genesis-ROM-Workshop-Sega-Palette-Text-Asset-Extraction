# GHIDRA Configuration for RKA Project

## Installation Setup

### Required Components
1. **GHIDRA 10.0+** from NSA releases
2. **Sega Genesis Loader Plugin** by Dr. Mefisto (lab313ru)
   - Repository: https://github.com/lab313ru/ghidra_sega_ldr
3. **68000 Processor Module** (included with GHIDRA)

### Plugin Installation
```bash
# Download Sega loader plugin
git clone https://github.com/lab313ru/ghidra_sega_ldr.git

# Copy to GHIDRA Extensions directory
cp ghidra_sega_ldr/SegaLoader.jar $GHIDRA_HOME/Extensions/Ghidra/

# Restart GHIDRA and enable plugin in File > Install Extensions
```

## Project Configuration

### Memory Map Settings
```
ROM:     0x000000 - 0x0FFFFF (1MB) [RX]
RAM:     0xFF0000 - 0xFFFFFF (64KB) [RWX]
VDP:     0xC00000 - 0xC0001F [RW] 
I/O:     0xA10000 - 0xA1001F [RW]
Z80:     0xA00000 - 0xA0FFFF [RW]
```

### Processor Settings
- **Language**: 68000 (Motorola)
- **Endian**: Big Endian
- **Address Size**: 24-bit
- **Default Pointer Size**: 32-bit

### Analysis Options
```
Enable: 
- Constant Reference Analyzer
- Function Start Analyzer  
- Subroutine References
- Stack Analysis
- Data Reference Analysis

Disable:
- Windows x86 PE Analyzer
- ELF Analyzer
- (platform-specific analyzers)
```

## RKA-Specific Setup

### Entry Points
```
Reset Vector:     Read from 0x000004
Main Entry:       Typically 0x000200
VBlank Handler:   Auto-detected by analysis
HBlank Handler:   Auto-detected by analysis
```

### Function Signatures
```c
// Common Genesis function patterns
void vdp_write_register(uint8_t reg, uint8_t value);
void dma_transfer(uint32_t source, uint16_t dest, uint16_t length);
void load_palette(uint16_t *palette_data, uint8_t palette_num);
```

### Custom Data Types
```c
// Genesis-specific structures
typedef struct {
    uint16_t pattern_index : 11;
    uint16_t h_flip : 1;
    uint16_t v_flip : 1; 
    uint16_t palette : 2;
    uint16_t priority : 1;
} name_table_entry_t;

typedef struct {
    uint16_t y_pos;
    uint16_t size_link;
    uint16_t pattern_flags;
    uint16_t x_pos;
} sprite_entry_t;
```

## Workflow Integration

### Script Locations
- **Auto-analysis scripts**: tools/ghidra-scripts/
- **Export utilities**: tools/ghidra-scripts/export/
- **Symbol management**: tools/ghidra-scripts/symbols/

### Recommended Workflow
1. Import ROM with Sega loader
2. Run auto-analysis with custom settings
3. Apply PC trace data for function boundaries
4. Export symbol tables for m68k-disasm
5. Generate cross-reference documentation

---

**Credits**:
- **Dr. Mefisto (lab313ru)**: GHIDRA Sega loader plugin
- **NSA**: GHIDRA reverse engineering framework
- **GHIDRA community**: 68000 processor support

**Note**: Keep GHIDRA and plugins updated for best compatibility.
