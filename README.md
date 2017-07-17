# pyannote.database plugin for LibriSpeech corpus

This repository provides a driver for LibriSpeech database.


1. Download LibriSpeech datasets from [`LibriSpeech`](http://www.openslr.org/12/).
2. Extract dev/test/train archives to the folder LibriSpeech
3. Rename folders to the template: {subset}-{protocol}. For example: `test-clean`, `train-clean`, `dev-clean`
4. Close this repository.
5. Set path to the:
- LibriSpeech corpus `db_dir` (it should consists SPEAKERS.txt file) 
- `annotation_dir` (`pyannote-db-librispeech/LibriSpeech`) consists annotation files for the current corpuses
- `protocols` e.g. ['dev-clean', 'dev-other', ...]
- `path_to_wav` path where training wav files will be stored
6. Convert audio files and create annotation files by run script `LibriSpeech/generate.py`
7. Write string `LibriSpeech: /path/to/corpus/LibriSpeech/wav/{uri}.wav` to file ` ~/.pyannote/db.yml `
