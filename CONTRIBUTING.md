# Contributing to Genesis ROM Workshop

Thank you for your interest in contributing to an **honest** ROM modification toolkit that doesn't make impossible promises.

## 🎯 Project Philosophy (Brutally Honest)

This project exists because we got tired of ROM tools that promise revolutionary enhancements and deliver nothing. We prioritize:

- **Brutal honesty** over marketing hype
- **Working tools** over flashy promises  
- **Realistic expectations** over impossible dreams
- **Educational value** over revolutionary claims

## 🤷‍♂️ What You're Contributing To

Let's be clear about what this project actually is:

### **What This Toolkit Does:**
- Changes colors in old games (blue Sonic becomes red Sonic)
- Replaces text with different text (for translations)
- Extracts sprites and sounds from ROMs
- Tweaks simple numbers (speed, health, lives)
- Documents ROM structure for educational purposes

### **What This Toolkit Doesn't Do:**
- Create HD graphics (impossible - no texture system exists)
- Add 60fps to old games (would require rewriting game engines)
- Enable true widescreen (graphics systems not designed for it)
- Perform magical enhancements (magic isn't real)

### **Is This Worth Contributing To?**

**YES, if you value:**
- Translation work that makes old games accessible
- Preservation of gaming history through asset extraction
- Educational tools that teach how retro games work
- Honest documentation of what's possible vs impossible

**NO, if you want:**
- Revolutionary graphics enhancements
- Magical performance improvements
- Impossible technical achievements
- Marketing-friendly feature lists

## 🛠️ Realistic Contribution Areas

### **High Value Contributions:**

#### 1. **Translation Tools (Actually Important)**
- Better text extraction algorithms
- Character encoding detection
- Translation memory systems
- Project management for translation teams

**Why this matters:** Making Japanese games playable in English has real cultural value.

#### 2. **Asset Preservation (Historically Valuable)**
- Improved sprite detection
- Audio format conversion
- Asset cataloging systems
- ROM structure documentation

**Why this matters:** Preserving gaming history matters for future generations.

#### 3. **Educational Resources (Genuinely Useful)**
- Tutorials about ROM structure
- Hardware limitation explanations
- "Why X is impossible" documentation
- Realistic capability demonstrations

**Why this matters:** Teaching people about retro game development is valuable.

#### 4. **Quality of Life Improvements (Modestly Helpful)**
- Save state integration
- Input lag reduction
- Performance optimization (eliminate slowdown)
- Better color optimization within hardware limits

**Why this matters:** Small improvements can make old games more playable.

### **Low Value Contributions:**

#### ❌ **Impossible Enhancement Attempts**
- 60fps conversion projects
- True widescreen implementations
- HD graphics "enhancement"
- Revolutionary performance improvements

**Why we don't want these:** They don't work and waste everyone's time.

#### ❌ **Marketing Hype**
- Exaggerated success rate claims
- Revolutionary feature descriptions
- Impossible capability promises
- Buzzword-heavy documentation

**Why we don't want these:** This project exists to counter ROM tool marketing lies.

## 📋 Development Guidelines

### **Code Standards**
```python
def extract_palettes(rom_data: bytes) -> List[List[Tuple[int, int, int]]]:
    """
    Extract color palettes from Genesis ROM.
    
    Args:
        rom_data: Genesis ROM binary data
        
    Returns:
        List of palettes, each containing RGB color tuples
        
    Reality Check:
        This finds existing colors in the ROM data.
        It doesn't create new colors or enhance quality.
        Success rate ~95% because palette data is standardized.
    """
```

### **Documentation Standards**
- **Be honest** about limitations and success rates
- **Explain why** things are impossible, not just that they are
- **Provide realistic** examples and expectations
- **Avoid hype** and revolutionary language

### **Testing Standards**
- Test with real Genesis ROMs (legally owned)
- Document actual success rates with specific games
- Note failures and limitations honestly
- Compare results with original game behavior

## 🎯 How to Contribute

### **1. Pick a Realistic Task**
Check [GitHub Issues](../../issues) for:
- "translation-tools" label
- "asset-extraction" label  
- "documentation" label
- "quality-of-life" label

**Avoid issues labeled:**
- "impossible-enhancement"
- "revolutionary-feature"
- "magic-required"

### **2. Set Realistic Expectations**
```bash
# Good contribution goal:
"Improve text extraction success rate from 80% to 85%"

# Bad contribution goal:
"Add revolutionary HD graphics enhancement"
```

### **3. Submit Honest Pull Requests**
```
Title: "Improve sprite detection accuracy by 10%"

Description:
- What: Better heuristics for finding sprite data
- Why: Current method misses compressed sprites
- Reality: Still won't detect everything, but helps
- Testing: Tested with 20 games, success rate 80% → 90%
```

## 🧪 Testing Your Changes

### **Required Reality Checks**
```bash
# Test with these questions:
1. Does this actually work?
2. What's the real success rate?
3. What are the limitations?
4. Is this genuinely useful?
5. Am I overhyping the results?
```

### **Success Criteria**
- **Works:** Feature actually functions as described
- **Honest:** Documentation matches reality
- **Useful:** Provides genuine value to users
- **Realistic:** Doesn't promise impossible things

## 📖 Resources for Contributors

### **Learn About Genesis Hardware:**
- [Genesis Technical Reference](https://segaretro.org/Genesis_technical_information)
- [VDP Programming Guide](https://plutiedev.com/vdp-intro)
- [Sound Chip Documentation](https://plutiedev.com/ym2612-intro)

### **Understand the Limitations:**
- 512 total colors max (9-bit RGB)
- 64 colors on-screen simultaneously
- Fixed resolution (320x224 or 256x224)
- M68000 CPU with specific timing constraints

### **ROM Hacking Community:**
- [RHDN Forums](https://www.romhacking.net/forum/)
- [Genesis ROM Hacking Resources](https://info.sonicretro.org/Category:Technical_information)

## 🚫 What We Don't Accept

### **Impossible Feature Attempts**
- ❌ Code that tries to add 60fps to games
- ❌ Widescreen conversion implementations
- ❌ HD graphics enhancement attempts
- ❌ Magic performance improvements

### **Marketing Nonsense**
- ❌ Revolutionary feature claims
- ❌ Exaggerated success rates
- ❌ Buzzword-heavy descriptions
- ❌ Impossible capability promises

### **Time-Wasting Projects**
- ❌ Attempts to "enhance" fundamental hardware limitations
- ❌ Projects that ignore technical reality
- ❌ Features that can't actually work

## 🏆 Recognition for Realistic Contributions

### **Valued Contributors:**
- People who improve translation tools
- Developers who enhance asset extraction
- Writers who create honest documentation
- Testers who provide realistic feedback

### **Hall of Fame:**
- Contributors who significantly improve success rates
- People who add genuinely useful features
- Developers who maintain realistic expectations
- Anyone who helps keep the project honest

## 💭 The Big Picture

This project exists because the ROM hacking community is full of tools that promise impossible things and deliver nothing. We're building something different:

**A toolkit that:**
- Does what it says it does
- Documents real limitations
- Helps with achievable goals
- Doesn't waste people's time

**If you value honesty over hype, realistic tools over impossible promises, and working code over marketing claims, we'd love your contributions.**

## 🆘 Getting Help

### **Good Questions:**
- "How can I improve text extraction success rates?"
- "What's the best way to detect compressed sprites?"
- "Why is X impossible and what can we do instead?"

### **Questions We Can't Help With:**
- "How do I add 60fps to Genesis games?" (You don't)
- "Can we make true HD graphics?" (No)
- "Is revolutionary enhancement possible?" (No)

---

**Every realistic contribution helps build better tools and advances honest ROM hacking knowledge.**

Thank you for contributing to Genesis ROM Workshop! 🎮

*Remember: We build tools that actually work, not tools that make impossible promises.*
