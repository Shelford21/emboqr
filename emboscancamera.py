# pages/1_Generate_QR.py
import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image

st.title("Page 1 — Generate QR (two fields)")

st.markdown("Enter two values. The app will pack them into a single QR code as `value1|||value2`.")

text1 = st.text_input("Text 1")
text2 = st.text_input("Text 2")

col1, col2 = st.columns(2)
with col1:
    if st.button("Generate QR"):
        if not text1 or not text2:
            st.warning("Please fill both fields.")
        else:
            combined = f"{text1}|||{text2}"
            qr = qrcode.QRCode(box_size=8, border=2)
            qr.add_data(combined)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
            buf = BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            st.image(buf.getvalue(), caption="Generated QR code (contains both fields)", use_column_width=True)
            # provide download
            st.download_button("Download PNG", data=buf.getvalue(), file_name="qr_two_fields.png", mime="image/png")
with col2:
    st.info("Example usage:\n\n- Scan this QR on Page 2\n- Page 2 will split by `|||` and fill two fields")
    st.write("Packed format in QR:")
    st.code(f"{text1}|||{text2}")
