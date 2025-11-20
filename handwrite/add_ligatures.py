import json
import os
import sys

import fontTools  # camelCase!
from fontTools import ttLib  # camelCase!
from fontTools.feaLib import builder  # camelCase!

# █   ▀               ▄
# █  ▀█  ▄▀▀█   ▀▀▄  ▀█▀  █  █  █▄▀  ▄▀▀▄  ▄▀▀▄
# █   █  █  █  ▄▀▀█   █   █  █  █    █▄▄█   ▀▄
# █   █  ▀▄▄█  ▀▄▄█   ▀▄  ▀▄▄█  █    ▀▄▄   ▀▄▄▀
#         ▄▄▀


def add_ligatures(
    debug_dir, out_dir, default_json, cli_args=None, other_words_string=None
):
    # Mathematical fonts typically don't need complex ligature systems
    # like sitelen pona. We'll create a minimal ligature file for compatibility.

    cli_args_dict = cli_args

    with open(default_json) as f:
        default_json_data = json.load(f)

    filename = cli_args_dict.get("filename", "MathHandwriting")
    if filename is None:
        raise NameError("filename not found in config file.")

    family = cli_args_dict.get("family", None) or filename

    # fontTools: input font file
    infile = str(debug_dir + os.sep + (filename + " without ligatures.ttf"))

    # fontTools: output font file
    filename = filename + ".ttf" if not filename.endswith(".ttf") else filename
    outfile = str(out_dir + os.sep + filename)

    # Minimal ligature string for mathematical font
    # Mathematical fonts generally don't need ligatures, but we keep the structure
    # for potential future mathematical combinations (like multi-character operators)
    ligatures_string = """languagesystem DFLT dflt;
languagesystem latn dflt;

# LIGATURES
# Mathematical fonts typically use direct Unicode mapping without ligatures

feature liga {
} liga;
"""

    # Write the feature file
    feature_file = open(debug_dir + os.sep + family + ".fea", "w", encoding="utf-8")
    feature_file.write(ligatures_string)
    feature_file.close()

    tt = ttLib.TTFont(infile, recalcTimestamp=False)
    builder.addOpenTypeFeatures(tt, debug_dir + os.sep + family + ".fea", debug=True)
    sys.stderr.write("Generating %s...\n" % outfile)
    tt.save(outfile)
    print("\a")
