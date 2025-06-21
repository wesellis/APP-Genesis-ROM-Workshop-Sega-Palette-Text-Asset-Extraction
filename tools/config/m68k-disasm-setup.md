# m68k-disasm Configuration for RKA

## Installation Setup

### Source and Build
```bash
# Clone Oxore's m68k-disasm
git clone https://github.com/Oxore/m68k-disasm.git
cd m68k-disasm

# Build with CMake
cmake -B build -S .
cmake --build build

# Copy to project tools
cp build/m68k-disasm ../../tools/external/
```

### Dependencies
- **CMake 3.10+**
- **C++ compiler** (GCC/Clang/MSVC)
- **Capstone library** (auto-downloaded)

## Configuration for RKA

### Command Line Usage
```bash
# Basic disassembly
./m68k-disasm -i rocket_knight_adventures.bin -o rka_disasm.asm

# With PC trace integration
./m68k-disasm -i rka.bin -o rka.asm -t pc_traces.txt --labels

# Generate symbol table
./m68k-disasm -i rka.bin -o rka.asm -t traces.txt --symbols symbols.txt
```

### Configuration File (rka-config.ini)
```ini
[input]
rom_file = rocket_knight_adventures.bin
rom_start = 0x000000
rom_size = 0x100000

[output]  
asm_file = rka_disassembly.asm
symbols_file = rka_symbols.txt
labels_file = rka_labels.txt

[analysis]
pc_trace_file = traces/rka_complete_trace.txt
entry_point = 0x000200
vector_table = 0x000000

[formatting]
use_labels = true
generate_equates = true
comment_style = semicolon
indent_size = 8
```

### PC Trace Format
```
# Format: one address per line (hex)
000200
000202  
000206
00020A
# ... continue for all executed addresses
```

## Integration with Project Workflow

### Symbol Export from GHIDRA
```python
# GHIDRA script to export symbols for m68k-disasm
# Save as tools/ghidra-scripts/export_symbols.py

from ghidra.program.model.symbol import *

def export_symbols():
    symbol_table = currentProgram.getSymbolTable()
    with open("symbols_for_m68k_disasm.txt", "w") as f:
        for symbol in symbol_table.getAllSymbols(True):
            if symbol.getSymbolType() == SymbolType.FUNCTION:
                f.write(f"{symbol.getAddress()}:{symbol.getName()}\n")
```

### Automated Workflow Script
```bash
#!/bin/bash
# tools/automation/generate_disassembly.sh

echo "🔄 Generating RKA disassembly with m68k-disasm..."

# Check for required files
if [ ! -f "rocket_knight_adventures.bin" ]; then
    echo "❌ ROM file not found!"
    exit 1
fi

if [ ! -f "traces/rka_complete_trace.txt" ]; then
    echo "❌ PC trace file not found! Run trace collection first."
    exit 1
fi

# Run disassembly
echo "⚙️  Running m68k-disasm..."
./tools/external/m68k-disasm \
    -i rocket_knight_adventures.bin \
    -o original/disassembly/rka_main.asm \
    -t traces/rka_complete_trace.txt \
    --labels \
    --symbols original/symbols/rka_symbols.txt \
    --config tools/config/rka-m68k-config.ini

echo "✅ Disassembly complete!"
echo "📁 Output files:"
echo "   - original/disassembly/rka_main.asm"
echo "   - original/symbols/rka_symbols.txt"
```

## Output Format Customization

### Assembly Style Settings
```ini
[style]
# Label format
label_suffix = :
global_label_prefix = 
local_label_prefix = .

# Instruction formatting  
mnemonic_case = lower
register_case = lower
immediate_prefix = #
address_format = $%06X

# Data formatting
byte_directive = dc.b
word_directive = dc.w  
long_directive = dc.l
```

### Comment Generation
```ini
[comments]
auto_generate = true
include_addresses = true
include_opcodes = false
vector_table_comments = true
hardware_register_comments = true
```

---

**Credits**:
- **Oxore (Vladimir Novikov)**: m68k-disasm development
- **Capstone Engine**: Disassembly framework
- **68000 community**: Processor documentation

**Note**: m68k-disasm produces assembler-compatible output that can be reassembled to identical ROM when properly configured.
