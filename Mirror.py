import streamlit as st
import cv2
import numpy as np
from deepface import DeepFace
import random
from PIL import Image
import urllib.parse
import io

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Sarcastic Mirror", page_icon="🙄", layout="centered")

# --- SARCASTIC DICTIONARIES ---
emotion_compliments = {
    "happy": ["Oh look, someone's in a good mood. Suspicious. 🤔", "Smiling like you know a secret. ✨"],
    "angry": ["Whoa, who stole your coffee? ☕", "Looking ready to fight a Wi-Fi router. 💥"],
    "sad": ["Cheer up, at least you aren't a variable getting garbage collected. 🗑️", "Aww, did someone drop their ice cream? 🥺"],
    "surprise": ["The face you make when you realize it's only Tuesday. 😲", "Caught in 4K. 📸"],
    "neutral": ["Giving absolutely nothing. Like an empty while loop. 🔄", "Ah, the default NPC expression. Iconic. 😐"],
    "default": ["Well, that's certainly a face. 🚀", "My AI circuits are struggling to comprehend this. ✨"]
}

# 🔴 NEW: BREAKING NEWS HEADLINES
news_headlines = {
    "happy": "LOCAL RESIDENT ARRESTED FOR BEING TOO CHEERFUL BEFORE 10 AM",
    "angry": "AREA CITIZEN READY TO THROW HANDS WITH A PRINTER",
    "sad": "TRAGIC: PERSON JUST REMEMBERED EMBARRASSING THING THEY DID IN 2014",
    "surprise": "CITIZEN SHOCKED TO LEARN THAT ACTIONS HAVE CONSEQUENCES",
    "neutral": "LOCAL HUMAN SUCCESSFULLY PRETENDS TO CARE ABOUT COWORKER'S STORY",
    "default": "UNIDENTIFIED ANOMALY DETECTED IN LOCAL AREA"
}

# --- WEBSITE UI ---
st.title("📺 Confidence Mirror Booster")
st.write("Step right up and become today's biggest (and dumbest) headline.")

user_name = st.text_input("What is your name?", placeholder="Type your name here...")

if user_name:
    st.markdown(f"### Welcome to the broadcast, {user_name.capitalize()}.")
    
    camera_photo = st.camera_input("Look into the camera like you just got caught:")

    if camera_photo is not None:
        with st.spinner("Contacting the newsroom..."):
            image = Image.open(camera_photo)
            img_array = np.array(image)
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

            # Emotion Analysis
            try:
                analysis = DeepFace.analyze(img_bgr, actions=['emotion'], enforce_detection=False)
                current_emotion = analysis[0]['dominant_emotion']
            except:
                current_emotion = "default"

            # Randomize stats
            confidence_score = random.randint(10, 100) 
            final_compliment = random.choice(emotion_compliments.get(current_emotion, emotion_compliments["default"]))
            headline = news_headlines.get(current_emotion, news_headlines["default"])

        # --- DISPLAY RESULTS ---
        st.success("Broadcast Live! 📡")
        
        # 🔴 NEW: THE NEWS BROADCAST UI
        st.markdown(f"""
        <div style="background-color: #8B0000; padding: 10px; border-radius: 5px 5px 0 0; text-align: center; color: white;">
            <h2 style="margin: 0; font-family: 'Arial Black', sans-serif; text-transform: uppercase;">🚨 BREAKING NEWS 🚨</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.image(image, use_container_width=True)
        
        st.markdown(f"""
        <div style="background-color: white; padding: 15px; border-left: 10px solid #8B0000; border-right: 10px solid #8B0000;">
            <h3 style="margin: 0; color: black; font-family: 'Arial Black', sans-serif; text-transform: uppercase;">"{headline}"</h3>
        </div>
        <div style="background-color: black; padding: 5px; border-radius: 0 0 5px 5px; color: yellow; font-family: monospace; font-size: 16px;">
            <marquee behavior="scroll" direction="left" scrollamount="8">
                <b>LIVE TICKER:</b> EXPERTS SAY {user_name.upper()}'S EGO RATING IS CURRENTLY AT {confidence_score}%... AI DETECTS HIGH LEVELS OF "{current_emotion.upper()}" VIBES... PLEASE STAND BY FOR MORE ROASTS...
            </marquee>
        </div>
        """, unsafe_allow_html=True)

        st.divider()
        st.info(f"**Off-Camera AI Roast:** \"{final_compliment}\"")

        # Save & Share
        buf = io.BytesIO()
        image.save(buf, format="JPEG")
        byte_im = buf.getvalue()

        col1, col2 = st.columns(2)
        with col1:
            st.download_button("💾 Save Evidence", byte_im, f"{user_name}_news.jpg", "image/jpeg", use_container_width=True)
        with col2:
            st.link_button("🐦 Expose Yourself on Twitter", f"https://twitter.com/intent/tweet?text=I made the news today. 🙄", use_container_width=True)