from openai import OpenAI

client = OpenAI()

TTS_MODEL = "gpt-4o-mini-tts"
TTS_VOICE = "marin"

def generate_speech(text: str) -> bytes:
    
    response = client.audio.speech.create(
        model=TTS_MODEL,
        voice=TTS_VOICE,
        input=text,
        instructions=(
            # basic TTS prompt. To be improved in future
            "Speak slowly and clearly. Use a warm, supportive tone. "
            "Pause briefly between sentences and emphasise important words."
        ),
        response_format="mp3",
    )
    
    return response.content