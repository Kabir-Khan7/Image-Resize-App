import streamlit as st
import cv2
import numpy as np
from PIL import Image 
import io

#Set Page Config
st.set_page_config(page_title="Photo Shop Editor", layout="centered")

#Sidebar menu
st.sidebar.title("🛠️ Tools")
selected_tool = st.sidebar.radio(
    "Select a feature:", 
    ["Resize Image", "Convert Format", "Crop Image", "Edge Detection" "Apply Filter"],
    index=0
)

#Tile
st.title("📸 Photo Shop Editor")

#Resize Image Feature
if selected_tool == "Resize Image":
    st.markdown("Upload an image, resize it, and download the resized image.")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        #Load image
        img = Image.open(uploaded_file)
        img = np.array(img)
        img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        #Orginal Size
        orginal_height, orginal_width = img.shape[:2]
        st.subheader('Orginal Image')
        st.image(img, caption=f"Orginal Size: {orginal_width}x{orginal_height}", use_container_width=True)

        #Resize options
        st.subheader("Resize Options")
        new_width = st.number_input("Select Width", min_value=50, max_value=2000, value=450, step=10)
        new_height = st.number_input("Select Height", min_value=50, max_value=2000, value=270, step=10)

        #Resize and Convert
        resized_img = cv2.resize(img_bgr, (new_width, new_height))
        resized_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)

        #Show resized image
        st.subheader('Resized Image')
        st.image(resized_img, caption=f"Resized Size: {new_width}x{new_height}")

        #Shape Info
        st.text(f"Orginal Shape: {img_bgr.shape}")
        st.text(f"Resized Shape: {resized_img.shape}")

        #Download
        is_success, buffer = cv2.imencode(".jpg", resized_img)
        io_buf = io.BytesIO(buffer)

        st.download_button(
            label="Download Resized Image",
            data=io_buf
            file_name="resized_img.jpg"
            mime="image/jpeg"
        )
    else:
        st.info("Please upload an image to get started.")

#Placeholder for convert format
elif selected_tool == "Convert Format":
    st.markdown("This feature is under construction. Stay tuned for updates!")
    