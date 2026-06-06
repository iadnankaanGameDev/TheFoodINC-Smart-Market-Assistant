from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "model" / "model_4_1_v4_extra_best.keras"
CLASS_NAMES_PATH = BASE_DIR / "model" / "class_names_v4_1.json"
PRODUCT_INFO_PATH = BASE_DIR / "data" / "product_info.json"

IMAGE_SIZE = (224, 224)
LOW_CONFIDENCE_THRESHOLD = 0.60
MEDIUM_CONFIDENCE_THRESHOLD = 0.75
HIGH_CONFIDENCE_THRESHOLD = 0.85



LOW_RELIABILITY_CLASSES = {
    "mint",
    "chard",
    "apricot_dried",
    "parsley",
    "green_bean",
}