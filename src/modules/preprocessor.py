from lingua import Language, LanguageDetectorBuilder
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from unidecode import unidecode
from typing import List

import Stemmer

TOKENIZER = RegexpTokenizer(r'\w+')
STEMMER_IT = Stemmer.Stemmer('italian')
STEMMER_EN = Stemmer.Stemmer('english')
STOPWORDS_IT = stopwords.words('italian')
STOPWORDS_EN = stopwords.words('english')
LANGUAGES = [Language.ENGLISH, Language.ITALIAN]
DETECTOR = LanguageDetectorBuilder.from_languages(*LANGUAGES).build()

class Preprocessor:

	@staticmethod
	def perform_language_detection_stemming(tokens: List[str]) -> List[str]:
		results = []
		for token in tokens:
			confidence_values = DETECTOR.compute_language_confidence_values(token)
			for confidence in confidence_values:
				if confidence.language == Language.ITALIAN and confidence.value > 0.3:
					results.append(STEMMER_IT.stemWord(token))
					break
				elif confidence.language == Language.ENGLISH and confidence.value > 0.3:
					results.append(STEMMER_EN.stemWord(token))
					break
		return results

	@staticmethod
	def perform_preprocess(
		text: str,
	) -> List[str]:
		
		tokens = TOKENIZER.tokenize(text)
		filtered_tokens = filter(lambda token: token not in STOPWORDS_IT, tokens)
		filtered_tokens = filter(lambda token: token not in STOPWORDS_EN, filtered_tokens)
		lower_case_tokens = map(lambda token: token.casefold(), filtered_tokens)
		long_tokens = filter(lambda token: len(token) > 2, lower_case_tokens)
		no_digit_tokens = filter(lambda token: not any(c.isdigit() for c in token), long_tokens)
		unidecoded_tokens = map(lambda token: unidecode(token), no_digit_tokens)
		unpatterned_tokens = filter(lambda token: 'ah' not in token and 'uh' not in token and 'oioi' not in token and 'oh' not in token and not any(c*3 in token for c in token), unidecoded_tokens)
		return Preprocessor.perform_language_detection_stemming(list(unpatterned_tokens))
	
	@staticmethod
	def perform_author_title_preprocess(
		text: str,
	) -> List[str]:
		tokens = TOKENIZER.tokenize(text)
		filtered_tokens = filter(lambda token: token not in STOPWORDS_IT, tokens)
		lower_case_tokens = map(lambda token: token.casefold(), filtered_tokens)
		long_tokens = filter(lambda token: len(token) > 2, lower_case_tokens)
		no_digit_tokens = filter(lambda token: not any(c.isdigit() for c in token), long_tokens)
		unidecoded_tokens = map(lambda token: unidecode(token), no_digit_tokens)
		return unidecoded_tokens
