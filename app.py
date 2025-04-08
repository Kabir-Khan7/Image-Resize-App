import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

# Set page configuration
st.set_page_config(page_title="Image Resizer", layout="centered")

st.title("📸 Image Resizer App")
st.markdown("Upload an image, resize it, and download the resized image.")

# Image uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Convert uploaded file to OpenCV format (RGB)
    img = Image.open(uploaded_file)
    img = np.array(img)
    
    # Convert RGB to BGR for OpenCV compatibility
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Get original image dimensions
    original_height, original_width = img_bgr.shape[:2]
    
    # Display original image
    st.subheader("Original Image")
    st.image(img, caption=f"Original Size: {original_width}x{original_height}", use_container_width=True)

    # User input for new size
    st.subheader("Resize Options")
    new_width = st.number_input("Select Width", min_value=50, max_value=2000, value=450, step=10)
    new_height = st.number_input("Select Height", min_value=50, max_value=2000, value=270, step=10)

    # Resize image
    resized_img = cv2.resize(img_bgr, (new_width, new_height))

    # Convert resized image back to RGB for display in Streamlit
    resized_img_rgb = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)

    # Show resized image
    st.subheader("Resized Image")
    st.image(resized_img_rgb, caption=f"New Size: {new_width}x{new_height}", use_container_width=False)

    # Show shape details
    st.text(f"Original Shape: {img_bgr.shape}")
    st.text(f"Resized Shape: {resized_img.shape}")

    # Convert resized image to a byte array for download
    is_success, buffer = cv2.imencode(".jpg", resized_img)
    io_buf = io.BytesIO(buffer)

    # Add a download button for the resized image
    st.download_button(
        label="Download Resized Image",
        data=io_buf,
        file_name="resized_image.jpg",
        mime="image/jpeg"
    )
else:
    st.info("Please upload an image to get started.")
