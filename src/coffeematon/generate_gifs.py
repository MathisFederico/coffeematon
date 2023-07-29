import os
from pathlib import Path

import imageio.v2 as imageio
import argparse


def generate_gif(path: Path):
    path = Path(path)
    bitmaps_steps = [
        int(filename.split(".")[0])
        for filename in os.listdir(path)
        if filename.endswith(".bmp")
    ]
    bitmaps_steps.sort()
    gif_path = path.parent / f"{path.name}_bitmaps.gif"
    with imageio.get_writer(gif_path, mode="I") as writer:
        for step in bitmaps_steps:
            image = imageio.imread(path / f"{step}.bmp")
            writer.append_data(image)

    return gif_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        help="Path to the bitmaps folder. Gif will be generated alongside.",
    )
    args = parser.parse_args()
    saved_path = generate_gif(args.path)
    print(f"Successfuly saved gif at {saved_path}")
