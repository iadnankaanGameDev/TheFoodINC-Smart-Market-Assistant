import numpy as np
from PIL import Image
from .config import IMAGE_SIZE


def preprocess_image(image: Image.Image) -> np.ndarray:
    """
    PIL image -> model input tensor
    Output shape: (1, 224, 224, 3)
    """

    image = image.convert("RGB")
    image = image.resize(IMAGE_SIZE)

    image_array = np.array(image).astype("float32")

    # EfficientNetV2 preprocessing konusu kritik.
    # Eğer model eğitiminde ayrıca Rescaling(1./255) kullanmadıysan,
    # şimdilik raw 0-255 float32 bırakıyoruz.
    image_array = np.expand_dims(image_array, axis=0)

    return image_array