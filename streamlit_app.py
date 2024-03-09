import base64
import os
import streamlit as st
from PIL import Image
import requests
import app_config as app_config    # Import configuration
from utils.image_utils import resize_image, calculate_similarity  # Import image utilities
import cv2

# Import style from CSS file
def load_css(file_path):
    with open(file_path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style/style.css")

@st.cache_data ()
def get_img_as_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Get relative paths for images
main_img_path = os.path.join("images", "main1.jpeg")
left_img_path = os.path.join("images", "left1.jpeg")

# Convert images to base64
main_img = get_img_as_base64(main_img_path)
left_img = get_img_as_base64(left_img_path)

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("data:image/png;base64,{main_img}");
}}

[data-testid="stSidebar"] > div:first-child {{
background-image: url("data:image/png;base64,{left_img}");
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

def image_loading(path):
    try:
        original_img = Image.open(requests.get(path, stream=True).raw)
    except Exception as e:
        st.error(f'Error loading the original image: {str(e)}')
        return None, None

    original_img = resize_image(original_img, 300, 300)  # Resize original image
    st.image(original_img, caption='Original Image', width=200)

    tampered_img = st.file_uploader('###### Upload a tampered image', type=['jpg', 'png', 'jpeg'])
    if tampered_img is not None:
        try:
            tampered_img = Image.open(tampered_img)
            tampered_img = resize_image(tampered_img, 300, 300)  # Resize tampered image
            st.image(tampered_img, caption='Uploaded Tampered Image (Resized)', width=200)
        except Exception as e:
            st.error(f"Error loading the tampered image: {str(e)}")
            return None, None

    return original_img, tampered_img

def main():
    option = st.selectbox('###### Choose an option:', ['Select', 'Pan Card', 'AADHAR Card', 'Other'])
    if option == 'Pan Card':
        st.title('Pan Card Tampering Detector')
        original_img, tampered_img = image_loading(app_config.DEFAULT_PAN_CARD_IMAGE_URL)
        if original_img is not None and tampered_img is not None:
            score = calculate_similarity(original_img, tampered_img)
            if score < app_config.TAMPERING_THRESHOLD:
                st.error('###### This image is likely tampered!')
            else:
                st.success('###### This image appears to be authentic.')
            similarity_percent = score * 100
            st.write("###### Similarity Score: " + f"<span style='color:red'><b>{int(similarity_percent)}%</b></span>", unsafe_allow_html=True)

if __name__ == '__main__':
    main()
