# Transcription Tool

This repository is a tool for transcribing audio files.
It uses python with pydub for preprocessing and whisper for transcription.

## Python Execution Rule
Since `uv` is used, please run Python commands through the `uv` command.

```bash
uv run some_script.py
```

## Coding Guidelines
### Libraries to Use
* pathlib:
    * It is included in the standard library for handling paths. Do not use `os.path` under any circumstances.
* argparse:
    * It is also part of the standard library for parsing command-line arguments. Do not access `sys.argv` directly.

### Type Hints
Use type hints as much as possible.

1. Use the style introduced in Python `3.12` or later for generic parameters.
2. Use built-in container types like list, dict, etc., without importing them.
3. If type hints make the code harder to understand, it’s acceptable to use Any.

Example for Rule 1:
```python
from collections.abc import Sequence

def first[T](l: Sequence[T]) -> T:  # Function is generic over the TypeVar "T"
    return l[0]
```

Example for Rule 2:
```python
def some_list_func(some_list: list[int]):
    pass
```

## Commit Rules

Commit messages should first adhere to gitmoji.
Then, describe the detailed changes for each file.
Please write in English.

Example gitmoji
```
:sparkles: Add new feature
:bug: Fix bug
:recycle: Refactor code
:speech_balloon: Add logging
:rotating_light: fix lint
:zap: Improve performance
:fire: Remove unnecessary code
:memo: Update documentation
```
