import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import av
import cv2
import numpy as np
from pyzbar.pyzbar import decode, ZBarSymbol

st.title("QR Scanner Page")

if "decoded_text1" not in st.session_state:
    st.session_state.decoded_text1 = ""
if "decoded_text2" not in st.session_state:
    st.session_state.decoded_text2 = ""

# TURN + STUN CONFIG (important for Streamlit Cloud)
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

def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
    # ALWAYS SAFE FRAME
    try:
        img = frame.to_ndarray(format="bgr24")
    except:
        return frame

    # Convert to grayscale
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    except:
        return frame

    # Decode QR
    try:
        decoded = decode(gray, symbols=[ZBarSymbol.QRCODE])
    except:
        decoded = []

    if decoded:
        qr = decoded[0]

        try:
            data = qr.data.decode("utf-8")
        except:
            data = ""

        # expecting: "text1|||text2"
        if "|||" in data:
            t1, t2 = data.split("|||", 1)
        else:
            t1, t2 = data, ""

        st.session_state.decoded_text1 = t1
        st.session_state.decoded_text2 = t2

        # Draw polygon (SAFE)
        try:
            pts = qr.polygon
            if pts and len(pts) >= 4:
                pts = np.array([(p.x, p.y) for p in pts], dtype=np.int32)
                cv2.polylines(img, [pts], True, (0, 255, 0), 2)
        except:
            pass

    # Always return a valid frame
    try:
        return av.VideoFrame.from_ndarray(img, format="bgr24")
    except:
        return frame


from streamlit_webrtc import webrtc_streamer, WebRtcMode

webrtc_streamer(
    key="test",
    mode=WebRtcMode.RECVONLY,
    rtc_configuration={
        "iceServers": [
            {"urls": ["stun:stun.l.google.com:19302"]},
            {
                "urls": ["turn:openrelay.metered.ca:80",
                         "turn:openrelay.metered.ca:443",
                         "turn:openrelay.metered.ca:443?transport=tcp"],
                "username": "openrelayproject",
                "credential": "openrelayproject",
            },
        ]
    },
    media_stream_constraints={"video": True, "audio": False},
)


# Display results
st.text_input("Field 1", st.session_state.decoded_text1)
st.text_input("Field 2", st.session_state.decoded_text2)

