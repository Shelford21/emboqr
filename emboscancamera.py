# pages/2_Scan_QR.py
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import av
import cv2
import numpy as np
from pyzbar.pyzbar import decode

st.title("Page 2 — Scan QR using Camera (ZBAR / pyzbar)")

st.markdown("""
Using **pyzbar** + ZBar C library  
(ensure `libzbar0` & `libzbar-dev` are in `packages.txt`)
""")

# init session keys
if "decoded_text1" not in st.session_state:
    st.session_state.decoded_text1 = ""
if "decoded_text2" not in st.session_state:
    st.session_state.decoded_text2 = ""

def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
    img = frame.to_ndarray(format="bgr24")

    # Convert image to grayscale for pyzbar
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    decoded = decode(gray)

    if decoded:
        qr = decoded[0]
        data = qr.data.decode("utf-8")

        # expected format: part1|||part2
        if "|||" in data:
            t1, t2 = data.split("|||", 1)
            st.session_state.decoded_text1 = t1
            st.session_state.decoded_text2 = t2
        else:
            st.session_state.decoded_text1 = data
            st.session_state.decoded_text2 = ""

        # draw bounding box
        pts = qr.polygon
        pts = np.array([(p.x, p.y) for p in pts], dtype=np.int32)

        cv2.polylines(img, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

    return av.VideoFrame.from_ndarray(img, format="bgr24")

# Use a public TURN server to avoid RTC negotiation issues on Cloud
rtc_conf = {
    "iceServers": [
        {"urls": ["stun:stun.l.google.com:19302"]},
        {
            "urls": "turn:global.relay.metered.ca:80",
            "username": "open",
            "credential": "open",
        },
    ]
}

webrtc_ctx = webrtc_streamer(
    key="qr_camera",
    mode=WebRtcMode.RECVONLY,
    video_frame_callback=video_frame_callback,
    media_stream_constraints={"video": True, "audio": False},
    rtc_configuration=rtc_conf,
)

st.markdown("**Decoded fields (auto-filled):**")
c1, c2 = st.columns(2)

with c1:
    text1 = st.text_input("Decoded Text 1", value=st.session_state.decoded_text1, key="decoded1")
with c2:
    text2 = st.text_input("Decoded Text 2", value=st.session_state.decoded_text2, key="decoded2")

if st.button("Submit scanned values"):
    st.success("Submitted:")
    st.write("Text 1:", text1)
    st.write("Text 2:", text2)
    # You can add Google Sheets / database upload here
