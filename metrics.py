
import os
import numpy as np
from resemblyzer import VoiceEncoder, preprocess_wav
import librosa
import argparse

from numpy import dot
from numpy.linalg import norm

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



args = parser.parse_args()

encoder = VoiceEncoder()


def cosine(a,b):
    return dot(a, b)/(norm(a)*norm(b))
    

def get_wav(path):
    data, samplerate = librosa.load(path)
    data  = librosa.resample(data, orig_sr=samplerate, target_sr=16000)
    return data

files_orig_folder = set(os.listdir(args.speakers_wav))
files_generated = set(os.listdir(args.out_folder)).intersection(files_orig_folder)

for f_name in files_orig_folder:
    orig = get_wav(os.path.join(args.speakers_wav,f_name))
    ref = get_wav(os.path.join(args.out_folder,f_name))
    
    orig = preprocess_wav(orig)    
    ref = preprocess_wav(ref)    
    
    orig_embed = encoder.embed_utterance(orig)
    ref_embed = encoder.embed_utterance(ref)
    
    print(f'Similarity score for a file {f_name} : {cosine(orig_embed, ref_embed)}')
    with open('scores.txt', 'a') as f:
        print(f'Similarity score for a file {f_name} : {cosine(orig_embed, ref_embed)}', file=f)

os.makedirs(args.out_folder, exist_ok=True)