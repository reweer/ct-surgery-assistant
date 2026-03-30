import queue
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer


class VoiceController:
    def __init__(self, model_path="models/vosk-model-small-en-us-0.15"):
        self.q = queue.Queue()
        self.model = Model(model_path)
        self.rec = KaldiRecognizer(self.model, 16000)

    def _callback(self, indata, frames, time, status):
        self.q.put(bytes(indata))

    def listen(self):
        with sd.RawInputStream(
            samplerate=16000,
            blocksize=8000,
            dtype="int16",
            channels=1,
            callback=self._callback,
        ):
            print("Listening...")

            while True:
                data = self.q.get()

                if self.rec.AcceptWaveform(data):
                    result = json.loads(self.rec.Result())
                    text = result.get("text", "")

                    if text:
                        print("You said:", text)
                        return text