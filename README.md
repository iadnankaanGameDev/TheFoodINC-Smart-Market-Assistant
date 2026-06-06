# TheFoodINC — Smart Market Assistant

TheFoodINC is a computer vision prototype that classifies grocery, fruit, and vegetable images and presents useful product information to the user.

The project started as an image classification model, but evolved into a user-facing app prototype with confidence-aware predictions, Top-5 alternatives, product information cards, and uncertainty handling.

---

## Project Goal

The goal of this project is to build a smart market assistant that can help users identify products from market, grocery, or bazaar photos.

A user can upload a product image, and the app returns:

* Predicted product class
* Model confidence score
* Top-5 alternative predictions
* Product category
* Approximate calories per 100g
* Storage suggestions
* Food pairing ideas
* Recipe ideas
* Warnings for uncertain or low-reliability predictions

This project is not only a classification notebook. It is designed as a step toward a practical web/mobile grocery assistant.

---

## Current Prototype

The current version is a Streamlit web prototype.

### Current Features

* Upload a fruit, vegetable, or grocery product image
* Run prediction using a trained EfficientNetV2B0 model
* Display Top-1 prediction and confidence score
* Show Top-5 alternative predictions
* Use confidence thresholds to avoid overconfident wrong outputs
* Display product information cards for confident predictions
* Warn the user when the prediction is uncertain
* Warn the user for known low-reliability classes
* Show a sidebar with model and prototype information

---

## Demo Preview

The prototype currently supports a simple image upload workflow:

1. User uploads an image.
2. The model predicts the product class.
3. The app checks prediction confidence.
4. If confidence is high enough, a product information card is shown.
5. If confidence is low, the app warns the user and suggests taking a clearer photo.
6. Top-5 predictions are always displayed for transparency.

---

## Model

The latest model used in this prototype:

* Architecture: EfficientNetV2B0
* Approach: Transfer learning
* Input size: 224 × 224 × 3
* Number of classes: 63
* Output layer: Dense(63, softmax)
* Best validation accuracy: approximately 95.11%
* Main checkpoint: `model_4_1_v4_extra_best.keras`

---

## Dataset Development

The dataset was built through multiple iterations.

The project began with grocery/product image datasets and was later expanded by merging multiple sources, including fruit and vegetable image datasets. After initial testing, real-world market and bazaar images revealed a domain shift problem.

The model performed well on curated datasets, but some real-world images were harder:

* Distant market photos
* Multiple products in the same frame
* Bazaar/market stall images
* Leafy greens
* Similar-looking fruits and vegetables
* Images with cluttered backgrounds
* Stylized or watermarked stock photos

To improve real-world robustness, additional manually collected market-style images were added for weaker classes.

---

## Dataset Versions

### v3

* Classes: 56
* Train images: approximately 20,741
* Validation images: approximately 3,994
* Test images: approximately 3,968
* Test accuracy: approximately 97.76%

Although v3 achieved strong test accuracy, real-world custom images showed domain shift.

### v4

v4 expanded the class list and added manually collected images.

New or adjusted classes included:

* `apricot_dried`
* `celery`
* `chard`
* `green_bean`
* `parsley`
* `dill`
* `mint`

Some class name corrections were also made:

* `pepper` → `bell_pepper`
* `brocoli` → `broccoli`
* `zuchini` → `zucchini`

### v4.1

v4.1 added extra targeted images for weaker or important classes:

* `apricot_dried`
* `chard`
* `cucumber`
* `green_bean`
* `mint`
* `parsley`
* `pear`

Current v4.1 dataset size:

* Train images: approximately 21,627
* Validation images: approximately 4,236
* Classes: 63

---

## Confidence Handling

A key part of this project is not forcing the model to always give a confident answer.

The app uses confidence thresholds:

* Low confidence: below 60%
* Medium confidence: 75% - 85%
* High confidence: 85%+

If the confidence is low, the app warns the user instead of presenting the prediction as a certain result.

Example uncertain message:

> The model is not confident enough about this image. The product may be outside the dataset or the photo may not be clear enough.

