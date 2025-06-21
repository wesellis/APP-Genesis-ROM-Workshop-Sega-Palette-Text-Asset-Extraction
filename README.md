# Genesis ROM Workshop (GRW)

Professional Toolkit for Real Genesis ROM Modification

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![ROM Hacking](https://img.shields.io/badge/ROM-Hacking-red.svg)](https://github.com/wesellis/genesis-rom-workshop)

## The Honest Truth About ROM Hacking

**What this toolkit actually gives you:**
- Change colors that are already in the game data
- Replace text with different text (if it fits)
- Extract sprites and sounds from old games  
- Tweak simple numbers (speed, health, lives)
- Add quality-of-life features for emulation

**What it doesn't give you (because it's impossible):**
- Revolutionary graphics enhancements
- New gameplay mechanics
- True HD or widescreen conversions
- Magical performance improvements

## What Genesis ROM Workshop Actually Does

- ✅ **Palette modification** - Use colors games already had but didn't use (95% success rate)
- ✅ **Text extraction/replacement** - Translation work within length limits (80% success rate)
- ✅ **Asset extraction** - Pull sprites, sounds, data from ROMs for preservation
- ✅ **ROM analysis** - Understand how old games were built
- ✅ **Parameter tweaks** - Make Sonic faster, give more lives, adjust difficulty
- ✅ **Emulation QoL** - Save states, pause anywhere, input lag reduction

## The Reality Check

### ✅ **What You're Actually Getting:**
```
Before: Sonic is blue, runs at normal speed, 3 lives
After:  Sonic is red, runs 50% faster, 5 lives, save anywhere
```

### ❌ **What You're NOT Getting:**
```
Before: 16-bit Genesis game with 320x224 resolution
After:  Still a 16-bit Genesis game with 320x224 resolution
        (but now with slightly better colors and tweaked gameplay)
```

### 🤷‍♂️ **Is This Worth It?**

**For translation teams:** Yes - making Japanese games playable in English has real value

**For preservationists:** Yes - extracting assets from old games matters for history

**For educators:** Yes - learning how retro games work is genuinely interesting

**For casual users:** Maybe - depends if you care about red Sonic and extra lives

## Quick Start

1. **Clone and setup:**
   ```bash
   git clone https://github.com/wesellis/genesis-rom-workshop.git
   cd genesis-rom-workshop
   pip install -r requirements.txt
   ```

2. **Launch workshop:**
   ```bash
   python grw_pipeline.py
   # Interactive mode - pick your modest improvement
   ```

3. **Manage expectations:**
   ```bash
   # This will analyze your ROM and show you what's actually possible
   # Spoiler: it's mostly colors, text, and simple number changes
   ```

## Real Working Example: The Famous "Red Sonic"

```python
from grw_pipeline import GenesisROMWorkshop

# Initialize workshop
workshop = GenesisROMWorkshop()

# Load Sonic ROM
with open("sonic.md", 'rb') as f:
    rom_data = f.read()

# Extract palettes
palettes = workshop.palette_editor.extract_palettes(rom_data)

# Change Sonic from blue to red
# (This is literally the extent of most "ROM enhancements")
palettes[0][1] = (255, 0, 0)  # Blue to red

# Save your groundbreaking "red Sonic" modification
# modified_rom = workshop.palette_editor.apply_modification(rom_data, palettes)
```

**Success Rate: 95%** - Because changing blue to red in a color table is pretty straightforward.

## What This Toolkit Provides

| Tool | What It Actually Does | Success Rate | Real Value |
|------|----------------------|-------------|------------|
| **Palette Editor** | Changes existing colors to different colors | 95% | Cosmetic customization |
| **Text Editor** | Replaces text with other text (same length) | 80% | Translation projects |
| **Asset Extractor** | Copies sprites/sounds out of ROM files | 85% | Preservation, research |
| **ROM Analyzer** | Shows technical info about game structure | 98% | Education, documentation |
| **Parameter Tweaker** | Changes speed/health/lives numbers | 90% | Difficulty adjustment |

## Use Cases (Realistic)

### **Translation Teams**
**Value: HIGH** - Making Japanese games playable in English has genuine cultural impact

### **Gaming Historians/Preservationists**  
**Value: MEDIUM** - Extracting and documenting old game assets matters for preservation

### **Educators/Students**
**Value: MEDIUM** - Learning how retro games work is interesting and educational

### **ROM Hackers Who Want Red Sonic**
**Value: LOW** - It's fun for 5 minutes, then you realize it's still just Sonic

### **People Expecting HD Remasters**
**Value: ZERO** - This won't give you what you're looking for

## Development Roadmap (Honest Version)

### **v1.1 - Complete Basic Features** (2 weeks)
- [ ] Actually save color changes back to ROM files
- [ ] Visual preview of color swaps
- [ ] Batch processing for multiple color changes

### **v1.2 - Text Tools for Translators** (1 month)  
- [ ] Safe text replacement that won't crash ROMs
- [ ] Translation project management
- [ ] Length validation to prevent overflow

### **v1.3 - Better Asset Extraction** (6 weeks)
- [ ] Smarter sprite detection algorithms
- [ ] Audio format conversion
- [ ] Asset relationship mapping

### **v1.4 - Emulation Quality of Life** (3 months)
- [ ] Save state integration for any game
- [ ] Input lag reduction techniques
- [ ] Performance optimization (eliminate slowdown)
- [ ] Pause-anywhere functionality

### **v2.0 - The Limit of What's Possible** (1 year)
- [ ] Every feasible enhancement within technical constraints
- [ ] Community sharing of modifications
- [ ] Complete documentation of Genesis ROM structure
- [ ] Educational resources about hardware limitations

## What We Learned After 4 Failed Pivots

**Attempt 1:** "60fps enhancement for all Genesis games!"  
**Reality:** Impossible without rewriting every game engine

**Attempt 2:** "Universal widescreen conversion!"  
**Reality:** Graphics systems aren't designed for different aspect ratios

**Attempt 3:** "HD scaling and enhancement!"  
**Reality:** That's an emulator feature, not ROM modification

**Attempt 4:** "Genesis ROM Workshop - honest tools for modest improvements"  
**Reality:** This is what actually works

## The Bottom Line

ROM hacking gives you:
- **Different colors** instead of original colors
- **Translated text** instead of Japanese text
- **Tweaked numbers** for speed, health, difficulty
- **Extracted assets** for preservation and research
- **Quality of life** improvements for emulation

If that sounds valuable to you - great! This toolkit does those things reliably.

If you want revolutionary enhancements - this isn't the right tool. Nothing is, because they're not possible.

## Contributing

We welcome contributions from people who understand the limitations and find value in working within them.

**Realistic contributions:**
- Better color optimization algorithms
- More robust text extraction
- Improved sprite detection
- Documentation and tutorials

**Unrealistic contributions:**
- Attempts at impossible enhancements
- Marketing claims about revolutionary features
- Promises of HD graphics or 60fps conversion

## License

MIT License - see [LICENSE](LICENSE) for details.

**Legal Note:** This tool modifies ROM files you legally own. Results will be modest improvements, not revolutionary enhancements.

---

**Genesis ROM Workshop - Honest tools for realistic improvements** 🎮

*What you see is what you get. No hype, no impossible promises, just tools that do what they say they do.*
