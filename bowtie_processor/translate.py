import requests
from django.conf import settings

class GoogleTranslateProcessor(object):

	def __init__(self):
		self.api_key = settings.TRANSLATE_API_KEY

	def translate(self, word):
		"""
		Detect language and translate
		"""

		# Detect Language
		try:
			query = "https://www.googleapis.com/language/translate/v2/detect?key={0}&q={1}".format(self.api_key, word)
			r = requests.get(query)
			result = r.json()
			language = result['data']['detections'][0][0]['language']
			
			# Translate Language
			
			query = "https://www.googleapis.com/language/translate/v2?key={0}&q={1}&source={2}&target=en".format(
				self.api_key, word, language)

			r = requests.get(query)
			result = r.json()
			translated_word = result['data']['translations'][0]['translatedText']

			return translated_word
		except:
			return ''

