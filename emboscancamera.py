import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from pyzbar.pyzbar import decode
import av
import cv2

st.title("Page 2 — Scan QR Using Camera")

# To store the two decoded values
if "text1" not in st.session_state:
    st.session_state.text1 = ""
if "text2" not in st.session_state:
    st.session_state.text2 = ""

def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    
    # Decode QR
    decoded_list = decode(img)

    if decoded_list:
        data = decoded_list[0].data.decode("utf-8")

        if "|||" in data:
            t1, t2 = data.split("|||")

            st.session_state.text1 = t1
            st.session_state.text2 = t2

    # Display the video back
    return av.VideoFrame.from_ndarray(img, format="bgr24")


webrtc_streamer(
    key="qrscanner",
    mode=WebRtcMode.RECVONLY,
    video_frame_callback=video_frame_callback,
    media_stream_constraints={"video": True, "audio": False},
)


# Result fields (auto-filled)
st.text_input("Decoded Text 1", st.session_state.text1)
st.text_input("Decoded Text 2", st.session_state.text2)
