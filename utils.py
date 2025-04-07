# import requests
# import os
# from gtts import gTTS
# import uuid
# from dotenv import load_dotenv

# load_dotenv()
# HF_TOKEN = "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"

# def generate_story(prompt):
#     API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
#     headers = {"Authorization": f"Bearer {HF_TOKEN}"}
#     payload = {
#         "inputs": f"Write an audio story based on: {prompt}",
#         "parameters": {"max_new_tokens": 200}
#     }
#     response = requests.post(API_URL, headers=headers, json=payload)
#     result = response.json()

#     if isinstance(result, list) and "generated_text" in result[0]:
#         return result[0]["generated_text"]
#     elif isinstance(result, dict) and "error" in result:
#         return f"❌ Error: {result['error']}"
#     else:
#         return "⚠️ Unexpected response from model."


# def text_to_speech(text):
#     audio_id = str(uuid.uuid4())
#     os.makedirs("audio", exist_ok=True)
#     path = f"audio/{audio_id}.mp3"
#     tts = gTTS(text)
#     tts.save(path)
#     return path

from gtts import gTTS
import requests
import uuid
import os

HF_TOKEN = "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"

def generate_story(prompt):
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 200}
    }
    res = requests.post(API_URL, headers=headers, json=payload)
    result = res.json()
    return result[0]["generated_text"] if isinstance(result, list) else "⚠️ Model error."

def continue_story(partial):
    return generate_story(f"Continue this story: {partial}")

def mask_story_ending(text):
    parts = text.strip().split('. ')
    if len(parts) < 3:
        return text, "Too short to mask."
    visible = '. '.join(parts[:-2]) + '.'
    answer = '. '.join(parts[-2:])
    return visible, answer

def text_to_speech(text):
    audio_id = str(uuid.uuid4())
    os.makedirs("audio", exist_ok=True)
    path = f"audio/{audio_id}.mp3"
    gTTS(text).save(path)
    return path

def generate_image(prompt):
    url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    res = requests.post(url, headers=headers, json={"inputs": prompt})
    if res.status_code == 200:
        with open(f"images/{uuid.uuid4()}.png", "wb") as f:
            f.write(res.content)
        return f.name
    else:
        return "https://via.placeholder.com/512?text=Image+Error"