This is especially important for real-world use, where users may upload unclear, distant, or unrelated images.

---

## Low Reliability Classes

Some classes are currently known to be more difficult for the model.

```python
LOW_RELIABILITY_CLASSES = {
    "mint",
    "chard",
    "apricot_dried",
    "parsley",
    "green_bean"
}
```

When one of these classes is predicted, the app displays an additional warning:

> This class was trained with a limited number of examples. Please interpret the result carefully.

This makes the app more transparent and safer for users.

---

## Product Information Cards

For confident predictions, the app displays a product information card.

Each card may include:

* Display name
* Category
* Approximate calories per 100g
* Storage suggestion
* Food pairings
* Recipe ideas

Example:

```json
{
  "display_name": "Cucumber",
  "category": "Vegetable",
  "calories_per_100g": "15 kcal",
  "storage": "Keep refrigerated, preferably wrapped or in a container to reduce moisture loss.",
  "pairs_well_with": ["tomato", "yogurt", "mint", "lemon", "dill"],
  "recipe_ideas": ["Cacık", "Cucumber salad", "Fresh sandwich"]
}
```

Product information is stored in:

```text
data/product_info.json
```

---

## Project Structure

```text
thefoodinc_app/
│
├── app.py
├── README.md
├── requirements.txt
├── manual_test_log.md
│
├── model/
│   ├── model_4_1_v4_extra_best.keras
│   └── class_names_v4_1.json
│
├── data/
│   └── product_info.json
│
├── src/
│   ├── config.py
│   ├── info_cards.py
│   ├── predict.py
│   └── preprocessing.py
│
└── assets/
    └── sample_images/
```

---

## How to Run

### 1. Clone or download the project

```bash
git clone <repository-url>
cd thefoodinc_app
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Windows:

```bash
.venv\Scripts\activate
```

macOS / Linux:

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Run the app

```bash
python -m streamlit run app.py
```

The app will open in the browser, usually at:

```text
http://localhost:8501
```

---

## Manual Testing Notes

Some manual tests showed strong results:

* Pear: high-confidence correct prediction
* Cucumber: high-confidence correct prediction
* Mushroom: high-confidence correct prediction
* Onion: correct prediction with medium confidence

Known issues:

* Green plum-like images may not be recognized reliably
* Leafy greens such as mint, parsley, and chard may be confused
* Distant market photos may reduce confidence
* Some visually similar products may appear in Top-5 alternatives

These issues are tracked in:

```text
manual_test_log.md
```

---

## Known Limitations

This is an educational and portfolio prototype.

Current limitations:

* The model may confuse visually similar products.
* Leafy greens are still challenging.
* Some market/bazaar images create domain shift.
* Product information cards contain approximate nutritional values.
* The app should not be used for medical, dietary, or professional advice.
* The model only recognizes classes included in the training dataset.

---

## Next Steps

Possible next improvements:

* Improve weak classes with more manually curated images
* Add more real-world market/bazaar images
* Add object detection for images containing multiple products
* Add camera input for mobile use
* Convert the model to TensorFlow Lite for on-device mobile inference
* Build a Flutter mobile interface
* Add FastAPI backend for model serving
* Add better unknown/out-of-dataset detection
* Add multilingual product cards
* Add richer recipe recommendations

---

## Why This Project Matters

TheFoodINC is more than a simple image classification demo.

The project includes:

* Transfer learning with EfficientNetV2B0
* Dataset merging and class mapping
* Real-world domain shift analysis
* Manual data collection for weak classes
* Confidence thresholding
* Top-5 prediction transparency
* Low-reliability class warnings
* User-facing Streamlit app design
* Product information cards
* Manual testing and known limitation tracking

This makes the project closer to a real applied machine learning product workflow rather than a standalone notebook experiment.

---

## Model File

The trained `.keras` model file is required to run the app locally.

Expected path:

```text
model/model_4_1_v4_extra_best.keras

## Disclaimer

This app is a prototype. Predictions and nutritional information are approximate and may be incorrect. The app should not be used as professional dietary, medical, or safety advice.
