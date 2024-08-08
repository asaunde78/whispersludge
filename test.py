import os
import threading
import logging
os.environ["CUDA_VISIBLE_DEVICES"] = ""
# os.environ["SUNO_USE_SMALL_MODELS"] = "1"

from bark import SAMPLE_RATE, generate_audio, preload_models
from bark.api import semantic_to_waveform
from scipy.io.wavfile import write as write_wav
import nltk 
import numpy as np


SPEAKER = "v2/en_speaker_5"
# download and load all models
# preload_models(text_use_small=True, coarse_use_small=True, fine_use_small=True)
preload_models()

# test = "hello there how are you doing im doing really good hey i hope you're having a great day today"
# sentences = nltk.word_tokenize(test)
# # nltk.download("averaged_perceptron_tagger")
# print(sentences)
count = 0
gen_lock = threading.Lock()
def gen(text):
    global count 
    logging.info(f"Thread starting... '{text}'")
    with gen_lock:
        tokens = nltk.word_tokenize(text)
        if(len(tokens) > 15):
            print('Too long!')
            logging.info(f"Thread finishing early... '{text}'")
            return
        # sentences = nltk.sent_tokenize(text)
        
        # pieces = [] 
        # print(f"[info] sentence count: {len(sentences)}")
        # for sentence in sentences:
        #     audio_array = generate_audio(sentence, history_prompt=SPEAKER)
        #     pieces.extend(audio_array) 
        audio_array = generate_audio(text, silent=True)
        count += 1
        write_wav(f"audio/test{count}.wav", SAMPLE_RATE, audio_array)
        generating = False
    logging.info(f"Thread finishing... '{text}'")



format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,datefmt="%H:%M:%S")
while True: 
    text = input("What's your input?\n\t").replace("\n", " ").strip()
    if(not gen_lock.locked()):
        x = threading.Thread(target=gen, args=(text,), daemon=True)
        x.start()
    else:
        print("currently generating")

# print(nltk.pos_tag(sentences))
