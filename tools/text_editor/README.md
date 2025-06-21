# Text Editor Guide  
# Professional text extraction and replacement for translation projects

## How Genesis Text Works

Genesis games store text in various ways:
1. **Plain ASCII** - Easy to find and modify
2. **Custom character sets** - Game-specific encoding
3. **Compressed text** - Harder to modify
4. **Fixed-width strings** - Must maintain exact length

## Text Modification Process

### 1. Text Extraction
```bash
python grw_pipeline.py your_rom.md
# Select: Text Editor
# Choose: Extract all text strings
# Output: text_strings_your_rom.json
```

### 2. Translation Planning
Review extracted strings and note:
- **Length constraints** - New text must fit in original space
- **Context** - Where each string appears in game
- **Special characters** - Control codes, formatting

### 3. Text Replacement
```python
# Replace individual strings
text_editor.replace_text_string(
    rom_data,
    offset=0x12345,
    old_text="PRESS START",
    new_text="APPUYEZ SUR"  # Must be same length or shorter
)
```

## Success Examples

### High Success Rate (90%+):
- **Menu text** - Usually uncompressed ASCII
- **Character names** - Fixed-length fields
- **Item names** - Simple string tables
- **Credits text** - Plain text format

### Medium Success Rate (60-80%):
- **Dialog text** - May use compression or word-wrapping
- **Story text** - Often compressed to save space
- **Instructions** - May have formatting codes

### Low Success Rate (30-50%):
- **Japanese games** - Use complex character encoding
- **Compressed dialog** - Requires decompression first
- **Formatted text** - Has embedded control codes

## Translation Project Workflow

### Phase 1: Analysis
1. Extract all text strings
2. Identify text types and contexts
3. Test modification on sample strings
4. Document length constraints

### Phase 2: Translation
1. Translate strings within length limits
2. Handle special characters appropriately  
3. Test modifications in emulator
4. Document any issues found

### Phase 3: Integration
1. Apply all text changes
2. Verify text displays correctly
3. Test complete game playthrough
4. Create distribution patch

## Common Issues and Solutions

### Text Too Long
**Problem:** Translation doesn't fit in original space
**Solution:** Use abbreviations, shorter phrases, or multi-line display

### Garbled Characters  
**Problem:** Game uses custom character set
**Solution:** Map custom encoding or use hex editing with character table

### Missing Text
**Problem:** Some text not found by extraction
**Solution:** Manual ROM analysis to find compressed or encoded text

### Formatting Broken
**Problem:** Text layout is corrupted
**Solution:** Preserve control codes and spacing from original

## Tools and Resources

### Included Tools:
- Text string extractor
- Length-aware text replacer
- Character encoding analyzer
- Project management templates

### External Tools (Recommended):
- Hex editor (HxD, 010 Editor)
- Genesis emulator for testing
- Character table generators
- Text compression tools

## Professional Tips

1. **Always backup original ROM** before making changes
2. **Test frequently** in emulator during translation
3. **Document everything** - offsets, lengths, special cases
4. **Use consistent terminology** across all translated text
5. **Plan for longer languages** - some need 20% more space
6. **Consider cultural adaptation** not just literal translation

## Legal Considerations

- Only modify ROMs you legally own
- Distribute patches, not modified ROMs
- Credit original developers
- Respect copyright and trademark law
- Follow fan translation community guidelines
