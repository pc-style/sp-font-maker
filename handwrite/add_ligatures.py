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
    # Now the font has exported, presumably.
    # We're back to the `python` environment, not the `ffpython` one, so we can use libraries like fontTools, camelCase.

    # `debug_dir` is the temp directory

    cli_args_dict = cli_args

    with open(default_json) as f:
        default_json_data = json.load(f)

    filename = cli_args_dict.get("filename", "MathHandwriting")
    if filename is None:
        raise NameError("filename not found in config file.")

    family = cli_args_dict.get("family", None) or filename

    # fontTools: input font file
    infile = str(debug_dir + os.sep + (filename + " without ligatures.ttf"))
    # sys.stderr.write("\nAdding ligatures to %s\n" % infile)

    # fontTools: output font file
    filename = filename + ".ttf" if not filename.endswith(".ttf") else filename
    outfile = str(out_dir + os.sep + filename)
    # while os.path.exists(outfile):
    #     filename = os.path.splitext(filename)[0] + " (1).ttf"
    #     outfile = out_dir + os.sep + filename

    ligatures_string = """languagesystem DFLT dflt; # this part is apparently necessary so that
languagesystem latn dflt; # people can edit the font in fontforge after??










# LIGATURES

feature liga {
"""

    list_of_ligs = []

    # create ligature lines
    with open(default_json) as f:
        glyphs = json.load(f).get("glyphs", {}).get("sheet", {})
        for glyph in glyphs:
            if "ligature" in glyph:
                lig = glyph["ligature"]
                name = glyph["name"]

                # create tuples of ligature text, followed by ligature length by tokens
                list_of_ligs.append(
                    (
                        f"  sub   {lig.rjust(22)}   by   {name.rjust(13)};",
                        len(lig.split(" ")),
                    )
                )

    aliases = default_json_data.get("glyphs", {}).get("ligature-aliases") or []
    for alias in aliases:
        list_of_ligs.append(
            (
                f"  sub   {(alias['ligature']).rjust(22)}   by   {(alias['target-name']).rjust(13)};",
                len(alias["ligature"].split(" ")),
            )
        )

    # sort them by number of tokens
    list_of_ligs.sort(reverse=True, key=lambda x: x[1])

    # add to our cool string
    for line in list_of_ligs:
        ligatures_string += line[0] + "\n"

    ligatures_string += """} liga;"""

    # print(ligatures_string)
    feature_file = open(debug_dir + os.sep + family + ".fea", "w", encoding="utf-8")
    feature_file.write(ligatures_string)
    feature_file.close()

    tt = ttLib.TTFont(infile, recalcTimestamp=False)
    builder.addOpenTypeFeatures(tt, debug_dir + os.sep + family + ".fea", debug=True)
    sys.stderr.write("Generating %s...\n" % outfile)
    tt.save(outfile)
    print("\a")
