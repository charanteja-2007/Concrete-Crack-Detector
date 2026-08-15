

import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

st.set_page_config(page_title="AI Concrete Crack Detector", layout="centered")

@st.cache_resource
def load_model():
    return tf.keras.models.load_model('crack_detector.h5')

model = load_model()

st.title("AI-Powered Concrete Crack Detector")
st.write("Upload an image of a concrete surface (wall, pavement, beam) to check for cracks.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file).convert('RGB')
    st.image(img, caption='Uploaded Image', use_container_width=True)

    with st.spinner('🔍 Please wait, Crack Detector is analyzing the image...'):
        img_resized = img.resize((128, 128))
        img_array = np.array(img_resized) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        pred = model.predict(img_array)[0][0]

    if pred > 0.5:
        st.error(f"⚠️ Crack Detected — Confidence: {pred:.2%}")
    else:
        st.success(f"✅ No Crack Detected — Confidence: {(1-pred):.2%}")

st.markdown("---")
st.caption("Model: MobileNetV2 (transfer learning) | Trained on 40,000+ labeled concrete images")