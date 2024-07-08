import time

import torch
from classifiers.classifier_base import ClassifierBase
from PIL import Image
from transformers import AutoModelForCausalLM, AutoTokenizer


class MoondreamClassifier(ClassifierBase):
    def __init__(self):
        super().__init__()

    def generate_text_using_image(self, prompt, image_path, model_name, model_version, sleep_time=4):
        start = time.perf_counter()

        device, dtype = self._detect_device()

        model = AutoModelForCausalLM.from_pretrained(
            model_name, trust_remote_code=True, revision=model_version, torch_dtype=dtype,
        ).to(device=device)
        model.eval()

        tokenizer = AutoTokenizer.from_pretrained(
            model_name, revision=model_version)
        image = Image.open(image_path)
        enc_image = model.encode_image(image)
        response = model.answer_question(enc_image, prompt, tokenizer)

        end = time.perf_counter()
        duration = end - start
        time.sleep(sleep_time - duration if duration < sleep_time else 0)
        return response.lower()

    def _detect_device(self):
        """
        Detects the appropriate device to run on, and return the device and dtype.
        """
        if torch.cuda.is_available():
            return torch.device("cuda"), torch.float16
        elif torch.backends.mps.is_available():
            return torch.device("mps"), torch.float16
        else:
            return torch.device("cpu"), torch.float32
