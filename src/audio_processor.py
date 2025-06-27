import argparse
from pathlib import Path

from pydub import AudioSegment
from pydub.silence import detect_nonsilent

from utils import setup_logger


def remove_silence(audio: AudioSegment, silence_thresh: int = -50, min_silence_len: int = 1000) -> AudioSegment:
    """Remove silence from audio."""
    nonsilent_ranges = detect_nonsilent(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)

    if not nonsilent_ranges:
        return audio

    processed_audio = AudioSegment.empty()
    for start, end in nonsilent_ranges:
        processed_audio += audio[start:end]

    return processed_audio


def split_audio(audio: AudioSegment, chunk_length_ms: int) -> list[AudioSegment]:
    """Split audio into chunks of specified length."""
    chunks = []
    for i in range(0, len(audio), chunk_length_ms):
        chunk = audio[i : i + chunk_length_ms]
        chunks.append(chunk)
    return chunks


def process_audio_file(
    input_file: Path, output_dir: Path, chunk_duration: int = 300, silence_thresh: int = -50, min_silence_len: int = 1000
) -> list[Path]:
    """Process audio file: remove silence and split into chunks."""
    logger = setup_logger(__name__)

    # Load audio file
    audio = AudioSegment.from_file(input_file)
    logger.info(f"Loaded audio file: {str(input_file)}")

    # Remove silence
    audio_no_silence = remove_silence(audio, silence_thresh=silence_thresh, min_silence_len=min_silence_len)
    logger.info("Removed silence from audio")

    # Split into chunks
    chunk_length_ms = chunk_duration * 1000  # Convert seconds to milliseconds
    chunks = split_audio(audio_no_silence, chunk_length_ms)
    logger.info(f"Split audio into {len(chunks)} chunks of {chunk_duration} seconds each")

    # Save chunks
    base_name = input_file.stem
    output_path = output_dir
    output_path.mkdir(parents=True, exist_ok=True)

    output_files = []
    for i, chunk in enumerate(chunks):
        output_file = output_path / f"{base_name}_chunk_{i + 1:03d}.wav"
        chunk.export(str(output_file), format="wav")
        output_files.append(output_file)
        logger.info(f"Saved: {str(output_file)}")

    return output_files


def main():
    logger = setup_logger(__name__)

    parser = argparse.ArgumentParser(description="Process audio files: remove silence and split into chunks")
    parser.add_argument("-i", "--input_file", type=Path, help="Path to input audio file")
    parser.add_argument("-o", "--output", type=Path, help="Output directory (default: output)")
    parser.add_argument("-d", "--duration", type=int, default=300, help="Chunk duration in seconds (default: 300)")
    parser.add_argument("--silence-thresh", type=int, default=-50, help="Silence threshold in dB (default: -50)")
    parser.add_argument("--min-silence-len", type=int, default=1000, help="Minimum silence length in ms (default: 1000)")

    args = parser.parse_args()

    if not args.input_file.exists():
        logger.error(f"Input file '{str(args.input_file)}' not found")
        return

    try:
        output_files = process_audio_file(args.input_file, args.output, args.duration, args.silence_thresh, args.min_silence_len)
        logger.info(f"Processing complete. Generated {len(output_files)} chunks.")
    except Exception:
        logger.exception("Error processing audio")
    return


if __name__ == "__main__":
    main()
