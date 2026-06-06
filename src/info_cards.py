import json
from .config import PRODUCT_INFO_PATH


_product_info = None


def load_product_info():
    global _product_info

    if _product_info is None:
        with open(PRODUCT_INFO_PATH, "r", encoding="utf-8") as f:
            _product_info = json.load(f)

    return _product_info


def get_product_info(class_name: str):
    product_info = load_product_info()
    return product_info.get(class_name)