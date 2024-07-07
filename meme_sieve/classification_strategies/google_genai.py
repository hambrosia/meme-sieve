import time
import google.generativeai as genai
from classification_strategies.classifier_base import ClassifierBase
from PIL import Image

class GoogleGenAIClassifier(ClassifierBase):
    def generate_text_using_image(self, prompt, image_path, model_name, sleep_time=4):
        """Sleep time of 4 keeps usage under the free tier limit of 15 requests per minute for gemini 1.5 flash."""
        start = time.perf_counter()
        model = genai.GenerativeModel(model_name=model_name, system_instruction=prompt)

        response = model.generate_content(contents=[Image.open(image_path)])

        end = time.perf_counter()
        duration = end - start
        time.sleep(sleep_time - duration if duration < sleep_time else 0)
        return response.text
