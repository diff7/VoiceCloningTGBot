import sys
from omegaconf import OmegaConf as omg

cfg = omg.load('./config.yaml')
TTS_PATH = cfg.TTS_PATH
# add libraries into environment
sys.path.append(TTS_PATH) # set this if TTS is not installed globally

import random
import torch
import numpy as np
import librosa
from TTS.tts.utils.synthesis import synthesis

try:
  from TTS.utils.audio import AudioProcessor
except:
  from TTS.utils.audio import AudioProcessor


from TTS.tts.models import setup_model
from TTS.config import load_config
from TTS.tts.models.vits import *
import soundfile as sf

from TTS.tts.utils.speakers import SpeakerManager


class VoiceArtist:
    def __init__(self, CFG, CUDA=False, sample_rate=16000):
        print(CFG)
        self.CUDA = CUDA
        self.C = load_config(CFG.CONFIG_PATH)
        self.set_model(CFG)
        self.sample_rate = sample_rate
        
        self.SPM = SpeakerManager(encoder_model_path=CFG.CHECKPOINT_SE_PATH, 
                                    encoder_config_path=CFG.CONFIG_SE_PATH, 
                                    use_cuda=self.CUDA)
        
        
        self.reference_emb = np.random.rand(512)
        
        self.ap = AudioProcessor(**self.C.audio)
        self.language_id = CFG.language_id
        
    def set_model(self, CFG):
        self.C.model_args['d_vector_file'] = CFG.TTS_SPEAKERS
        self.C.model_args['use_speaker_encoder_as_loss'] = False
        self.model = setup_model(self.C)
        self.model.language_manager.set_language_ids_from_file(CFG.TTS_LANGUAGES)
        cp = torch.load(CFG.MODEL_PATH, map_location=torch.device('cpu'))
        # remove speaker encoder
        model_weights = cp['model'].copy()
        for key in list(model_weights.keys()):
            if "speaker_encoder" in key:
                del model_weights[key]

        self.model.load_state_dict(model_weights)
        self.model.eval()
        if  self.CUDA:
            self.model.cuda()
            
            
        self.model.length_scale = CFG.length_scale  # scaler for the duration predictor. The larger it is, the slower the speech.
        self.model.inference_noise_scale = CFG.inference_noise_scale # defines the noise variance applied to the random z vector at inference.
        self.model.inference_noise_scale_dp = CFG.inference_noise_scale_dp
    
    def get_wav(self, path):    
        data, samplerate = librosa.load(path)
        data  = librosa.resample(data, orig_sr=samplerate, target_sr=self.sample_rate)
        return data, samplerate    
    
    def resample(self, path):
        data, samplerate = self.get_wav(path)
        if samplerate != self.sample_rate:
            sf.write(path, data, self.sample_rate)
        
        
    def set_speaker_identity(self, referece_path):
        self.resample(referece_path)
        self.reference_emb = self.SPM.compute_d_vector_from_clip(referece_path)
        
        

    def generate(self, text):
        wav, alignment, _, _ = synthesis(
                    self.model,
                    text,
                    self.C,
                    "cuda" in str(next(self.model.parameters()).device),
                    self.ap,
                    speaker_id=None,
                    d_vector= self.reference_emb,
                    style_wav=None,
                    language_id=self.language_id,
                    enable_eos_bos_chars=False).values()
        
        return wav
    
    def set_random_speaker(self):
        self.reference_emb =  random.choice([-1,-0.5,0.5,1])*(np.random.randn(512)/10)
    
