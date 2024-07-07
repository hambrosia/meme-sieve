import time
from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image
import torch
from classifiers.classifier_base import ClassifierBase

def detect_device():
    """
    Detects the appropriate device to run on, and return the device and dtype.
    """
    if torch.cuda.is_available():
        return torch.device("cuda"), torch.float16
    elif torch.backends.mps.is_available():
        return torch.device("mps"), torch.float16
    else:
        return torch.device("cpu"), torch.float32

class MoondreamClassifier(ClassifierBase):
    def generate_text_using_image(self, prompt, image_path, model_name, sleep_time=4):
        start = time.perf_counter()

        # TODO() update cli args to accept cpu/gpu

        device, dtype = detect_device()
        if device != torch.device("cpu"):
            print("Using device:", device)
            print("If you run into issues, pass the `--cpu` flag to this script.")
            print()

        # TODO() update classifier base to accept model name and version separately
        model_id = "vikhyatk/moondream2"
        revision = "2024-05-20"

        model = AutoModelForCausalLM.from_pretrained(
            model_id, trust_remote_code=True, revision=revision, torch_dtype=dtype,
            ).to(device=device)
        model.eval()
        
        tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)
        image = Image.open(image_path)
        enc_image = model.encode_image(image)
        response = model.answer_question(enc_image, "Return 'true' if this image is a meme, 'false' if not a meme", tokenizer)

        end = time.perf_counter()
        duration = end - start
        time.sleep(sleep_time - duration if duration < sleep_time else 0)
        return response.lower()
