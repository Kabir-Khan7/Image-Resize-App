import streamlit as st
import numpy as np
from PIL import Image
import io
import cv2

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
#Edge Detection
elif selected_tool == "Edge Detection":
    st.markdown("Apply edge detection to an image.")
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        img_np = np.array(image)

        st.subheader("Orginal Image")
        st.image(image, use_container_width=True)

        st.subheader("Canny Edge Detection Setting")
        low_threshold = st.slider("Low Threshold", min_value=0, max_value= 255, value=50)
        high_threshold = st.slider("High Threshold", min_value=0, max_value= 255, value=150)

        #Convert to grayscale and apply Canny Edge Detection
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, low_threshold, high_threshold)

        st.subheader("Edge Detected Image")
        st.image(edges, clamp=True, channels="GRAY", use_container_width=True)

        #Prepare for download
        edge_imp_pil = Image.fromarray(edges)
        image_bytes = io.BytesIO()
        edge_imp_pil.save(image_bytes, format="PNG")
        image_bytes.seek(0)

        st.download_button(
            label="Download Edge Detected Image",
            data= image_bytes,
            file_name="edge_detected_image.png",
            mime="image/png"
        )
    else:
        st.info("Please upload an image to apply edge detection")
#Cropping Image
# Edge Detection Feature
elif selected_tool == "Edge Detection":
    st.markdown("Apply edge detection to an image.")
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        img_np = np.array(image)

        st.subheader("Original Image")
        st.image(image, use_container_width=True)

        st.subheader("Canny Edge Detection Setting")
        low_threshold = st.slider("Low Threshold", min_value=0, max_value=255, value=50)
        high_threshold = st.slider("High Threshold", min_value=0, max_value=255, value=150)

        # Convert to grayscale and apply Canny Edge Detection
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, low_threshold, high_threshold)

        st.subheader("Edge Detected Image")
        st.image(edges, clamp=True, channels="GRAY", use_container_width=True)

        # Prepare for download
        edge_img_pil = Image.fromarray(edges)
        image_bytes = io.BytesIO()
        edge_img_pil.save(image_bytes, format="PNG")
        image_bytes.seek(0)

        st.download_button(
            label="Download Edge Detected Image",
            data=image_bytes,
            file_name="edge_detected_image.png",
            mime="image/png"
        )
    else:
        st.info("Please upload an image to apply edge detection.")

# Crop Image Feature
elif selected_tool == "Crop Image":
    st.markdown("Upload an image and crop it by specifying pixel boundaries.")
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        img_width, img_height = image.size

        st.subheader("Original Image")
        st.image(image, caption=f"Size: {img_width}x{img_height}", use_container_width=True)

        st.subheader("Crop Settings")
        left = st.number_input("Left (px)", min_value=0, max_value=img_width - 1, value=0)
        top = st.number_input("Top (px)", min_value=0, max_value=img_height - 1, value=0)
        right = st.number_input("Right (px)", min_value=left + 1, max_value=img_width, value=img_width)
        bottom = st.number_input("Bottom (px)", min_value=top + 1, max_value=img_height, value=img_height)

        if left < right and top < bottom:
            cropped_image = image.crop((left, top, right, bottom))
            st.subheader("Cropped Image")
            st.image(cropped_image, caption=f"Cropped Size: {right - left}x{bottom - top}", use_container_width=True)

            # Download Button 
            image_bytes = io.BytesIO()
            cropped_image.save(image_bytes, format="PNG")
            image_bytes.seek(0)

            st.download_button(
                label="Download Cropped Image", 
                data=image_bytes,
                file_name="cropped_image.png",
                mime="image/png"
            )
        else: 
            st.error("Invalid crop dimensions: ensure right > left and bottom > top.")
    else: 
        st.info("Please upload an image to crop it.")
