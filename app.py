import streamlit as st
import pandas as pd
from PIL import Image

from src.predict import predict_top_k
from src.info_cards import get_product_info
from src.config import (
    LOW_CONFIDENCE_THRESHOLD,
    MEDIUM_CONFIDENCE_THRESHOLD,
    HIGH_CONFIDENCE_THRESHOLD,
)


st.set_page_config(
    page_title="TheFoodINC - Smart Market Assistant",
    page_icon="🥦",
    layout="centered",
)
with st.sidebar:
    st.title("🥦 TheFoodINC")
    st.markdown("### Prototype Info")
    st.write("Version: v0.3")
    st.write("Model: EfficientNetV2B0")
    st.write("Classes: 63")
    st.write("Framework: Streamlit + TensorFlow/Keras")

    st.markdown("---")
    st.markdown("### Confidence Levels")
    st.write(f"Low: below {int(LOW_CONFIDENCE_THRESHOLD * 100)}%")
    st.write(
        f"Medium: {int(MEDIUM_CONFIDENCE_THRESHOLD * 100)}% - "
        f"{int(HIGH_CONFIDENCE_THRESHOLD * 100)}%"
    )
    st.write(f"High: {int(HIGH_CONFIDENCE_THRESHOLD * 100)}%+")

    st.markdown("---")
    st.markdown("### Known Limitations")
    st.write("- Leafy greens can be confused.")
    st.write("- Distant market photos may reduce confidence.")
    st.write("- Some visually similar products may be mixed.")
    st.write("- This is a prototype, not dietary or professional advice.")

st.title("🥦 TheFoodINC")
st.subheader("Smart Market Assistant")

st.write(
    "Bir market, manav veya pazar ürününün fotoğrafını yükle. "
    "Model ürün sınıfını tahmin eder ve güven skorunu gösterir."
)

uploaded_file = st.file_uploader(
    "Bir ürün görseli yükle",
    type=["jpg", "jpeg", "png", "webp"],
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    st.image(image, caption="Yüklenen görsel", width="stretch")

    with st.spinner("Model tahmin yapıyor..."):
        result = predict_top_k(image, k=5)

    best = result["best_prediction"]

    st.markdown("---")

    if best["confidence"] < LOW_CONFIDENCE_THRESHOLD:
        st.warning(
            f"Model bu görselden yeterince emin değil. "
            f"En yüksek tahmin: **{best['class_name']}** "
            f"({best['confidence_percent']}%). "
            f"Minimum threshold: %{int(LOW_CONFIDENCE_THRESHOLD * 100)}"
        )

    elif best["confidence"] < MEDIUM_CONFIDENCE_THRESHOLD:
        st.warning(
            f"Tahmin: **{best['class_name']}** "
            f"({best['confidence_percent']}% güven). "
            "Model düşük-orta güven seviyesinde. Top-5 alternatifleri kontrol etmek iyi olur."
        )

    elif best["confidence"] < HIGH_CONFIDENCE_THRESHOLD:
        st.info(
            f"Tahmin: **{best['class_name']}** "
            f"({best['confidence_percent']}% güven). "
            "Model makul seviyede emin ama sonuç yine de kesin kabul edilmemeli."
        )

    else:
        st.success(
            f"Tahmin: **{best['class_name']}** "
            f"({best['confidence_percent']}% güven)"
        )
    st.progress(best["confidence"])

    st.caption(
        f"Model confidence: {best['confidence_percent']}% — "
        f"low threshold: {int(LOW_CONFIDENCE_THRESHOLD * 100)}%, "
        f"medium threshold: {int(MEDIUM_CONFIDENCE_THRESHOLD * 100)}%, "
        f"high threshold: {int(HIGH_CONFIDENCE_THRESHOLD * 100)}%"
    )

    if result["is_low_reliability"]:
        st.info(
            "Bu sınıf için model hâlâ sınırlı sayıda örnekle eğitildi. "
            "Sonucu dikkatli yorumlamak iyi olur."
        )

    product_info = get_product_info(best["class_name"])

    if product_info and not result["is_uncertain"]:
        st.markdown("---")
        st.subheader(f"📌 {product_info['display_name']}")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🧾 Basic Info")
            st.write(f"**Category:** {product_info['category']}")
            st.write(f"**Calories:** {product_info['calories_per_100g']} / 100g")

        with col2:
            st.markdown("### 🧊 Storage")
            st.write(product_info["storage"])

        st.markdown("### 🍽️ Pairs Well With")
        st.write(", ".join(product_info["pairs_well_with"]))

        st.markdown("### 👨‍🍳 Recipe Ideas")
        for recipe in product_info["recipe_ideas"]:
            st.write(f"- {recipe}")

    elif product_info and result["is_uncertain"]:
        st.info(
            "Model bu görselden emin olmadığı için ürün bilgi kartı kesin sonuç gibi gösterilmiyor."
        )

        st.markdown("### 📷 Daha iyi sonuç için")
        st.write("- Ürünü daha yakından çek")
        st.write("- Mümkünse tek ürünü merkeze al")
        st.write("- Çok karışık pazar/tezgâh arka planından kaçın")
        st.write("- Işık çok düşükse daha aydınlık bir fotoğraf dene")

    elif not product_info and not result["is_uncertain"]:
        st.info(
            "Bu ürün için bilgi kartı henüz eklenmedi. Tahmin sonucu gösteriliyor."
        )

    st.subheader("Top-5 Tahmin")

    top_df = pd.DataFrame(result["top_predictions"])
    top_df = top_df[["class_name", "confidence_percent"]]
    top_df.columns = ["Sınıf", "Güven (%)"]

    st.dataframe(top_df, width="stretch")