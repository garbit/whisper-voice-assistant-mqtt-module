import paho.mqtt.client as mqtt

import os
import time
import pickle

import time
from collections import deque
import os
from dotenv import load_dotenv

import numpy as np
import pvporcupine
import pvcobra
import whisper
from pvrecorder import PvRecorder
import torch

from schemas.event import SpeechEvent

EVENT_TOPIC = "new_event"

load_dotenv()


class Transcriber:
    def __init__(self, model, client) -> None:
        print("loading model")
        # TODO: put model on GPU
        self.client = client
        self.model = whisper.load_model(model)
        print("loading model finished")
        self.prompts = os.environ.get("WHISPER_INITIAL_PROMPT", "")
        print(f"Using prompts: {self.prompts}")

    def transcribe(self, frames):
        transcribe_start = time.time()
        samples = np.array(frames, np.int16).flatten().astype(np.float32) / 32768.0

        result = self.model.transcribe(
            audio=samples,
            language="en",
            fp16=False,
            initial_prompt=self.prompts,
        )

        # print the recognized text
        transcribe_end = time.time()
        # print(
        #     f"{transcribe_end} - {transcribe_end - transcribe_start}sec: {result.get('text')}",
        #     flush=True,
        # )
        data = SpeechEvent(
            event="speech_query",
            time=time.time(),
            query=result.get("text", "speech not detected"),
        )
        print(f"Publishing:{data}")
        self.client.publish(EVENT_TOPIC, pickle.dumps(data))
        return result.get("text", "speech not detected")


def whisper_voice_assistant_client(hostname, client_id):
    def on_connect(client, userdata, flags, rc):
        print("on_connect: publisher")

    client = mqtt.Client(client_id)

    client.on_connect = on_connect
    client.connect(hostname)
    client.loop_start()
    try:
        transcriber = Transcriber(os.environ.get("WHISPER_MODEL"), client=client)
        sample_rate = 16000
        frame_size = 512
        vad_mean_probability_sensitivity = float(os.environ.get("VAD_SENSITIVITY"))

        porcupine = pvporcupine.create(
            access_key=os.environ.get("ACCESS_KEY"),
            keyword_paths=[os.environ.get("WAKE_WORD_MODEL_PATH")],
        )

        cobra = pvcobra.create(
            access_key=os.environ.get("ACCESS_KEY"),
        )

        recoder = PvRecorder(device_index=-1, frame_length=512)

        try:
            recoder.start()

            max_window_in_secs = 3
            window_size = sample_rate * max_window_in_secs
            samples = deque(maxlen=(window_size * 6))
            vad_samples = deque(maxlen=25)
            is_recording = False

            while True:
                data = recoder.read()
                vad_prob = cobra.process(data)
                vad_samples.append(vad_prob)

                if porcupine.process(data) >= 0:
                    print(f"Detected wakeword")
                    is_recording = True
                    samples.clear()

                if is_recording:
                    if (
                        len(samples) < window_size
                        or np.mean(vad_samples) >= vad_mean_probability_sensitivity
                    ):
                        samples.extend(data)
                        print(f"listening - samples: {len(samples)}")
                    else:
                        print("is_recording: False")
                        print(transcriber.transcribe(samples))
                        is_recording = False
        except KeyboardInterrupt:
            recoder.stop()
        finally:
            porcupine.delete()
            recoder.delete()
            cobra.delete()
            client.loop_stop()

    except KeyboardInterrupt:
        print("Keyboard interrupt")
        client.loop_stop()


if __name__ == "__main__":
    broker = os.environ.get("MQTT_ENDPOINT", "0.0.0.0")
    whisper_voice_assistant_client(broker, "whisper-voice-assistant")
