import os
import urllib.parse
import requests
import streamlit as st
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

def get_secret(name):
    if name in st.secrets:
        return st.secrets[name]
    return os.getenv(name)

HF_API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
HF_TOKEN = get_secret("HF_TOKEN")

def generate_image(prompt):
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&seed=42"

        response = requests.get(url, timeout=45)

        if response.status_code == 200:
            return response.content, None
        else:
            return None, f"Сервіс тимчасово непрацює ({response.status_code})"
    except requests.exceptions.Timeout:
        return None, "Time-out"
    except Exception as e:
        return None, f"Помилка підключення: {e}"

st.title("AI Creative Studio")
st.write("Напиши яке зображення хочеш отримати - ШІ створить його безкоштовно")

prompt = st.text_area("Опис зображення (промпт)", placeholder="Наприклад: логотип кафе у формі зерна")

STYLES = {

    "Без стилю (як написано)": "",

    "Реалістичне фото": (
        ", photorealistic photography, highly realistic textures and materials, "
        "natural skin and hair details, realistic proportions, physically accurate lighting, "
        "soft natural shadows, realistic depth of field, sharp focus, high detail, "
        "professional camera quality, authentic colors, no illustration, no cartoon"
    ),

    "Акварель": (
        ", delicate watercolor illustration, hand-painted appearance, "
        "soft translucent watercolor washes, visible paper texture, gentle brush strokes, "
        "subtle color blending, slightly imperfect painted edges, pastel color palette, "
        "soft natural lighting, artistic and elegant composition, traditional watercolor paper"
    ),

    "Мультфільм": (
        ", polished 3D animated movie style, stylized but detailed characters, "
        "appealing expressive faces, smooth clean shapes, vibrant but balanced colors, "
        "soft cinematic lighting, gentle ambient occlusion, detailed 3D textures, "
        "rounded forms, charming friendly appearance, high-quality animation render, "
        "cinematic composition"
    ),

    "Аніме": (
        ", high-quality Japanese anime art style, detailed anime character design, "
        "expressive large eyes, clean line art, carefully rendered hair, "
        "stylized facial features, detailed clothing, dynamic composition, "
        "cel shading, soft highlights, vibrant colors, atmospheric background, "
        "beautiful cinematic lighting, polished anime illustration, highly detailed"
    ),

    "Гаррі Поттер": (
        ", magical dark-academia fantasy atmosphere, old British wizarding school aesthetic, "
        "ancient stone castle, gothic architecture, enchanted candles, floating lights, "
        "mysterious magical atmosphere, spell books, potion bottles, vintage school robes, "
        "deep atmospheric lighting, warm candlelight mixed with cool shadows, "
        "misty cinematic environment, richly detailed fantasy world, "
        "realistic magical effects, cinematic fantasy photography"
    ),

}
style_choice = st.selectbox("Вибери стиль зображення:", list(STYLES.keys()))

if st.button("Сгенерувати зображення") and prompt:
    final_prompt = prompt + STYLES[style_choice]

    with st.spinner("AI створює зображення"):
        image_bytes, error = generate_image(final_prompt)

    if error:
        st.error(f"Не вдалося сгенерувати зображення: {error}")
    elif image_bytes:
        st.image(image_bytes, caption=f"Стиль: {style_choice}", use_container_width=True)
        st.session_state["last_image"] = image_bytes

if "last_image" in st.session_state:
    st.download_button(
        label="Завантажити фото",
        data=st.session_state["last_image"],
        file_name="ai_studio_result.png",
        mime="image/png"
    )