import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode

st.title("Camera Test")

webrtc_streamer(
    key="cam",
    mode=WebRtcMode.RECVONLY,
    media_stream_constraints={"video": True, "audio": False},
)
