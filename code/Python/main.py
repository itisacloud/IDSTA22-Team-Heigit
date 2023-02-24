import argparse
from preprocess import preprocess
parser = argparse.ArgumentParser()

parser.add_argument("command",
                    action="store",
                    nargs='1',
                    default=None,
                    required=True,
                    choices=["preprocess","process","full"],)

parser.add_argument("filepath",
                    action="store",
                    nargs='1',
                    default=r"../../files/tweets/output.RData",
                    required=False,
                    )
parser.add_argument("filepathOut",
                    action="store",
                    nargs='1',
                    default=r"../../files/aoi/3_mittel.geo.json",
                    required=False,
                    )

parser.add_argument("filepathAoi",
                    action="store",
                    nargs='1',
                    default=r"../../files/aoi/3_mittel.geo.json",
                    required=False,
                    )

parser.add_argument("columns",
                    action="store",
                    nargs='1',
                    default=",".join([f"NAME_{i}" for i in range(4)]),
                    required=False,
                    )

args = parser.parse_args()

if args.command=="preprocess":
    fp = args.filepath
    cols = args.columns.split(",")
    fp_aoi = args.filepathAoi
    fp_output = args.filepathOut
    preprocess(fp,fp_output,fp_aoi,cols)
"""
if args.command=="process":

if args.command=="full":"""


