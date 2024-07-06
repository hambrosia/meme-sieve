#!/usr/bin/env python3

import argparse
import os
import sys
import time
from glob import glob
from pathlib import Path

import google.generativeai as genai
from PIL import Image

PROMPT = """You are a heavy social media user meme lord. You know memes like the back of your hand. Your job is to label an image as a meme: true / false.
Provide no commentary other than the word true or false.

Example 1, the image contains a meme: true
Example 2, the image does not contain a meme, it is a normal photograph: false
"""

def generate_text_using_image(prompt, image_path, model_name, sleep_time=4):
    """Sleep time of 4 keeps usage under the free tier limit of 15 requests per minute for gemini 1.5 flash."""
    start = time.perf_counter()
    model = genai.GenerativeModel(model_name=model_name, system_instruction=prompt)

    response = model.generate_content(contents=[Image.open(image_path)])

    end = time.perf_counter()
    duration = end - start
    time.sleep(sleep_time - duration if duration < sleep_time else 0)
    return response.text


def main():
    parser = argparse.ArgumentParser(prog="Meme Sieve", description="Returns a list of filepaths for memes in the specified folder")
    parser.add_argument("-s", "--source_folder", default=".", type=str, help="The source folder path containing the files to be checked for memes")
    parser.add_argument("-d", "--delay", default=4, type=int, help="The amount of seconds to wait between each examined file. This helps the tool stay within the free tier for the Gemini Flash model")
    parser.add_argument('-e', '--extensions', nargs="+", default=["jpg", "png", "gif"], help="The extensions to include in the searched files.")
    parser.add_argument('-m', '--model', default="gemini-1.5-flash-latest", type=str, help="The Google Gemini model to use." )

    args = parser.parse_args()

    try:
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    except Exception:
        sys.exit("Error: GOOGLE_API_KEY env var must be set with a valid Google API key.")
        
    file_paths = []
    for ext in args.extensions:
        file_paths += glob(f"{args.source_folder}/*.{ext.lower()}")
        file_paths += glob(f"{args.source_folder}/*.{ext.upper()}")


    if not file_paths:
        sys.exit("Error: No image files found in the specified folder with the specified extensions.")

    for path in file_paths:
        res_text = generate_text_using_image(prompt=PROMPT, image_path=path, model_name=args.model, sleep_time=args.delay)
        if "true" in res_text:
            if args.source_folder == ".":
                print(Path(path).name)
            else:
                print(os.path.abspath(path))


if __name__ == "__main__":
    main()