#!/usr/bin/env python3

import google.generativeai as genai
import os
from glob import glob
import time
from IPython.display import Image

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])


PROMPT = """You are a gen z heavy instagram user. You know memes like the back of your hand. Your job is to label an image as a meme: true / false.
Provide no commentary other than the word true or false.

Example 1, the image contains a meme: true
Example 2, the image does not contain a meme, it is a normal photograph: false
"""

def generate_text_using_image(prompt, image_path, sleep_time=4):
    """Sleep time of 4 keeps usage under the free tier limit of 15 requests per minute for gemini 1.5 flash."""
    start = time.perf_counter()
    model = genai.GenerativeModel('gemini-1.5-flash-latest', system_instruction=prompt)

    response = model.generate_content(contents=[Image(image_path)])

    end = time.perf_counter()
    duration = end - start
    time.sleep(sleep_time - duration if duration < sleep_time else 0)
    return response.text


if __name__ == "__main__":
    folder = input("Enter folder name to check for memes. Must be in same folder as script\n")

    file_paths = glob(f"{folder}/*")
    print("Files found:\n")
    meme_index = {}
    for path in file_paths:
        res_text = generate_text_using_image(prompt=PROMPT, image_path=path)
        print(f"{path}\n{res_text}")
        meme_index[path] = True if "true" in res_text else False
    print(meme_index)    
