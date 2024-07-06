#!/usr/bin/env python3

import google.generativeai as genai
import os
from glob import glob
import time
from PIL import Image
import argparse
from pathlib import Path
import sys



PROMPT = """You are a gen z heavy instagram user. You know memes like the back of your hand. Your job is to label an image as a meme: true / false.
Provide no commentary other than the word true or false.

Example 1, the image contains a meme: true
Example 2, the image does not contain a meme, it is a normal photograph: false
"""

def generate_text_using_image(prompt, image_path, sleep_time=4):
    """Sleep time of 4 keeps usage under the free tier limit of 15 requests per minute for gemini 1.5 flash."""
    start = time.perf_counter()
    model = genai.GenerativeModel('gemini-1.5-flash-latest', system_instruction=prompt)

    response = model.generate_content(contents=[Image.open(image_path)])

    end = time.perf_counter()
    duration = end - start
    time.sleep(sleep_time - duration if duration < sleep_time else 0)
    return response.text


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Meme Sieve", description="Returns a list of filepaths for memes in the specified folder")
    parser.add_argument("-s", "--source_folder", default=".", type=str, help="The source folder path containing the files to be checked for memes")
    parser.add_argument("-d", "--delay", default=4, type=int, help="The amount of seconds to wait between each examined file. This helps the tool stay within thre free tier for the Gemini Flash model")

    args = parser.parse_args()
    file_paths = glob(f"{args.source_folder}/*")

    try:
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    except Exception:
        sys.exit("Error: GOOGLE_API_KEY env var must be set with a valid Google API key.")
        
    
    for path in file_paths:
        res_text = generate_text_using_image(prompt=PROMPT, image_path=path, sleep_time=args.delay)
        if "true" in res_text:
            if args.source_folder == ".":
                print(Path(path).name)
            else:
                print(path)
