# Contributing to Genesis ROM Workshop

Thank you for your interest in contributing to Genesis ROM Workshop! This project focuses on **real, working ROM modification tools** with documented success rates.

## 🎯 Project Philosophy

We prioritize:
- **Working tools over flashy features**
- **Honest documentation over marketing claims**  
- **Real success rates over impossible promises**
- **Educational value over complexity**

## 🚀 Quick Start for Contributors

### Prerequisites
- Python 3.8+
- Basic understanding of ROM file formats
- Respect for intellectual property rights

### Setup
```bash
git clone https://github.com/yourusername/genesis-rom-workshop.git
cd genesis-rom-workshop
pip install -r requirements.txt
python grw_pipeline.py  # Test the workshop
```

## 🛠️ Contribution Areas

### **Priority Areas (Help Needed!)**

#### 1. **Complete Palette Modification (v1.1)**
- **What's missing:** Palette changes aren't saved back to ROM
- **Skills needed:** Python, binary file handling
- **Impact:** High - makes palette editor actually functional
- **Files:** `grw_pipeline.py` - `PaletteEditor` class

#### 2. **Text Replacement Validation (v1.2)**
- **What's missing:** Length validation, encoding detection
- **Skills needed:** Text processing, character encoding
- **Impact:** High - prevents ROM crashes from text overflow
- **Files:** `grw_pipeline.py` - `TextEditor` class

#### 3. **Asset Detection Improvements (v1.3)**
- **What's missing:** Better sprite detection heuristics
- **Skills needed:** Pattern recognition, Genesis graphics formats
- **Impact:** Medium - improves asset extraction quality
- **Files:** `grw_pipeline.py` - `AssetExtractor` class

#### 4. **Documentation and Examples**
- **What's missing:** Step-by-step tutorials, real examples
- **Skills needed:** Technical writing, ROM hacking knowledge
- **Impact:** High - helps users actually use the tools
- **Files:** `tools/` directory, examples

### **Secondary Areas**

#### GUI Development
- Visual palette editor with color picker
- Text editor with in-ROM preview
- Project management interface

#### ROM Format Support
- Additional Genesis ROM formats
- Error handling for corrupted files
- Cross-platform compatibility

#### Community Features
- Modification sharing system
- Translation project templates
- Quality verification tools

## 📋 Development Guidelines

### **Code Standards**
- **Python style:** Follow PEP 8 with clear docstrings
- **Error handling:** Graceful failure with helpful messages
- **Documentation:** Comment complex algorithms and format handling
- **Testing:** Test with multiple ROM files and formats

### **Genesis ROM Specifics**
- Understand ROM formats: .md (interleaved), .bin, .smd, .gen
- Handle byte swapping correctly for .md format
- Respect hardware limitations (palette size, text length)
- Preserve original ROM behavior and structure

### **File Organization**
```python
def modify_rom_data(rom_data: bytes, modifications: dict) -> bytes:
    """
    Apply modifications to ROM data.
    
    Args:
        rom_data: Original ROM binary data
        modifications: Dict of changes to apply
        
    Returns:
        Modified ROM data
        
    Raises:
        ValueError: If modifications would corrupt ROM
    """
```

## 🔍 How to Contribute

### **1. Pick an Issue**
- Check [GitHub Issues](../../issues) for open tasks
- Look for "good first issue" labels for beginners
- Comment on issues to claim them

### **2. Development Process**
```bash
# Create feature branch
git checkout -b feature/palette-modification-saving

# Make changes with tests
python grw_pipeline.py "test_rom.md"  # Test your changes

# Commit with clear messages  
git commit -m "Implement palette modification saving to ROM files"

# Push and create PR
git push origin feature/palette-modification-saving
```

### **3. Pull Request Guidelines**
- **Clear description:** What problem does this solve?
- **Testing notes:** How did you test the changes?
- **Example usage:** Show the feature working
- **Documentation:** Update relevant docs

## 🧪 Testing Your Changes

### **Required Tests**
```bash
# Test with different ROM formats
python grw_pipeline.py "sonic.md"     # Interleaved format
python grw_pipeline.py "sonic.bin"    # Binary format  
python grw_pipeline.py "sonic.smd"    # SMD format

# Test error handling
python grw_pipeline.py "corrupted.md" # Should fail gracefully
python grw_pipeline.py "not_a_rom.txt" # Should detect invalid file
```

### **Success Criteria**
- No crashes on valid ROM files
- Clear error messages for invalid files
- Preserves original ROM functionality
- Works across different Genesis games

## 📖 Resources for Contributors

### **Genesis Technical Resources**
- [Sega Genesis/Mega Drive Architecture](https://www.copetti.org/writings/consoles/mega-drive-genesis/)
- [Genesis ROM Format Documentation](http://md.squee.co/Code)
- [Genesis Palette Format](https://segaretro.org/Palette)

### **ROM Hacking Community**
- [RHDN (ROM Hacking Database)](https://www.romhacking.net/)
- [Genesis Hacking Community](https://forums.sonicretro.org/)
- [Technical Documentation](https://info.sonicretro.org/Category:Technical_information)

### **Python Resources**
- [Binary File Handling](https://docs.python.org/3/library/struct.html)
- [Bytes and Bytearray](https://docs.python.org/3/library/stdtypes.html#bytes-objects)

## 🚫 What We Don't Accept

### **Impossible Features**
- ❌ 60fps conversion attempts
- ❌ Widescreen conversion code
- ❌ "HD enhancement" features
- ❌ Features that violate hardware limitations

### **Code Quality Issues**
- ❌ Uncommented complex algorithms
- ❌ Hardcoded paths or assumptions
- ❌ Missing error handling
- ❌ Platform-specific code without alternatives

### **Legal Issues**
- ❌ Copyrighted ROM files in commits
- ❌ Copyrighted graphics or audio
- ❌ Code that enables piracy
- ❌ Trademark violations

## 🏆 Recognition

### **Contributor Levels**
- **⭐ Helper:** Documentation, bug reports, testing
- **🌟 Developer:** Code contributions, feature implementation
- **🚀 Maintainer:** Regular contributions, code review, project direction

### **Hall of Fame**
Contributors will be recognized in:
- README.md credits section
- CONTRIBUTORS.md file
- Release notes for major contributions

## 🆘 Getting Help

### **Stuck on Something?**
1. **Check existing docs** in `tools/` directories
2. **Search GitHub Issues** for similar problems
3. **Ask in GitHub Discussions** for technical questions
4. **Reference the codebase** - it's designed to be readable

### **Need Genesis ROM Knowledge?**
- Start with the resources listed above
- Join ROM hacking communities for advice
- Study existing ROM hacking tools for patterns
- Test with simple ROMs first (Sonic games are well-documented)

## 💡 Ideas for New Contributors

### **Easy First Contributions**
- Improve error messages in existing code
- Add support for additional ROM file extensions
- Create tutorial documentation with screenshots
- Test the workshop with different Genesis games

### **Medium Difficulty**
- Implement palette modification saving
- Add text length validation
- Improve sprite detection algorithms
- Create unit tests for core functions

### **Advanced Projects**
- GUI interface development
- Advanced ROM analysis features
- Integration with existing ROM hacking tools
- Community sharing platform

---

**Every contribution helps preserve gaming history and advances ROM hacking knowledge.**

Thank you for contributing to Genesis ROM Workshop! 🎮

*Remember: We build tools that actually work, not tools that make impossible promises.*
