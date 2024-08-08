#https://github.com/m-bain/whisperX
import whisperx
import json 
from datetime import timedelta

device = "cpu"
username = "redditstory"
audio_file = f"audio/{username}.wav"
model = whisperx.load_model("base", device, compute_type="int8",language="en")
audio = whisperx.load_audio(audio_file)
result = model.transcribe(audio_file, batch_size=8, language="en")

model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)
#could edit the audio segments after captioning to cut down on time between words (auto identify large gaps of no words)
output = result["segments"]

with open("subtitles.srt", "w") as f:
    f.write("")
with open("subtitles.srt", "a") as subt:
    count = 1
    for sentence in result["segments"]:
        for word in sentence["words"]:
            # print("WORD: ", word)
            start = str(timedelta(seconds=word["start"]))[:-3]
            end = str(timedelta(seconds=word["end"]))[:-3]
            txt = word["word"]
            stri = f"{count}\n0{start} --> 0{end}\n{txt}\n\n".replace(".",",")
            stri.replace(".",",")
            print(stri)
            subt.write(stri)
            count += 1



print(json.dumps(output, indent=2)) # after alignment

