import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import av
import cv2
import numpy as np
from pyzbar.pyzbar import decode, ZBarSymbol

st.title("Page 2 — Stable QR Scanner (pyzbar)")

if "decoded_text1" not in st.session_state:
    st.session_state.decoded_text1 = ""
if "decoded_text2" not in st.session_state:
    st.session_state.decoded_text2 = ""

def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
    try:
        img = frame.to_ndarray(format="bgr24")
    except Exception:
        return frame  # fail safely

    # Convert to grayscale for pyzbar
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    except Exception:
        return frame  # fail safely

    try:
        decoded_list = decode(gray, symbols=[ZBarSymbol.QRCODE])
    except Exception:
        decoded_list = []

    if decoded_list:
        qr = decoded_list[0]

        try:
            data = qr.data.decode("utf-8")
        except Exception:
            data = ""

        if "|||" in data:
            t1, t2 = data.split("|||", 1)
        else:
            t1, t2 = data, ""

        st.session_state.decoded_text1 = t1
        st.session_state.decoded_text2 = t2

        # draw polygon safely
        try:
            pts = qr.polygon
            if pts and len(pts) >= 4:
                pts = np.array([(p.x, p.y) for p in pts], dtype=np.int32)
                cv2.polylines(img, [pts], True, (0, 255, 0), 2)
        except:
            pass

    # ALWAYS return a valid frame
    try:
        return av.VideoFrame.from_ndarray(img, format="bgr24")
    except:
        return frame
