import time

from classifiers.classifier_base import ClassifierBase
from PIL import Image
from transformers import AutoModelForCausalLM, AutoTokenizer


class MoondreamClassifier(ClassifierBase):
    def generate_text_using_image(self, prompt, image_path, model_name, sleep_time=4):
        start = time.perf_counter()

        # TODO() update classifier base to accept model name and version separately
        model_id = "vikhyatk/moondream2"
        revision = "2024-05-20"
        model = AutoModelForCausalLM.from_pretrained(
            model_id, trust_remote_code=True, revision=revision
        )
        tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)

        image = Image.open(image_path)
        enc_image = model.encode_image(image)
        response = model.answer_question(enc_image, prompt, tokenizer)
        
        end = time.perf_counter()
        duration = end - start
        time.sleep(sleep_time - duration if duration < sleep_time else 0)
        return response
