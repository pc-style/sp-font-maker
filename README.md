# Mathematical Handwritten Font Creator

Convert your handwritten mathematical symbols into a custom font for use in LaTeX, Word, or any application!

## About

This tool takes a scanned image or SVG of handwritten mathematical symbols and outputs a valid `.ttf` or `.otf` file. The font includes:

- **Basic Latin letters**: A-Z (uppercase and lowercase)
- **Digits**: 0-9
- **Greek letters**: Α-Ω, α-ω (uppercase and lowercase)
- **Mathematical operators**: +, -, ×, ÷, =, ≠, <, >, ≤, ≥
- **Advanced symbols**: ∫, ∑, ∏, √, ∂, ∇, ∞, ∈, ∉, ⊂, ⊃, ∪, ∩, ∅
- **Logic operators**: ∧, ∨, ¬, ∀, ∃
- **Arrows**: →, ←, ↑, ↓, ⇒, ⇐, ↔
- **Brackets and punctuation**: ( ) [ ] { } , . : ; ! ? ' " / \ | _ ^ ~

## Usage Instructions

1. Download and print the template (or fill it out digitally):
   - `template.pdf` or `template.png`

2. Fill in all the boxes with your handwritten symbols

3. Scan or photograph your completed template

4. Run the tool:
   ```bash
   handwrite your-template.jpg output-directory/
   ```

5. Use your new font in any application!

## Installation Instructions

### Prerequisites
- Python 3.7 or higher
- FontForge (for font generation)

### Install from source

```bash
git clone https://github.com/pc-style/sp-font-maker.git
cd sp-font-maker
pip install -e .
```

### Install FontForge

#### macOS
```bash
brew install fontforge
```

#### Ubuntu/Debian
```bash
sudo apt-get install fontforge python3-fontforge
```

#### Windows
Download and install from [FontForge website](https://fontforge.org/)

## Command Line Options

```bash
handwrite [OPTIONS] INPUT_PATH OUTPUT_DIRECTORY
```

Options:
- `--filename NAME`: Set the font filename (default: "MathHandwriting")
- `--family NAME`: Set the font family name (default: same as filename)
- `--designer NAME`: Set the designer name
- `--license TYPE`: Set license (use "ofl" for SIL OFL 1.1, "cc0" for CC0)
- `--debug-directory PATH`: Save intermediate files for debugging
- `--pixel`: Create a pixel-style font (experimental)

### Example

```bash
handwrite my-math-symbols.jpg ./output/ --filename "MyMathFont" --designer "John Doe" --license ofl
```

## Use Cases

- Create personalized mathematical notation for educational materials
- Generate custom fonts for LaTeX documents
- Design unique mathematical handwriting for presentations
- Create accessible math fonts with your preferred style

## Technical Details

The tool processes your handwritten symbols through several stages:

1. **Sheet to PNG**: Detects individual symbols from the grid template
2. **PNG to SVG**: Converts bitmap images to vector graphics
3. **SVG to TTF**: Generates a TrueType font with proper Unicode mappings
4. **Font post-processing**: Adds metadata and finalizes the font

All mathematical symbols are mapped to their standard Unicode code points for maximum compatibility.

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

This project is based on [Handwrite](https://github.com/builtree/handwrite) and adapted for mathematical symbols.

See [LICENSE](LICENSE) for the project license.

---

## Credits

- Original Handwrite project: [builtree/handwrite](https://github.com/builtree/handwrite)
- Adapted for sitelen pona by [KelseyHigham](https://github.com/KelseyHigham/sp-font-maker)
- Refactored for mathematical symbols by the MathHandwriting team

## Support

For issues and questions, please use the [GitHub issue tracker](https://github.com/pc-style/sp-font-maker/issues).
