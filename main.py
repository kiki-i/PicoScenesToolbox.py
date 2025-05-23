#!/usr/bin/env python3

from datetime import datetime
from pathlib import Path
import glob

import numpy as np

from src.parsecli import parseCli
from src.PicoParser import Parser


def printInfo(info: str):
  now = datetime.now().strftime("%H:%M:%S")
  print(f"[{now}] {info}")


if __name__ == "__main__":
  args = parseCli()
  outDir = Path(args.output)

  fileList = []
  for path in args.input:
    fileList.extend(glob.glob(path, recursive=True))

  for file in fileList:
    filePath = Path(file).expanduser()
    printInfo(f"Convert {filePath.name}:")

    with Parser(filePath) as parser:
      if any([args.timestamp, args.csi, args.magnitude, args.phase]):
        outDir.mkdir(parents=True, exist_ok=True)

        printInfo("Parsing frames...")
        frameIndices = parser.iterFrameIdx()
        timestampList, csiList, magList, phaseList = parser.parseFrames(
          frameIndices,
          args.timestamp,
          args.csi,
          args.magnitude,
          args.phase,
        )

        printInfo("Saving...")
        if args.timestamp:
          filename = filePath.with_suffix(".timestamp.npy").name
          np.save(outDir / filename, timestampList)
          del timestampList
        if args.csi:
          filename = filePath.with_suffix(".csi.npy").name
          np.save(outDir / filename, csiList)
          del csiList
        if args.magnitude:
          filename = filePath.with_suffix(".mag.npy").name
          np.save(outDir / filename, magList)
          del magList
        if args.phase:
          filename = filePath.with_suffix(".phase.npy").name
          np.save(outDir / filename, phaseList)
          del phaseList

    printInfo("Done!")
