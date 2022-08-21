# importing libraries
import speech_recognition as sr

import os

from pydub import AudioSegment
from pydub.silence import split_on_silence

# a function that splits the audio file into chunks
# and applies speech recognition
def silence_based_conversion(path = "alice-medium.wav"):

	# open the audio file stored in
	# the local system as a wav file.
	song = AudioSegment.from_wav(path)

	
	fh = open("recognized.txt", "w+")
		
	
	chunks = split_on_silence(song,
		
		min_silence_len = 500,

		# consider it silent if quieter than -16 dBFS
		# adjust this per requirement
		silence_thresh = -16
	)

	# directory to store the audio chunks.
	try:
		os.mkdir('audio_chunks')
	except(FileExistsError):
		pass

	# move into the directory to store the audio files.
	os.chdir('audio_chunks')

	i = 0
	# process each chunk
	for chunk in chunks:
			
		# Create 0.5 seconds silence chunk
		chunk_silent = AudioSegment.silent(duration = 10)

		
		audio_chunk = chunk_silent + chunk + chunk_silent

		
		print("saving chunk{0}.wav".format(i))
		
		audio_chunk.export("./chunk{0}.wav".format(i), bitrate ='192k', format ="wav")

		
		filename = 'chunk'+str(i)+'.wav'

		print("Processing chunk "+str(i))

		
		# in the AUDIO_FILE variable for later use.
		file = filename

		# create a speech recognition object
		r = sr.Recognizer()

		# recognize the chunk
		with sr.AudioFile(file) as source:
			
			r.adjust_for_ambient_noise(source)
			audio_listened = r.listen(source)

		try:
			
			rec = r.recognize_google(audio_listened)
			
			fh.write(rec+". ")

		
		except sr.UnknownValueError:
			print("Could not understand audio")

		except sr.RequestError as e:
			print("Could not request results. check your internet connection")

		i += 1

	os.chdir('..')


if __name__ == '__main__':
		
	print('Enter the audio file path')

	path = input()

	silence_based_conversion(path)
