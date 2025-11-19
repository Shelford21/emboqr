# pages/2_Scan_QR.py
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import av
import cv2
import numpy as np

st.title("Page 2 — Scan QR using Camera (OpenCV)")

st.markdown("""
This page uses the browser camera and OpenCV's `QRCodeDetector` (no `zbar` needed).
If deployed to Streamlit Cloud, make sure camera permission is allowed in the app settings.
""")

# init session keys
if "decoded_text1" not in st.session_state:
    st.session_state.decoded_text1 = ""
if "decoded_text2" not in st.session_state:
    st.session_state.decoded_text2 = ""

qr_detector = cv2.QRCodeDetector()

def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
    img = frame.to_ndarray(format="bgr24")

    # detect & decode
    try:
        data, bbox, _ = qr_detector.detectAndDecode(img)
    except Exception:
        data = ""

    if data:
        # expected format: part1|||part2
        if "|||" in data:
            t1, t2 = data.split("|||", 1)
            st.session_state.decoded_text1 = t1
            st.session_state.decoded_text2 = t2
        else:
            # if format differs, put the whole string in text1
            st.session_state.decoded_text1 = data
            st.session_state.decoded_text2 = ""

    # optionally draw bbox
    if bbox is not None and len(bbox) > 0:
        pts = np.int32(bbox).reshape(-1, 2)
        for i in range(len(pts)):
            pt1 = tuple(pts[i])
            pt2 = tuple(pts[(i + 1) % len(pts)])
            cv2.line(img, pt1, pt2, (0, 255, 0), 2)

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
    # add your save-to-Google-Sheets or other logic here
