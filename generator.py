
import os

os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["SUNO_USE_SMALL_MODELS"] = "1"

from bark import SAMPLE_RATE, generate_audio, preload_models
from bark.api import semantic_to_waveform
from scipy.io.wavfile import write as write_wav
import nltk 
import numpy as np




# download and load all models
# preload_models(text_use_small=True, coarse_use_small=True, fine_use_small=True)
preload_models()
# nltk.download("punkt")
# generate audio from text

username = "Helpful-Mountain1356"
intro = f"This story comes from user u/{username}. [laughs]"
text_prompt = """


Am I the asshole? So we had a great morning, I was laying in bed and I get up to grab something and I see the door wide open.( we live on 3rd floor apartment for some context) We have 2 cats and a dog and the dog was on porch barking and cats were nowhere to be found. I started yelling for her and she didn’t respond so I start freaking out and searching for the cats while yelling for her to come help. I find one cat under stairs in our driveway within a minute, but couldn’t find the other cat. I go up on porch and start screaming for her with no response still, she was upstairs changing and came down, the cat was only in driveway and I screamed at her learn to shut the door because this is the second time in a week she has left it open and the animals have gotten out.

She acted like it was no big deal and that I was crazy for being upset about it, but it’s not like we live in a residential neighborhood we live right off an extremely busy main road where cars constantly go 45-50 mph. The bottom of stairs are only 10 feet from the road.

For some background I have extreme OCD about doors being closed and locked, I will Leave the house and turn back around to make sure they are all locked if I didn’t triple check them. It’s not healthy and is annoying sometimes but I genuinely feel like I’m having a panic attack if I don’t know if they are 100% locked and closed.

Our first fight (4 years ago) was because she left the outdoor gate open and let my first dog outside accidentally and he almost got out.

I feel bad and I hate that I screamed at her but my biggest fear is our animals getting out because of the main road and other variables that could happen. I apologized after I calmed down but she’s still upset with me and won’t come home. Am I the asshole?

EDITED: broke up my stress typing wall of text into smaller readable sections.

""".replace("\n", " ").strip()
SPEAKER = "v2/en_speaker_9"
sentences = nltk.sent_tokenize(intro + text_prompt)



# silence = np.zeros(int(0.25 * SAMPLE_RATE))
# audio_array = generate_audio(text_prompt)

pieces = []
print(f"[info] sentence count: {len(sentences)}")
for sentence in sentences:
    audio_array = generate_audio(sentence, history_prompt=SPEAKER)
    pieces.extend(audio_array) 
    # pieces.extend(silence.copy())

# save audio to disk
print(np.array(pieces))
write_wav(f"audio/{username}.wav", SAMPLE_RATE, np.array(pieces))

# audio_array = generate_audio(text_prompt)
# print(audio_array)
# write_wav("audio/long_bark_generation.wav", SAMPLE_RATE, audio_array)
  
