import queue
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import threading


class VoiceController:
    def __init__(self, model_path="models/vosk-model-small-en-us-0.15"):
        self.q = queue.Queue()
        self.model = Model(model_path)
        self.rec = KaldiRecognizer(self.model, 16000)

        self.last_command = None
        self.running = True

        # 🔥 start thread
        self.thread = threading.Thread(target=self._listen_loop)
        self.thread.daemon = True
        self.thread.start()

    def _callback(self, indata, frames, time, status):
        self.q.put(bytes(indata))

    def _listen_loop(self):
        with sd.RawInputStream(
            samplerate=16000,
            blocksize=4000,
            dtype="int16",
            channels=1,
            callback=self._callback,
        ):
            print("🎤 Voice thread running...")

            while self.running:
                try:
                    data = self.q.get(timeout=0.1)
                except queue.Empty:
                    continue

                if self.rec.AcceptWaveform(data):
                    result = json.loads(self.rec.Result())
                    text = result.get("text", "")

                    if text and self.last_command is None:
                        print("You said:", text)
                        self.last_command = text