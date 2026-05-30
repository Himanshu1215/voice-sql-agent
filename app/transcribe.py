import os
import whisper

_MODEL_NAME = os.environ.get("WHISPER_MODEL", "tiny")
_model = None

def _get_model():
    global _model
    if _model is None:
        print(f"Loading Whisper model: {_MODEL_NAME} ...")
        _model = whisper.load_model(_MODEL_NAME)
        print("Whisper model loaded.")
    return _model

def transcribe(audio_path: str) -> str:
    model = _get_model()
    result = model.transcribe(audio_path, language="en", fp16=False)
    return result["text"].strip()

if __name__ == "__main__":
    import sys
    print(transcribe(sys.argv[1]))
