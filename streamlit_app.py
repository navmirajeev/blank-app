import streamlit as st
import cv2
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import tempfile
from deepface import DeepFace

# Set up Spotify API (Replace with your credentials from developer.spotify.com)
SPOTIPY_CLIENT_ID = "dec9363d252441d2a86f7258568fde17"
SPOTIPY_CLIENT_SECRET = "75dba9a494ec4e639da6d9ab19e25fad"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET
))

# Emotion-to-Music Mapping
emotion_to_genre = {
    "happy": "pop",
    "sad": "acoustic",
    "angry": "rock",
    "surprise": "electronic",
    "neutral": "chill"
}

# Streamlit UI
st.title("🎵 Mood-Based Music Recommender 🎶")
st.write("Take a photo of your face and get a song recommendation!")

# Use Streamlit's built-in webcam input
image_file = st.camera_input("📸 Take a photo")

if image_file is not None:
    # Save image temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        temp_file.write(image_file.read())
    
    # Detect Emotion
    try:
        emotion_result = DeepFace.analyze(temp_file.name, actions=['emotion'], enforce_detection=False)
        
        if emotion_result and isinstance(emotion_result, list):  
            detected_emotion = emotion_result[0].get('dominant_emotion', None)
            
            if detected_emotion:
                st.write(f"### Detected Emotion: **{detected_emotion.capitalize()}** 🎭")

                # Fetch Songs from Spotify
                genre = emotion_to_genre.get(detected_emotion, "chill")
                results = sp.search(q=f"genre:{genre}", type="track", limit=5)

                # Display Recommended Songs
                st.subheader("🎧 Recommended Songs:")
                for track in results['tracks']['items']:
                    st.write(f"🎶 {track['name']} - {track['artists'][0]['name']}")
                    
                    # Only show audio if preview URL exists
                    if track['preview_url']:
                        st.audio(track['preview_url'], format="audio/mp3")
                    else:
                        st.write("⚠️ No preview available")
            else:
                st.error("😔 Couldn't detect a clear emotion. Try again!")
        else:
            st.error("😔 No valid emotion detected. Try again!")
    
    except Exception as e:
        st.error(f"🚨 Error: {e}")
