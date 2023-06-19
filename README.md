### Run a telegram bot for voice generation

```bash
python3 tg_bot.py
```

### Generate text with a given speaker styles

- 'out' a folder to save audio
- 'sf' a folder with reference files in wav
- 't' some text
- 'r' generate 5 random speakears for given text utterance (0 or 1)

```bash
python3 run_files.py -sf '../speech/speakers/' -r 1 -out './out_folder/' -t "Real stupidity beats artificial intelligence every time"
```

### To compute similarity scores use the following script:

(computed metrics can be found in scores.txt)

```bash
python3 metrics.py -sf '../speech/speakers/' -out './out_folder/'
```

### Installation

The solution is based on YourTTS repository.
https://github.com/Edresson/YourTTS

1. Run setup.sh to obtian a repository, weights and config files
2. Write paths to all config files, weights and repository in config.yaml
3. install requirements
