import json
from functools import lru_cache
from pathlib import Path

SUPPORTED_OPENAI_TTS_MODELS = (
    "tts-1",
    "tts-1-hd",
    "gpt-4o-mini-tts",
)

SUPPORTED_OPENAI_VOICES = (
    "alloy",
    "echo",
    "fable",
    "onyx",
    "nova",
    "shimmer",
)


@lru_cache(maxsize=1)
def load_custom_openai_voices() -> tuple[str, ...]:
    config_path = Path(__file__).with_name("custom_voices.json")
    if not config_path.exists():
        return ()

    with config_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    voices = data.get("voices", [])
    return tuple(sorted({str(voice).strip() for voice in voices if str(voice).strip()}))


def list_openai_voices(reference_ids: list[str] | None = None) -> list[str]:
    voices = set(SUPPORTED_OPENAI_VOICES)
    voices.update(load_custom_openai_voices())
    if reference_ids:
        voices.update(reference_ids)
    return sorted(voices)