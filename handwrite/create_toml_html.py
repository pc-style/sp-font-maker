import json
import os
import platform
import subprocess
from datetime import datetime

#    ▄                █
#   ▀█▀  ▄▀▀▄  █▀▄▀▄  █
#    █   █  █  █ █ █  █
# ▄  ▀▄  ▀▄▄▀  █ █ █  █
# generate metadata and preview files


def create_toml_html(debug_dir, out_dir, cli_args=None, other_words_string=None):
    """Generate metadata and preview files for the mathematical font.
    
    This is a simplified version for mathematical fonts, replacing the
    sitelen pona-specific preview generation.
    """
    cli_args_dict = cli_args

    filename = cli_args_dict.get("filename", "MathHandwriting")
    if filename is None:
        raise NameError("filename not found in config file.")

    family = cli_args_dict.get("family", None) or filename
    designer = cli_args_dict.get("designer", "MathHandwriting Creator")

    # for generating metadata files, we use short license codes from the SPDX License List
    license = cli_args_dict.get("license", "All rights reserved")
    licenseurl = cli_args_dict.get("license_url", "")
    if license == "ofl":
        license = "OFL-1.1"
        licenseurl = "https://openfontlicense.org"
    if license == "cc0":
        license = "CC0-1.0"
        licenseurl = "https://creativecommons.org/publicdomain/zero/1.0/"

    not_new = cli_args_dict.get("not_new", False)
    if not_new:
        print("\nSkipping metadata file generation.\n")
    else:
        # Generate a simple metadata file
        metadata_file_path = out_dir + os.sep + family + "_metadata.toml"
        if os.path.exists(metadata_file_path):
            print(f"\nOverwriting {metadata_file_path}\n")
        else:
            print(f"\nCreating {metadata_file_path}\n")
        
        with open(metadata_file_path, "w", encoding="utf-8") as metadata_file:
            metadata_file.write(f"""# Mathematical Handwritten Font Metadata

id        = "{family}"
name      = "{family}"
filename  = "{filename}.ttf"
creator   = ["{designer}"]
license   = "{license}"
license_url = "{licenseurl}"
writing_system = "mathematical notation"

last_updated = "{datetime.now().strftime("%Y-%m-%d")}"
version      = "1.0.0"

description = '''
A handwritten mathematical font containing:
- Basic Latin letters (A-Z, a-z)
- Digits (0-9)
- Greek letters (uppercase and lowercase)
- Mathematical operators and symbols
- Logic symbols
- Set theory symbols
- Arrows and relations
'''

features = [
  "Unicode-compliant mathematical symbols",
  "Standard codepoint mapping",
  "Latin alphabet (A-Z, a-z)",
  "Digits (0-9)",
  "Greek alphabet (Α-Ω, α-ω)",
  "Mathematical operators (+, -, ×, ÷, =, ≠, <, >, ≤, ≥, ±)",
  "Calculus symbols (∫, ∑, ∏, ∂, ∇)",
  "Set theory (∈, ∉, ⊂, ⊃, ∪, ∩, ∅)",
  "Logic (∧, ∨, ¬, ∀, ∃, ⇒, ⇐)",
  "Arrows and relations (→, ←, ↑, ↓, ↔)",
  "Special symbols (∞, √, ≈, ≡, ∝, ⊥, ∥, ∠)",
]

supported_applications = [
  "LaTeX",
  "Microsoft Word",
  "Google Docs",
  "Any Unicode-compliant text editor",
]
""")

        # Create a simple HTML preview file
        html_file_path = out_dir + os.sep + family + "_preview.html"
        with open(html_file_path, "w", encoding="utf-8") as html_file:
            html_file.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{family} - Mathematical Font Preview</title>
    <style>
        @font-face {{
            font-family: '{family}';
            src: url('{filename}.ttf') format('truetype');
        }}
        body {{
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        h1, h2 {{
            color: #333;
        }}
        .preview {{
            font-family: '{family}', serif;
            background: white;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .category {{
            margin: 30px 0;
        }}
        .symbols {{
            font-size: 32px;
            line-height: 1.8;
            letter-spacing: 10px;
        }}
        .label {{
            font-family: Arial, sans-serif;
            font-size: 14px;
            color: #666;
            margin-bottom: 10px;
        }}
    </style>
</head>
<body>
    <h1>{family}</h1>
    <p>Designer: {designer}</p>
    <p>License: {license}</p>
    
    <div class="category">
        <h2>Uppercase Latin</h2>
        <div class="preview symbols">
            ABCDEFGHIJKLMNOPQRSTUVWXYZ
        </div>
    </div>
    
    <div class="category">
        <h2>Lowercase Latin</h2>
        <div class="preview symbols">
            abcdefghijklmnopqrstuvwxyz
        </div>
    </div>
    
    <div class="category">
        <h2>Digits</h2>
        <div class="preview symbols">
            0123456789
        </div>
    </div>
    
    <div class="category">
        <h2>Greek Uppercase</h2>
        <div class="preview symbols">
            ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ
        </div>
    </div>
    
    <div class="category">
        <h2>Greek Lowercase</h2>
        <div class="preview symbols">
            αβγδεζηθικλμνξοπρστυφχψω
        </div>
    </div>
    
    <div class="category">
        <h2>Mathematical Operators</h2>
        <div class="preview symbols">
            + - × ÷ = ≠ &lt; &gt; ≤ ≥ ± ∞
        </div>
    </div>
    
    <div class="category">
        <h2>Calculus & Analysis</h2>
        <div class="preview symbols">
            ∫ ∑ ∏ √ ∂ ∇
        </div>
    </div>
    
    <div class="category">
        <h2>Set Theory</h2>
        <div class="preview symbols">
            ∈ ∉ ⊂ ⊃ ⊆ ⊇ ∪ ∩ ∅
        </div>
    </div>
    
    <div class="category">
        <h2>Logic Symbols</h2>
        <div class="preview symbols">
            ∧ ∨ ¬ ∀ ∃ ∄ ⇒ ⇐ ↔
        </div>
    </div>
    
    <div class="category">
        <h2>Arrows & Relations</h2>
        <div class="preview symbols">
            → ← ↑ ↓ ↔ ≈ ≡ ∝ ⊥ ∥ ∠
        </div>
    </div>
    
    <div class="category">
        <h2>Brackets & Punctuation</h2>
        <div class="preview symbols">
            ( ) [ ] {{ }} , . : ; ! ? ' " / \\ | _ ^ ~
        </div>
    </div>
    
    <div class="category">
        <h2>Sample Equations</h2>
        <div class="preview" style="font-size: 24px;">
            <p>E = mc²</p>
            <p>∫₀^∞ e^(-x²) dx = √π / 2</p>
            <p>∑ᵢ₌₁^n i = n(n+1) / 2</p>
            <p>∇ × E = -∂B / ∂t</p>
            <p>α² + β² = γ²</p>
            <p>∀ x ∈ ℝ, ∃ y ∈ ℝ : y > x</p>
        </div>
    </div>
    
    <footer style="margin-top: 50px; padding-top: 20px; border-top: 1px solid #ddd; color: #666;">
        <p>Generated by Mathematical Handwritten Font Creator</p>
        <p>Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    </footer>
</body>
</html>
""")
        
        print(f"Created preview at {html_file_path}")
        
        # Open the HTML file in the browser (optional)
        if platform.system() == "Darwin":  # macOS
            subprocess.run(["open", html_file_path])
        elif platform.system() == "Windows":
            os.startfile(html_file_path)
        # Linux users can manually open the file
