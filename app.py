import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

# Set Page Config
st.set_page_config(page_title="Photo Shop Editor", layout="centered")

# Sidebar menu
st.sidebar.title("🛠️ Tools")
selected_tool = st.sidebar.radio(
    "Select a feature:", 
    ["Resize Image", "Convert Format", "Crop Image", "Edge Detection", "Apply Filter"],
    index=0
)

# Title
st.title("📸 Photo Shop Editor")

# Resize Image Feature
if selected_tool == "Resize Image":
    st.markdown("Upload an image, resize it, and download the resized image.")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        # Load image
        img = Image.open(uploaded_file)
        img = np.array(img)
        img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # Original Size
        original_height, original_width = img.shape[:2]
        st.subheader("Original Image")
        st.image(img, caption=f"Original Size: {original_width}x{original_height}", use_container_width=True)

        # Resize options
        st.subheader("Resize Options")
        new_width = st.number_input("Select Width", min_value=50, max_value=2000, value=450, step=10)
        new_height = st.number_input("Select Height", min_value=50, max_value=2000, value=270, step=10)

        # Resize and Convert
        resized_img = cv2.resize(img_bgr, (new_width, new_height))
        resized_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)

        # Show resized image
        st.subheader("Resized Image")
        st.image(resized_img, caption=f"Resized Size: {new_width}x{new_height}")

        # Shape Info
        st.text(f"Original Shape: {img_bgr.shape}")
        st.text(f"Resized Shape: {resized_img.shape}")

        # Download
        is_success, buffer = cv2.imencode(".jpg", resized_img)
        io_buf = io.BytesIO(buffer)

        st.download_button(
            label="Download Resized Image",
            data=io_buf,
            file_name="resized_img.jpg",
            mime="image/jpeg"
        )
    else:
        st.info("Please upload an image to get started.")

# Convert Format Feature
elif selected_tool == "Convert Format":
    st.markdown("Upload an image and convert it to another format.")

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp", "pdf", "eps", "psd"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)

        st.image(image, caption="Original Image", use_container_width=True)

        format_options = ["JPEG", "PNG", "GIF", "TIFF", "WEBP", "BMP", "PDF", "EPS", "PSD"]
        selected_format = st.selectbox("Select Format", format_options)

        file_extension = selected_format.lower()
        converted_file_name = f"converted_image.{file_extension}"

        # Convert and download
        image_bytes = io.BytesIO()

        # PIL cannot save RGBA as JPEG or PDF; convert it
        if selected_format in ["JPEG", "PDF"] and image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

        try:
            image.save(image_bytes, format=selected_format)
            image_bytes.seek(0)

            st.download_button(
                label=f"Download as {selected_format}",
                data=image_bytes,
                file_name=converted_file_name,
                mime=f"image/{file_extension if selected_format != 'PDF' else 'pdf'}"
            )
        except Exception as e:
            st.error(f"❌ Could not convert image: {str(e)}")
    else:
        st.info("Please upload an image to start converting.")
