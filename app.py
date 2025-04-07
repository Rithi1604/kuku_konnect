

import streamlit as st
from utils import generate_story, text_to_speech, generate_image, continue_story, mask_story_ending
import os

st.set_page_config(page_title="KukuKonnect", layout="centered")
st.title("🎧 KukuKonnect – AI Audio Stories")

mode = st.selectbox("Choose a mode", ["🎙️ Audio Story", "📚 Cliffhanger", "🎯 Guess-the-ending"])

if mode == "🎙️ Audio Story":
    prompt = st.text_input("What do you want to hear?", placeholder="e.g. A funny bedtime story")
    if st.button("Generate 🎧"):
        if not prompt.strip():
            st.warning("Please enter something.")
        else:
            with st.spinner("Generating your story..."):
                story = generate_story(prompt)
                audio_path = text_to_speech(story)
                img_url = generate_image(prompt)
            st.image(img_url, caption="🎨 AI-generated cover")
            st.success("Here’s your story!")
            st.audio(audio_path)
            st.markdown("### 📖 Transcript")
            st.write(story)

elif mode == "📚 Cliffhanger":
    prompt = st.text_input("Start your mystery", placeholder="e.g. A ghost walks into a library...")
    if st.button("Generate Start"):
        cliffhanger = generate_story(prompt + " End with a cliffhanger.")
        st.write(cliffhanger)
        if st.button("🔄 Continue the Story"):
            continuation = continue_story(cliffhanger)
            st.markdown("**Continued...**")
            st.write(continuation)

elif mode == "🎯 Guess-the-ending":
    prompt = st.text_input("Choose your story theme", placeholder="e.g. A treasure map is found...")
    if st.button("Play Game"):
        full_story = generate_story(prompt)
        visible_part, answer = mask_story_ending(full_story)
        st.write(visible_part)
        user_guess = st.text_input("🤔 What do you think happens next?")
        if user_guess:
            st.markdown("**Actual Ending:**")
            st.write(answer)


