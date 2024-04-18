from pydub import AudioSegment
from spleeter.separator import Separator
from pydub.effects import speedup

def extract_vocals(filepath):
    separator = Separator('spleeter:2stems')
    separator.separate_to_file(filepath, 'output', codec='mp3')
    return 'output/vocals.mp3'

def extract_instruments(filepath):
   separator = Separator('spleeter:2stems')
   separator.separate_to_file(filepath, 'output', codec='mp3')
   return 'output/accompaniment.mp3'

def adjust_bpm(audio_path1, audio_path2, bpm_adjustment):
   from librosa.beat import tempo
   from librosa.core import load
   from pydub.playback import play
   
   y1, sr1 = load(audio_path1)
   y2, sr2 = load(audio_path2)
   bpm1 = tempo(y1, sr1)[0]
   bpm2 = tempo(y2, sr2)[0]
   
   if bpm_adjustment == 'file1' and bpm1 > bpm2:
       factor = bpm2 / bpm1
       song1 = AudioSegment.from_file(audio_path1).speedup(playback_speed=factor)
       song2 = AudioSegment.from_file(audio_path2)
   elif bpm_adjustment == 'file2' and bpm2 > bpm1:
       factor = bpm1 / bpm2
       song1 = AudioSegment.from_file(audio_path1)
       song2 = AudioSegment.from_file(audio_path2).speedup(playback_speed=factor)
   else:
       song1 = AudioSegment.from_file(audio_path1)
       song2 = AudioSegment.from_file(audio_path2)
   
   return song1, song2
   return song1, song2

def combine_audio(vocals_path, instruments_path):
   vocals, instruments = adjust_bpm(vocals_path, instruments_path)
   combined = vocals.overlay(instruments)
   combined.export("output/combined_song.mp3", format='mp3')
   return "output/combined_song.mp3"