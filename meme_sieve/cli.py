#!/usr/bin/env python3

import argparse
import os
import sys
import time
from glob import glob
from pathlib import Path

from classifiers.registry import MODEL_REGISTRY


def main():
    parser = argparse.ArgumentParser(prog="memesieve", description="Returns a list of filepaths for memes in the specified folder.")
    parser.add_argument("-s", "--source_folder", default=".", type=str, help="The source folder path containing the files to be checked for memes.")
    parser.add_argument("-d", "--delay", default=4, type=int, help="The amount of seconds to wait between each examined file.")
    parser.add_argument('-e', '--extensions', nargs="+", default=["jpg", "jpeg", "png", "gif"], help="The extensions to include in the searched files.")
    parser.add_argument('-m', '--model', choices=['moondream', 'gemini'], default="moondream", type=str, help="The name of the model to use." )

    args = parser.parse_args()

    file_paths = []
    for ext in args.extensions:
        file_paths += glob(f"{args.source_folder}/*.{ext.lower()}")
        file_paths += glob(f"{args.source_folder}/*.{ext.upper()}")

    if not file_paths:
        sys.exit("Error: No image files found in the specified folder with the specified extensions.")

    for path in file_paths:
        classifier = MODEL_REGISTRY[args.model]["classifier"]()

        res_text = classifier.generate_text_using_image(
            prompt=MODEL_REGISTRY[args.model]["prompt"], 
            image_path=path, 
            model_name=MODEL_REGISTRY[args.model]["model_name"],
            model_version=MODEL_REGISTRY[args.model]["model_version"],
            sleep_time=args.delay
        )

        if "true" in res_text:
            if args.source_folder == ".":
                print(Path(path).name)
            else:
                print(os.path.abspath(path))

if __name__ == "__main__":
    main()