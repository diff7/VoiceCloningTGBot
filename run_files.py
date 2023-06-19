import os
import argparse
from artist import VoiceArtist
from omegaconf import OmegaConf as omg

parser = argparse.ArgumentParser()

parser.add_argument(
    "-sf",
    "--speakers_wav",
    default='./speakers',
    type=str,
    help="a folder with reference speakers",
)


parser.add_argument(
    "-out",
    "--out_folder",
    default="./out",
    type=str,
    help="a folder to save values",
)

parser.add_argument(
    "-r",
    "--random",
    type=int,
    default=0,
    help="generate 5 random speakers",
)

parser.add_argument(
    "-t",
    "--text",
    type=str,
    default="Real stupidity beats artificial intelligence every time",
    help="generate 5 random speakers",
)


args = parser.parse_args()


if __name__ == "__main__":
    cfg = omg.load('./config.yaml')
    artist = VoiceArtist(cfg, CUDA=False, sample_rate=16000)
    
    files = os.listdir(args.speakers_wav)

    os.makedirs(args.out_folder, exist_ok=True)

    for f in files:
        full_p = os.path.join(args.speakers_wav,f)
        artist.set_speaker_identity(full_p)
        signal = artist.generate(args.text)
        artist.ap.save_wav(signal, os.path.join(args.out_folder,f))
        
    if args.random:
        for i in range(5):
            artist.set_random_speaker()
            signal = artist.generate(args.text)
            artist.ap.save_wav(signal, os.path.join(args.out_folder,f"random_{i}.wav"))