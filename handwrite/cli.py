import argparse
import json
import os
import shutil
import tempfile

import tomllib

from handwrite.add_ligatures import add_ligatures
from handwrite.create_toml_html import create_toml_html
from handwrite.pngtosvg import png_to_svg
from handwrite.sheettopng import sheet_to_png
from handwrite.svgtottf import svg_to_ttf


def run(sheet, output_directory, debug_dir, default_json, cli_args, other_words_string):
    create_toml_html(debug_dir, output_directory, cli_args, other_words_string)
    sheet_to_png(sheet, debug_dir, default_json, cli_args, other_words_string)
    png_to_svg(cli_args, default_json, debug_dir=debug_dir)
    svg_to_ttf(debug_dir, output_directory, default_json, cli_args, other_words_string)
    add_ligatures(
        debug_dir, output_directory, default_json, cli_args, other_words_string
    )


def converters(
    sheet,
    output_directory,
    debug_dir=None,
    default_json=None,
    cli_args=None,
    other_words_string=None,
):
    # debug/temp directory
    if not debug_dir:
        debug_dir = tempfile.mkdtemp()
        isTempdir = True
    else:
        isTempdir = False
    if not os.path.isdir(debug_dir):
        print("Debug directory does not exist. Creating it at", debug_dir)
        os.makedirs(debug_dir, exist_ok=True)

    if default_json is None:
        default_config = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "default.toml"
        )
        default_json = default_config

    # read initial config data from TOML
    with open(default_json, "rb") as file:
        font_data = tomllib.load(file)

    # save as JSON in debug directory. we'll edit it to add custom words.
    # extra config sheets should be merged into the same working JSON file.
    # ...we do this exact thing again after populating other_words... this is redundant.
    json_path = os.path.join(debug_dir, "default.json")
    with open(json_path, "w") as file:
        json.dump(font_data, file, indent=4)
    default_json = json_path

    # Mathematical font doesn't need custom words handling like sitelen pona did
    # All glyphs are predefined in default.toml

    with open(default_json, "w") as file:
        json.dump(font_data, file, indent=4)

    if os.path.isdir(default_json):
        raise IsADirectoryError("Config parameter should not be a directory.")

    if os.path.isdir(sheet):
        raise IsADirectoryError("Sheet parameter should not be a directory.")
    else:
        run(
            sheet,
            output_directory,
            debug_dir,
            default_json,
            cli_args,
            other_words_string,
        )

    if isTempdir:
        shutil.rmtree(debug_dir)


def main():
    print(
        "Mathematical Handwritten Font Creator - Convert your handwritten math symbols to a font!"
    )
    print(
        "If you get errors, try `handwrite --help`. "
        + "Also check the analysis PNGs in the debug directory."
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Path to sample sheet")
    parser.add_argument("output_directory", help="Directory Path to save font output")
    parser.add_argument(
        "--debug-directory",
        help="Generate in-progress PNGs, BMPs, SVGs, SFDs, and TTFs to this path \
        (Temp by default)",
        default=None,
    )
    parser.add_argument(
        "--filename", help='Font File name ("MathHandwriting" by default)', default="MathHandwriting"
    )
    parser.add_argument(
        "--family", help="Font Family name (filename by default)", default=None
    )
    parser.add_argument(
        "--designer", help='Font Designer name ("me" by default)', default=None
    )
    parser.add_argument(
        "--license",
        help='Font License. \
        (`--license ofl` and `--license cc0` will populate License and LicenseURL appropriately. \
        IMPORTANT: The command line tool defaults to "All rights reserved", even though the sheet defaults to OFL.)',
        default=None,
    )
    parser.add_argument(
        "--license-url", help='Font License URL ("" by default)', default=None
    )
    parser.add_argument(
        "--sheet-version", help="Sheet version (latest by default)", default=None
    )
    parser.add_argument(
        "--pixel",
        action="store_true",
        help="Pixel font (experimental, false by default)",
        default=False,
    )
    parser.add_argument(
        "--not-new",
        action="store_true",
        help="Skip creating a .TOML file (false by default)",
        default=False,
    )

    args = parser.parse_args()
    cli_args = vars(parser.parse_args())
    converters(
        args.input_path,
        args.output_directory,
        args.debug_directory,
        None,
        cli_args,
        None,  # other_words_string not needed for math font
    )
