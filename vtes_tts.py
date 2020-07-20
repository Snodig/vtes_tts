import traceback
import time
import os
import sys
from pydub import AudioSegment
from gtts import gTTS
from vlc import MediaPlayer

source_dir = "F:\\Games2\\LackeyCCGWin\\LackeyCCG\\plugins\\vtes\\sounds"
languages = ["en-us", "no"]
languages = ["en-nz", "en-gb", "en-us", "no"]
playback = True
statements = sys.argv[1:]  # Supports passing one or more strings as args instead of searching through the source dir

# The following needs customization:
overrides = {
    "absteins": "abstains",
    "combatend": "combat ends",
    "endofturn": "end of turn",
    "youdone": "you done?",
    "youready": "you ready?"
}

if len(statements) == 0:
    for r, d, f in os.walk(source_dir):
        for file in f:
            if ".wav" in file:
                statements.append(file.replace(".wav", ""))

for language in languages:
    for to_say in statements:
        try:
            file_basename = to_say.replace(" ", "-")
            mp3_dir = os.getcwd() + "\\" + language + "\\mp3\\"
            wav_dir = os.getcwd() + "\\" + language + "\\wav\\"
            mp3 = mp3_dir + file_basename + ".mp3"
            wav = wav_dir + file_basename + ".wav"

            if not os.path.exists(mp3_dir):
                os.makedirs(mp3_dir, exist_ok=True)
            if not os.path.exists(wav_dir):
                os.makedirs(wav_dir, exist_ok=True)

            if to_say in overrides.keys():
                to_say = overrides[to_say]
            tts = gTTS(to_say.replace("-", " "), lang=language)
            tts.save(mp3)

            sound = AudioSegment.from_mp3(mp3)
            sound.export(wav, format="wav")

            if playback:
                player = MediaPlayer(wav)
                player.play()
                time.sleep(0.1)
                duration = player.get_length() / 1000
                print(file_basename + " (" + str(duration) + "s)")
                time.sleep(duration)
            else:
                print(mp3)

        except KeyboardInterrupt:
            print("\n-- Ctrl^C ---")
            break

        except Exception:
            traceback.print_exc()
            break
