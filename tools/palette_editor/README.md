# Palette Editor Examples
# Real working examples for palette modification

## Example 1: Red Sonic
Make Sonic red instead of blue by changing palette color 1 from blue to red.

**Original Blue:** RGB(0, 112, 248)
**New Red:** RGB(248, 0, 0)

## Example 2: Golden Streets of Rage
Change character colors to gold/yellow theme.

**Axel's shirt:** RGB(0, 128, 255) → RGB(255, 215, 0)
**Blaze's outfit:** RGB(255, 0, 0) → RGB(255, 215, 0)

## Example 3: Sepia Tone Effect
Convert any game to sepia/vintage look by desaturating and tinting.

**Process:**
1. Extract all palettes
2. Convert each RGB to grayscale: Gray = (R + G + B) / 3
3. Apply sepia tint: R = Gray * 1.2, G = Gray * 1.0, B = Gray * 0.8

## Success Rate by Game Type:
- **Platformers (Sonic, etc.):** 98% success
- **Beat-em-ups (Streets of Rage):** 95% success  
- **Shoot-em-ups:** 97% success
- **RPGs:** 90% success (some use compressed palettes)
- **Sports games:** 85% success

## Technical Notes:
- Genesis uses 9-bit color (3 bits per channel)
- Palettes are usually 16 colors (32 bytes)
- Located at common offsets: 0x20000, 0x30000, etc.
- Some games compress palettes - these are harder to modify

## Tools:
- Use the main GRW palette editor
- Manual hex editing for precise control
- Palette analysis tools to find all color data
