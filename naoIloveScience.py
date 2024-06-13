import pygame
import sounddevice as sd
import numpy as np
import tempfile
from scipy.io.wavfile import write
from datetime import datetime
import time
import paho.mqtt.client as mqtt_client
import random


broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
client_id = f'python-mqtt-{random.randint(0, 1000)}'

# Function to calculate root mean square of audio frame
def rms(frame):
    return np.sqrt(np.mean(np.square(frame), axis=0))

# Function to play audio
def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

# Function to record audio until silence
def record_until_silence(threshold=0.01, fs=44100, chunk_size=1024, max_silence=5):
    print("Begin recording... Speak now.")
    recorded_frames = []
    silent_frames = 0
    silence_limit = int(max_silence * fs / chunk_size)

    def callback(indata, frames, time, status):
        nonlocal silent_frames
        volume_norm = rms(indata)
        if volume_norm < threshold:
            silent_frames += 1
            if silent_frames > silence_limit:
                raise sd.CallbackStop
        else:
            silent_frames = 0
        recorded_frames.append(indata.copy())

    with sd.InputStream(callback=callback, device=1, dtype='float32', channels=1, samplerate=fs, blocksize=chunk_size):
        print("Recording started. Waiting for sound...")
        sd.sleep(5000)

    print("\nEnd of recording.")
    recording = np.concatenate(recorded_frames, axis=0)

    # Create temporary file and save recording
    temp_file = tempfile.mktemp(prefix='recorded_audio_', suffix='.wav')
    write(temp_file, fs, recording)
    print(f"Audio recorded and saved in: {temp_file}")
    return temp_file

# Function to announce player ready
def player_ready():
    print("Player 1 ready!")

# Function to announce player lost
def player_lost():
    print("Oh no, Player 1 lost!")

# Function for NAO's introduction and game explanation
def nao_introduction():
    print("Hello! My name is NAO.")
    print("Welcome to the Sphero Xscape game.")
    print("In this interactive multiplayer game, you control a robot ball through a maze.")
    print("Your objective is to navigate your robot ball to the finish line while avoiding obstacles.")
    print("Watch out for the Xarm! It may try to remove balls from the maze, so be quick and strategic!")
    print("Are you ready to embark on this exciting adventure? Let's get started!")

# Function to handle MTTQ - Xarm puts a ball in the game
def handle_xarm_puts_ball():
    # Trigger NAO's response for when Xarm puts a ball in the game
    player_ready()

# Function to handle MTTQ - Xarm takes a ball from the maze
def handle_xarm_takes_ball():
    # Trigger NAO's response for when Xarm takes a ball from the maze
    player_lost()

# Main function
def main():
    # Simulate receiving MTTQ events from Xarm
    mttq_received = "xarm_puts_ball"  # Simulate receiving MTTQ for Xarm putting a ball
    if mttq_received == "xarm_puts_ball":
        handle_xarm_puts_ball()
    elif mttq_received == "xarm_takes_ball":
        handle_xarm_takes_ball()

    # Record audio input from the microphone
    audio_file_path = record_until_silence()

    # If audio was recorded, play it back
    if audio_file_path:
        play_audio(audio_file_path)

if __name__ == "__main__":
    main()
