from pydub import AudioSegment
import speech_recognition as sr

from src.services.voice2text.decorators import print_decorator, timing_decorator


class GoogleAPIVoice2TextService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.language = "ru-RU"

    @print_decorator
    @timing_decorator
    def voice2text(self, file_path) -> str:
        """
        speech_recognition (Google API)

        Accuracy: Medium
        Speed: Fast
        Internet Required: Yes
        """

        wav_file = self.__convert_to_wav(file_path)

        with sr.AudioFile(wav_file) as source:
            audio_data = self.recognizer.record(source)

        try:
            text = self.recognizer.recognize_google(audio_data, language=self.language)  # Uses Google's free API
            return text
        except sr.UnknownValueError:
            return "Could not understand the audio"
        except sr.RequestError:
            return "API request failed"

    def __convert_to_wav(self, file_path: str):
        audio = AudioSegment.from_file(file_path)
        wav_file = file_path.rsplit(".", 1)[0] + ".wav"
        audio.export(wav_file, format="wav")
        return wav_file
