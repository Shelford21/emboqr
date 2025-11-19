# pages/2_Scan_QR.py
import streamlit as st
from pyzbar.pyzbar import decode
from PIL import Image

st.title("Page 2 — Upload QR Code to Decode")

uploaded = st.file_uploader("Upload a QR code image", type=["png", "jpg", "jpeg"])

# initialize state
if "decoded_text1" not in st.session_state:
    st.session_state.decoded_text1 = ""
if "decoded_text2" not in st.session_state:
    st.session_state.decoded_text2 = ""

if uploaded:
    img = Image.open(uploaded)

    decoded = decode(img)
    if decoded:
        data = decoded[0].data.decode("utf-8")

        # Expected format: text1|||text2
        if "|||" in data:
            t1, t2 = data.split("|||", 1)
            st.session_state.decoded_text1 = t1
            st.session_state.decoded_text2 = t2
        else:
            st.session_state.decoded_text1 = data
            st.session_state.decoded_text2 = ""
    else:
        st.error("No QR code detected.")

# Autofilled fields
text1 = st.text_input("Decoded Field 1", value=st.session_state.decoded_text1)
text2 = st.text_input("Decoded Field 2", value=st.session_state.decoded_text2)

if st.button("Submit"):
    st.success("Received:")
    st.write("Field 1:", text1)
    st.write("Field 2:", text2)
