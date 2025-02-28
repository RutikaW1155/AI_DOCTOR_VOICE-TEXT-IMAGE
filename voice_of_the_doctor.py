from flask import Flask, request, jsonify, send_file, render_template
import os
import platform
import subprocess
from dotenv import load_dotenv
from gtts import gTTS
from playsound import playsound
from pydub import AudioSegment
import elevenlabs
from elevenlabs.client import ElevenLabs

# Load environment variables
load_dotenv()

# Get ElevenLabs API Key
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

# Initialize Flask app
app = Flask(__name__)

# Function to convert MP3 to WAV
def convert_mp3_to_wav(mp3_filepath, wav_filepath):
    sound = AudioSegment.from_mp3(mp3_filepath)
    sound.export(wav_filepath, format="wav")

# ✅ Text-to-Speech using gTTS
def text_to_speech_with_gtts(input_text, output_filepath="static/gtts_output.mp3"):
    audio_obj = gTTS(text=input_text, lang="en", slow=False)
    audio_obj.save(output_filepath)
    return output_filepath

# ✅ Text-to-Speech using ElevenLabs
def text_to_speech_with_elevenlabs(input_text, output_filepath="static/elevenlabs_output.mp3"):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.generate(
        text=input_text,
        voice="Aria",
        output_format="mp3_22050_32",
        model="eleven_turbo_v2"
    )
    elevenlabs.save(audio, output_filepath)
    return output_filepath

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_audio():
    data = request.json
    input_text = data.get("text")
    tts_engine = data.get("engine")

    if not input_text:
        return jsonify({"error": "No text provided"}), 400
    
    output_filepath = "static/output.mp3"
    if tts_engine == "gtts":
        output_filepath = text_to_speech_with_gtts(input_text)
    elif tts_engine == "elevenlabs":
        output_filepath = text_to_speech_with_elevenlabs(input_text)
    else:
        return jsonify({"error": "Invalid TTS engine"}), 400
    
    return jsonify({"audio_url": output_filepath})

if __name__ == '__main__':
    app.run(debug=True)
