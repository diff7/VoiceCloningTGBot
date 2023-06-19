git clone https://github.com/Edresson/Coqui-TTS -b multilingual-torchaudio-SE TTS
pip install -q -e TTS/
pip install -q torchaudio==0.9.0

gdown --id 1-PfXD66l1ZpsZmJiC-vhL055CDSugLyP
gdown --id 1_Vb2_XHqcC0OcvRF82F883MTxfTRmerg
gdown --id 1SZ9GE0CBM-xGstiXH2-O2QWdmSXsBKdC -O speakers.json
gdown --id 1sgEjHt0lbPSEw9-FSbC_mBoOPwNi87YR -O best_model.pth.tar

CONFIG_SE_PATH="config_se.json"
CHECKPOINT_SE_PATH="SE_checkpoint.pth.tar"

gdown --id 19cDrhZZ0PfKf2Zhr_ebB-QASRw844Tn1 -O $CONFIG_SE_PATH
gdown --id 17JsW6h6TIh7-LkU2EvB_gnNrPcdBxt7X -O $CHECKPOINT_SE_PATH