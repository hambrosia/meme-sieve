from classifiers.google_genai import GoogleGenAIClassifier
from classifiers.moondream import MoondreamClassifier
from classifiers.prompts import GEMINI_PROMPT, MOONDREAM_PROMPT

MODEL_REGISTRY = {
        "moondream": {
            "model_name": "vikhyatk/moondream2",
            "model_version": "2024-05-20",
            "prompt": MOONDREAM_PROMPT,
            "classifier": MoondreamClassifier
        },
        "gemini": {
            "model_name": "gemini-1.5-flash",
            "model_version": "latest",
            "prompt": GEMINI_PROMPT,
            "classifier": GoogleGenAIClassifier
        }
    }