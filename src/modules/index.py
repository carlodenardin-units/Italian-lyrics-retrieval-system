from modules.constants import *
from modules.dataset import Dataset
from modules.document import Document
from modules.preprocessor import Preprocessor
from modules.utils import *
from modules.trie import Trie
from typing import List, Dict, Tuple
from tqdm import tqdm

import ast
import locale

locale.setlocale(locale.LC_COLLATE, 'it_IT.UTF-8')

class Indexer:

	def __generate_positional_index(self, documents: List[Document]) -> None:
		"""
			Given the list of documents this function generates and stores the
			positional index.

			- documents: The list of documents
		"""
		dictionary: Dict[str, list[int]] = {}

		for document in documents:
			for position, term in enumerate(document.terms):
				if term not in dictionary:
					temp = {}
					temp[document.id] = [position]
					dictionary[term] = [1, temp]
				else:
					if document.id not in dictionary[term][1]:
						dictionary[term][0] += 1
						dictionary[term][1][document.id] = [position]
					else:
						dictionary[term][1][document.id].append(position)
		
		sorted_terms = [term for term in sorted(dictionary, key = locale.strxfrm)]

		save_positional_index(POSITIONAL_INDEX_PATH, sorted_terms, dictionary)

	def create_indexes(self, dataset: Dataset) -> None:
		"""
			This function create the indexes for the author and title performing 
			different functions.
			Fist of all it preprocess each document for the author and title using a 
			specific function and another for the lite lyrics index.
			Then for each index it creates a dictionary that contains the term as key
			and a list of documents id as value.
			Then it sorts the terms and saves the indexes and sorted terms.

			- dataset: the dataset to preprocess
		"""
		dict_author = {}
		dict_lyrics = {}
		dict_title = {}
		for document in tqdm(dataset.documents, total = len(dataset.documents), desc = 'Preprocessoring documents'):
			tokens_author = Preprocessor.perform_author_title_preprocess(document.author)
			tokens_lyrics = Preprocessor.perform_preprocess(document.lyrics)
			tokens_title = Preprocessor.perform_author_title_preprocess(document.title)
			
			for token in tokens_author:
				if token not in dict_author:
					dict_author[token] = [document.id]
				else:
					dict_author[token].append(document.id)
			
			for token in tokens_lyrics:
				if token not in dict_lyrics:
					dict_lyrics[token] = [document.id]
				else:
					dict_lyrics[token].append(document.id)

			for token in tokens_title:
				if token not in dict_title:
					dict_title[token] = [document.id]
				else:
					dict_title[token].append(document.id)

		sorted_author_terms = [term for term in sorted(dict_author, key = locale.strxfrm)]
		sorted_lyrics_terms = [term for term in sorted(dict_lyrics, key = locale.strxfrm)]
		sorted_title_terms = [term for term in sorted(dict_title, key = locale.strxfrm)]
		
		save_index(AUTHOR_INDEX_PATH, sorted_author_terms, dict_author)
		save_index(LITE_INDEX_PATH, sorted_lyrics_terms, dict_lyrics)
		save_index(TITLE_INDEX_PATH, sorted_title_terms, dict_title)
		
	def create_positional_index(self, dataset: Dataset) -> None:
		"""
			This function preprocess each document and save informationa about the document.
			- document_lengths: a dictionary that contains the length of each document
			- avglen: the average length of the documents
			This information are important to perform ranking function like okapi bm25 and
			if the collection is not available or is too big is better to save them
			Then it generates the positional index

			- dataset: the dataset to preprocess
		"""
		document_lengths = {}
		for document in tqdm(dataset.documents, total = len(dataset.documents), desc = 'Preprocessoring documents'):
			tokens = Preprocessor.perform_preprocess(document.lyrics)
			document.terms = tokens
			document_lengths[document.id] = len(document.terms)

		sum = 0
		for document in document_lengths:
			sum += document_lengths[document]

		save_dataset_info(str(document_lengths), str(sum / len(dataset.documents)))

		self.__generate_positional_index(dataset.documents)
	
	@staticmethod
	def load_positional_index(path: str) -> Trie:
		"""
			This function loads the positional index from the given path into
			a Trie data structure and returns it

			- path: The path of the positional index
			- return: The positional index in a Trie data structure
		"""
		trie = Trie()
		with open(path, 'r') as file:
			lines = file.readlines()
			for line in tqdm(lines, total = len(lines), desc = 'Loading positional index'):
				term = line.split(':')[0]
				others = line.split(':', 1)[1]
				others = ast.literal_eval(others.strip())
				dict = others[1]
				trie.insert(term, dict)
		return trie
	
	@staticmethod
	def load_index(path: str) -> Trie:
		"""
			This function loads the index from the given path into a Trie data
			structure and returns it.

			- path: The path of the index
			- return: The index in a Trie data structure
		"""
		trie = Trie()
		with open(path, 'r') as file:
			lines = file.readlines()
			for line in tqdm(lines, total = len(lines), desc = 'Loading lite index'):
				term = line.split(' ')[0]
				others = line.split(' ', 1)[1]
				dict = {}
				for other in others.strip().split(' '):
					dict[other] = []
				trie.insert(term, dict)
		return trie
	
	@staticmethod
	def load_indexes() -> Tuple[Trie, Trie, Trie]:
		"""
			This function loads the indexes from the given paths into Trie data
			structures and returns them.

			- return: The author, title and positional index
		"""
		author_trie = Indexer.load_index(AUTHOR_INDEX_PATH)
		title_trie = Indexer.load_index(TITLE_INDEX_PATH)
		positional_trie = Indexer.load_positional_index(POSITIONAL_INDEX_PATH)

		return author_trie, title_trie, positional_trie
	
	@staticmethod
	def load_lite_index(path: str) -> Dict[str, List[int]]:
		"""
			This function loads the lite index from the given path into a dict
			and returns it. (used to perform compression analysis)

			- path: The path of the lite index
			- return: The lite index
		"""
		index = {}
		with open(path, 'r') as file:
			lines = file.readlines()
			for line in tqdm(lines, total = len(lines), desc = 'Loading lite index'):
				term = line.split(' ')[0]
				docs_id = line.split(' ')[1:]
				index[term] = [int(doc_id) for doc_id in docs_id]
		return index