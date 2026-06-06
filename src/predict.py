import json
import numpy as np
import tensorflow as tf

from .config import (
    MODEL_PATH,
    CLASS_NAMES_PATH,
    LOW_CONFIDENCE_THRESHOLD,
    LOW_RELIABILITY_CLASSES,
)
from .preprocessing import preprocess_image


_model = None
_class_names = None


def load_class_names():
    global _class_names

    if _class_names is None:
        with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as f:
            _class_names = json.load(f)

    return _class_names


def load_thefoodinc_model():
    global _model

    if _model is None:
        _model = tf.keras.models.load_model(MODEL_PATH)

    return _model


def predict_top_k(image, k=5):
    model = load_thefoodinc_model()
    class_names = load_class_names()

    image_tensor = preprocess_image(image)

    preds = model.predict(image_tensor, verbose=0)[0]

    top_indices = np.argsort(preds)[::-1][:k]

    top_predictions = []
    for idx in top_indices:
        class_name = class_names[idx]
        confidence = float(preds[idx])

        top_predictions.append(
            {
                "class_name": class_name,
                "confidence": confidence,
                "confidence_percent": round(confidence * 100, 2),
            }
        )

    best_prediction = top_predictions[0]
    best_class = best_prediction["class_name"]
    best_confidence = best_prediction["confidence"]

    is_uncertain = best_confidence < LOW_CONFIDENCE_THRESHOLD
    is_low_reliability = best_class in LOW_RELIABILITY_CLASSES

    return {
        "best_prediction": best_prediction,
        "top_predictions": top_predictions,
        "is_uncertain": is_uncertain,
        "is_low_reliability": is_low_reliability,
    }