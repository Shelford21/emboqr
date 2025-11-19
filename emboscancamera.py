import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import av
import cv2
import numpy as np

st.title("Page 2 — Scan QR with Camera (No ZBar)")

if "text1" not in st.session_state:
    st.session_state.text1 = ""
if "text2" not in st.session_state:
    st.session_state.text2 = ""

qr_detector = cv2.QRCodeDetector()

def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")

    # detect and decode QR
    data, bbox, _ = qr_detector.detectAndDecode(img)

    if data:
        if "|||" in data:
            t1, t2 = data.split("|||")
            st.session_state.text1 = t1
            st.session_state.text2 = t2

    return av.VideoFrame.from_ndarray(img, format="bgr24")


webrtc_streamer(
    key="qr_camera",
    mode=WebRtcMode.RECVONLY,
    video_frame_callback=video_frame_callback,
    media_stream_constraints={"video": True, "audio": False},
)

st.text_input("Decoded Text 1", st.session_state.text1)
st.text_input("Decoded Text 2", st.session_state.text2)
