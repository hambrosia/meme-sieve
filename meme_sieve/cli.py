#!/usr/bin/env python3

import argparse
import os
import sys
import time
from glob import glob
from pathlib import Path

import google.generativeai as genai
from classifiers.google_genai import GoogleGenAIClassifier
from classifiers.moondream import MoondreamClassifier
from classifiers.prompts import MEME_EXPERT_MINIMAL_STRUCTURE


def main():
    parser = argparse.ArgumentParser(prog="memesieve", description="Returns a list of filepaths for memes in the specified folder")
    parser.add_argument("-s", "--source_folder", default=".", type=str, help="The source folder path containing the files to be checked for memes")
    parser.add_argument("-d", "--delay", default=4, type=int, help="The amount of seconds to wait between each examined file. This helps the tool stay within the free tier for the Gemini Flash model")
    parser.add_argument('-e', '--extensions', nargs="+", default=["jpg", "jpeg", "png", "gif"], help="The extensions to include in the searched files.")
    parser.add_argument('-m', '--model', default="gemini-1.5-flash-latest", type=str, help="The Google Gemini model to use." )

    args = parser.parse_args()

    try:
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    except KeyError as e:
        sys.exit("Error: GOOGLE_API_KEY env var must be set with a valid Google API key.")
        
    file_paths = []
    for ext in args.extensions:
        file_paths += glob(f"{args.source_folder}/*.{ext.lower()}")
        file_paths += glob(f"{args.source_folder}/*.{ext.upper()}")


    if not file_paths:
        sys.exit("Error: No image files found in the specified folder with the specified extensions.")

    for path in file_paths:
        res_text = MoondreamClassifier().generate_text_using_image(prompt=MEME_EXPERT_MINIMAL_STRUCTURE, image_path=path, model_name=args.model, sleep_time=args.delay)
        if "true" in res_text:
            if args.source_folder == ".":
                print(Path(path).name)
            else:
                print(os.path.abspath(path))

if __name__ == "__main__":
    main()