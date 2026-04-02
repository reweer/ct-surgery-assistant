import queue
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import threading
import os


class VoiceController:
    def __init__(self, model_path="models/vosk-model-small-en-us-0.15"):
        self.q = queue.Queue()
        
        # Load configuration
        self.device_index = None
        if os.path.exists("config.json"):
            try:
                with open("config.json", "r") as f:
                    config = json.load(f)
                    self.device_index = config.get("device_index")
            except Exception as e:
                print(f"⚠️ Warning: Could not read config.json: {e}")

        try:
            self.model = Model(model_path)
            print(f"✅ Vosk model loaded from: {model_path}")
        except Exception as e:
            print(f"❌ ERROR: Could not load Vosk model: {e}")
            raise

        self.rec = KaldiRecognizer(self.model, 16000)

        self.commands = queue.Queue()
        self.running = True

        # Show device info
        try:
            device_info = sd.query_devices(self.device_index, 'input')
            print(f"🎤 Using Microphone: {device_info['name']} (Index: {self.device_index if self.device_index is not None else 'Default'})")
        except Exception as e:
            print(f"⚠️ Warning: Could not query device {self.device_index}: {e}")

        #  start thread
        self.thread = threading.Thread(target=self._listen_loop)
        self.thread.daemon = True
        self.thread.start()

    def _callback(self, indata, frames, time, status):
        if status:
            print(f"[AUDIO STATUS] {status}")
        self.q.put(bytes(indata))

    def _listen_loop(self):
        try:
            with sd.RawInputStream(
                samplerate=16000,
                blocksize=8000,
                dtype="int16",
                channels=1,
                device=self.device_index,
                callback=self._callback,
            ):
                print(f"🎤 Voice thread running... (Microphone active)")

                while self.running:
                    try:
                        data = self.q.get(timeout=0.1)
                    except queue.Empty:
                        continue

                    if self.rec.AcceptWaveform(data):
                        result = json.loads(self.rec.Result())
                        text = result.get("text", "")

                        if text:
                            print(">>> You said:", text)
                            self.commands.put(text)

        except Exception as e:
            print(f"❌ ERROR in Voice Loop: {e}")
            self.running = False