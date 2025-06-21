# Master Tool Configuration and Credits

**Purpose**: Central configuration index and proper attribution for all tools  
**Date**: December 2024  
**Project**: Rocket Knight Adventures Decompilation

---

## Complete Tool Attribution

### Core Reverse Engineering Tools

#### **m68k-disasm**
- **Author**: Oxore (Vladimir Novikov)
- **License**: Unlicense (Public Domain)  
- **Repository**: https://github.com/Oxore/m68k-disasm
- **Purpose**: Motorola 68000 disassembly with PC trace support
- **Configuration**: `tools/config/m68k-disasm-setup.md`

#### **GHIDRA Sega Loader**
- **Author**: Dr. Mefisto (lab313ru)
- **License**: Apache License 2.0
- **Repository**: https://github.com/lab313ru/ghidra_sega_ldr  
- **Purpose**: GHIDRA plugin for Genesis ROM analysis
- **Configuration**: `tools/config/ghidra-setup.md`

#### **SMD IDA Tools 2**
- **Author**: Dr. Mefisto (lab313ru)
- **Repository**: https://github.com/lab313ru/smd_ida_tools2
- **Purpose**: IDA Pro plugin for Genesis debugging
- **Status**: Optional - requires IDA Pro license

### Compression and Asset Tools

#### **Genesis Compression Libraries (md-decomp)**
- **Author**: Devon Artmeier  
- **License**: Unlicense (Public Domain)
- **Repository**: https://github.com/devon-artmeier/md-decomp
- **Purpose**: Nemesis, Kosinski, Enigma decompression
- **Implementation**: `tools/compression/`

#### **RKA LZSS Decompressor**
- **Author**: Clownacy
- **Repository**: https://github.com/Clownacy/RKA-decompressor  
- **Purpose**: RKA-specific LZSS compression handling
- **Integration**: `tools/compression/rka_lzss/`

### Modern Analysis Framework

#### **LLM4Decompile**
- **Author**: albertan017
- **License**: MIT License
- **Repository**: https://github.com/albertan017/LLM4Decompile
- **Purpose**: AI-powered assembly to C conversion
- **Setup**: Requires Python, PyTorch, Transformers

#### **Python Genesis Tools**
```bash
# Core Python analysis tools
pip install bare68k              # M68K emulation and PC tracing
pip install capstone-python      # Modern disassembly framework  
pip install keystone-engine      # Assembly engine
```

#### **PyReveng3**
- **Repository**: https://github.com/bsdphk/PyReveng3
- **Purpose**: Advanced reverse engineering framework
- **Usage**: Complex pattern analysis and data structure identification

### Emulation and Testing

#### **BizHawk**
- **Team**: BizHawk Development Team
- **License**: MIT License  
- **Website**: http://tasvideos.org/Bizhawk.html
- **Purpose**: PC trace collection via automated gameplay
- **Scripts**: `tools/automation/bizhawk_scripts/`

## Technical Documentation Sources

### **Charles MacDonald's Documentation**
- **Genesis Hardware Notes v0.8**: `docs/hardware/genesis-hardware-notes.md`
- **VDP Documentation v1.5f**: `docs/hardware/genesis-vdp-reference.md`
- **Website**: http://cgfm2.emuviews.com (historical)
- **Impact**: Definitive Genesis hardware reference

### **Felipe XnaK & Volker Oth**
- **Genesis ROM Format Documentation v1.1**: `docs/formats/genesis-rom-format.md`
- **Contribution**: Complete ROM header specification and validation

### **Bart Trzynadlowski**
- **Genesis Technical Notes (Second Edition)**: `docs/technical/genesis-development-notes.md`
- **Website**: http://www.powernet.net/~trzy (historical)
- **Focus**: Practical development guidelines and gotchas

### **Community Collections**
- **GENESIS INFO archive**: Source of GENESIS.EQU and reference tools
- **Sonic Retro**: https://sonicretro.org/ - Genesis development community
- **Sega Retro**: https://segaretro.org/ - Hardware documentation wiki

---

## Configuration Quick Start

### 1. Environment Setup (Week 1)
```bash
# Clone essential tools
git clone https://github.com/Oxore/m68k-disasm.git external/m68k-disasm
git clone https://github.com/lab313ru/ghidra_sega_ldr.git external/ghidra_sega_ldr
git clone https://github.com/devon-artmeier/md-decomp.git external/md-decomp

# Build m68k-disasm  
cd external/m68k-disasm && cmake -B build -S . && cmake --build build

# Install Python tools
pip install bare68k capstone-python keystone-engine
```

### 2. GHIDRA Setup (Week 1)
- Install GHIDRA 10.0+
- Copy Sega loader to Extensions folder
- Configure for 68000/Genesis analysis
- See: `tools/config/ghidra-setup.md`

### 3. Project Integration (Week 2)
- Configure m68k-disasm for RKA ROM
- Set up automated PC trace collection
- Integrate compression libraries
- See: Individual setup files in `tools/config/`

---

## Licensing Summary

### Public Domain / Unlicense
- m68k-disasm (Oxore)
- md-decomp compression libraries (Devon Artmeier)

### Open Source (Apache/MIT)
- GHIDRA framework (NSA)
- GHIDRA Sega loader (Dr. Mefisto)  
- BizHawk emulator
- LLM4Decompile (MIT)

### Commercial (Optional)
- IDA Pro + SMD Tools (requires license)

### Community Contributions
- Technical documentation (various authors)
- Assembly constants and macros
- Compression research and implementations

---

## Support and Community

### Primary Communities
- **Sonic Retro Forums**: Genesis development and reverse engineering
- **RHDN (RomHacking.net)**: General ROM hacking community  
- **GitHub**: Individual tool repositories and issues

### Getting Help
1. Check tool-specific documentation in `tools/config/`
2. Consult community forums for Genesis-specific questions
3. Review original author repositories for updates
4. Submit issues to appropriate GitHub repositories

---

**Acknowledgment**: This project stands on the shoulders of giants. Every tool, piece of documentation, and community contribution has made modern Genesis decompilation possible. We are deeply grateful to all contributors who have shared their knowledge freely.

**Project Philosophy**: Continue the tradition of open knowledge sharing. Document everything, credit sources, and contribute improvements back to the community.
