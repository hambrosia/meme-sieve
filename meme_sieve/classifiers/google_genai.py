import os
import sys
import time

import google.generativeai as genai
from classifiers.classifier_base import ClassifierBase
from PIL import Image


class GoogleGenAIClassifier(ClassifierBase):
    def __init__(self):
        super().__init__()
        try:
            genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
        except KeyError as e:
            sys.exit("Error: When using Gemini model, GOOGLE_API_KEY env var must be set with a valid Google API key.")

    def generate_text_using_image(self, prompt, image_path, model_name, model_version, sleep_time=4):
        """Sleep time of 4 keeps usage under the free tier limit of 15 requests per minute for gemini 1.5 flash."""
        start = time.perf_counter()

        complete_name = f"{model_name}-{model_version}"
        model = genai.GenerativeModel(model_name=complete_name, system_instruction=prompt)

        response = model.generate_content(contents=[Image.open(image_path)])

        end = time.perf_counter()
        duration = end - start
        time.sleep(sleep_time - duration if duration < sleep_time else 0)
        return response.text
