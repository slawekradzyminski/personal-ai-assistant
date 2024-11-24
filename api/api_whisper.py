import openai
import backoff
import os
from api.api_client import OpenAIClient

@backoff.on_exception(backoff.expo, (openai.RateLimitError, openai.OpenAIError), max_tries=10)
def api_get_transcript(audio_path):
    if not os.path.exists(audio_path):
        raise ValueError("Audio file not found")
        
    valid_types = ['.mp3', '.mp4', '.mpeg', '.mpga', '.m4a', '.wav', '.webm']
    if not any(audio_path.lower().endswith(t) for t in valid_types):
        raise ValueError(f"Audio file must be one of: {', '.join(valid_types)}")
    
    client = OpenAIClient.get_client()
    
    try:
        with open(audio_path, 'rb') as f:
            response = client.audio.transcriptions.create(
                file=f,
                model='whisper-1',
                response_format='text',
                temperature=0.2
            )
            
        if not response:
            raise ValueError("Empty response from Whisper API")
            
        return response
            
    except Exception as e:
        raise RuntimeError(f"Transcription failed: {str(e)}")