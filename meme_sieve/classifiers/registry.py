from classifiers.google_genai import GoogleGenAIClassifier
from classifiers.moondream import MoondreamClassifier
from classifiers.prompts import DEFAULT_PROMPT

MODEL_REGISTRY = {
    "moondream": {
        "model_name": "vikhyatk/moondream2",
        "model_version": "2024-05-20",
        "prompt": DEFAULT_PROMPT,
        "classifier": MoondreamClassifier,
        "default_delay": 0
    },
    "gemini": {
        "model_name": "gemini-1.5-flash",
        "model_version": "latest",
        "prompt": DEFAULT_PROMPT,
        "classifier": GoogleGenAIClassifier,
        "default_delay": 4
    }
}
