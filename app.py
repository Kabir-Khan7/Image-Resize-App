import streamlit as st
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
        # Load image using PIL
        img_pil = Image.open(uploaded_file)
        img_np = np.array(img_pil)

        original_width, original_height = img_pil.size
        st.subheader("Original Image")
        st.image(img_pil, caption=f"Original Size: {original_width}x{original_height}", use_container_width=True)

        # Resize options
        st.subheader("Resize Options")
        new_width = st.number_input("Select Width", min_value=50, max_value=2000, value=450, step=10)
        new_height = st.number_input("Select Height", min_value=50, max_value=2000, value=270, step=10)

        # Resize using PIL (preserve color accuracy)
        resized_img = img_pil.resize((new_width, new_height), Image.LANCZOS)

        # Show resized image
        st.subheader("Resized Image")
        st.image(resized_img, caption=f"Resized Size: {new_width}x{new_height}")

        st.text(f"Original Shape: {img_np.shape}")
        st.text(f"Resized Shape: {np.array(resized_img).shape}")

        # Download resized image
        image_bytes = io.BytesIO()
        resized_img.save(image_bytes, format="JPEG", quality=95)
        image_bytes.seek(0)

        st.download_button(
            label="Download Resized Image",
            data=image_bytes,
            file_name="resized_img.jpg",
            mime="image/jpeg"
        )
    else:
        st.info("Please upload an image to get started.")

# Convert Format Feature
elif selected_tool == "Convert Format":
    st.markdown("Upload an image and convert it to another format.")

    uploaded_file = st.file_uploader(
        "Upload an image", 
        type=["jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp", "pdf", "eps"]
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Original Image", use_container_width=True)

        format_options = ["JPEG", "PNG", "GIF", "TIFF", "WEBP", "BMP", "PDF", "EPS"]
        selected_format = st.selectbox("Select Format", format_options)

        file_extension = selected_format.lower()
        converted_file_name = f"converted_image.{file_extension}"

        # Convert image mode if needed
        if selected_format in ["JPEG", "PDF"] and image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

        # Convert and download
        image_bytes = io.BytesIO()
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
