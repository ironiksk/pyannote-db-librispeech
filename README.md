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




1. Fork this repository.
2. Edit `MyDatabase/__init__.py`
3. Edit `setup.py`, `setup.cfg` and `.gitattributes`
4. Edit lines 45 to 48 in `MyDatabase/_version.py`
5. Rename `MyDatabase` directory to the name of your database (e.g. to [`Etape`](http://github.com/pyannote/pyannote-db-etape) or [`REPERE`](http://github.com/pyannote/pyannote-db-repere))
6. Commit and tag your changes using [`semantic versioning`](http://semver.org)
7. Run `pip install -e .` and enjoy!


In case your database is public and you want to share, I'd be happy to integrate your plugin in `pyannote`: a [pull request](https://help.github.com/articles/about-pull-requests/) to this repository should help us get started...



echo "LibriSpeech: /usr/src/app/data/corpuses/speaker/LibriSpeech/wav/{uri}.wav" > ~/.pyannote/db.yml