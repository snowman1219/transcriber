import argparse
import os
from pathlib import Path

from openai import OpenAI

from utils import setup_logger


def get_audio_files(path: Path) -> list[Path]:
    """Get all audio files from a directory or return single file."""
    if path.is_file():
        return [path]

    if path.is_dir():
        audio_extensions = {".mp3", ".wav", ".m4a", ".flac", ".ogg", ".aac"}
        audio_files = []
        for ext in audio_extensions:
            audio_files.extend(path.glob(f"*{ext}"))
            audio_files.extend(path.glob(f"*{ext.upper()}"))
        return sorted(audio_files)

    return []


def transcribe_audio(client: OpenAI, audio_file: Path, model: str = "whisper-1", language: str = "ja") -> str:
    """Transcribe audio file using OpenAI Whisper API."""
    logger = setup_logger(__name__)

    try:
        with audio_file.open("rb") as file:
            logger.info(f"Transcribing: {audio_file.name}")
            transcript = client.audio.transcriptions.create(model=model, file=file, response_format="json", language=language)
            return transcript.text
    except Exception:
        logger.exception(f"Failed to transcribe {audio_file.name}")
        return ""


def save_transcript(transcript: str, output_file: Path) -> None:
    """Save transcript to file."""
    logger = setup_logger(__name__)

    try:
        with output_file.open("w", encoding="utf-8") as f:
            f.write(transcript)
        logger.info(f"Saved transcript: {output_file}")
    except Exception:
        logger.exception(f"Failed to save transcript to {output_file}")


def main():
    logger = setup_logger(__name__)

    parser = argparse.ArgumentParser(description="Transcribe audio files using OpenAI Whisper API")
    parser.add_argument("-i", "--input", type=Path, help="Input audio file or directory containing audio files")
    parser.add_argument("-o", "--output", type=Path, help="Output directory for transcripts (default: transcripts)")
    parser.add_argument("--model", default="whisper-1", help="Whisper model to use (default: whisper-1)")
    parser.add_argument("--language", default="ja", help="Language of the audio (default: ja for Japanese)")

    args = parser.parse_args()

    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OpenAI API key is required. Set OPENAI_API_KEY environment variable")
        return

    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    # Check input path
    if not args.input.exists():
        logger.error(f"Input path '{args.input}' not found")
        return

    # Get audio files
    audio_files = get_audio_files(args.input)
    if not audio_files:
        logger.error(f"No audio files found in '{args.input}'")
        return

    logger.info(f"Found {len(audio_files)} audio file(s) to transcribe")

    # Create output directory
    args.output.mkdir(parents=True, exist_ok=True)

    # Transcribe each file
    success_count = 0
    for audio_file in audio_files:
        transcript = transcribe_audio(client, audio_file, args.model, args.language)
        if transcript:
            output_file = args.output / f"{audio_file.stem}.txt"
            save_transcript(transcript, output_file)
            success_count += 1

    logger.info(f"Successfully transcribed {success_count}/{len(audio_files)} files")
    return


if __name__ == "__main__":
    main()
