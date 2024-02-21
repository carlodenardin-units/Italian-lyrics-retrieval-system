from functools import reduce
from modules.preprocessor import Preprocessor
from modules.trie import Trie
from typing import Dict, List
import math

class Query:
	"""
		This class is used to perform queries on the indexes. It contains
		three tries: one for the author, one for the title and one for the
		positional index. It also contains the parameters b and k1 used to
		compute the Okapi BM25 score.
	"""

	def __init__(self, author_trie: Trie, title_trie: Trie, positional_trie: Trie):
		self.author_trie = author_trie
		self.title_trie = title_trie
		self.positional_trie = positional_trie
		self.b = 0.75
		self.k1 = 1.2
	
	def compute_idf(self, N: int, df: int):
		"""
			This function computes the idf of a term.

			- N: The number of documents in the collection
			- df: The document frequency of the term
			- return: The idf of the term
		"""
		return math.log(N / df)
	
	def compute_tf_idf(self, tf: int, idf: int):
		"""
			This function computes the tf-idf of a term.

			- tf: The term frequency of the term
			- idf: The idf of the term
			- return: The tf-idf of the term
		"""
		return tf * idf

	def perform_tfidf_query(self, query: str, N: int) -> List[int]:
		"""
			This function performs a tf-idf query on the positional index.
			More specifically it computes the tf-idf score of each document that
			contains at least one token of the query.

			- query: The query to perform
			- N: The number of documents in the collection
			- return: The list of documents that contains at least one token of the query
			ordered by tf-idf score
		"""

		tokens = Preprocessor.perform_preprocess(query)

		dict = {}
		for token in tokens:
			posting_lists = self.positional_trie.search(token)
			idf = self.compute_idf(N, len(posting_lists))

			for doc in posting_lists:
				if doc not in dict:
					dict[doc] = self.compute_tf_idf(len(posting_lists[doc]), idf)
				else:
					dict[doc] += self.compute_tf_idf(len(posting_lists[doc]), idf)
		
		dict = {k: v for k, v in sorted(dict.items(), key = lambda item: item[1], reverse = True)}

		return list(dict.keys())[:5]

	def perform_okapi_bm25(self, query: str, document_info: Dict, avglen: float) -> Dict:
		"""
			This function performs an Okapi BM25 query on the positional index (not considering
			the positional information).

			- query: The query to perform
			- document_info: A dictionary containing the length of each document
			- avglen: The average length of the documents in the collection
		"""

		N = len(document_info)

		print(f'Preprocessoring query: {query}')
		tokens = Preprocessor.perform_preprocess(query)
		print(f'Query tokens: {tokens}')
		
		answers = {}
		for token in tokens:
			posting_lists = self.positional_trie.search(token)
			idf = self.compute_idf(N, len(posting_lists))

			for doc in posting_lists:
				if doc not in answers:
					answers[doc] = idf * ((len(posting_lists[doc]) * (self.k1 + 1)) / (len(posting_lists[doc]) + self.k1 * ((1 - self.b) + self.b * (document_info[doc] / avglen))))
				else:
					answers[doc] += idf * ((len(posting_lists[doc]) * (self.k1 + 1)) / (len(posting_lists[doc]) + self.k1 * ((1 - self.b) + self.b * (document_info[doc] / avglen))))

		answers = {k: v for k, v in sorted(answers.items(), key = lambda item: item[1], reverse = True)}

		return answers

	def __compute_positional_intersect(self, p1, p2, k):
		"""
			This function append to the results list the documents that contains
			the 2 tokens with a distance of k.
		"""
		results = []
		for doc in p1:

			if doc in p2:

				list_1 = p1[doc]
				list_2 = p2[doc]

				for position_1 in list_1:
					for position_2 in list_2:
						if position_2 - position_1 == k:
							results.append(doc)
							break

		return results
	
	def perform_phrase_query(self, query):
		"""
			This function performs a phrase query on the positional index.
			The query is handled has a biword index (can generate false positive).
                        More specifically given a query of more than one token it finds
			the documents that contains the tokens with a distance of k. The rank
                        is based on the number of occurences.

			- query: The query to perform
			- return: The list of documents that contain or partialy contain the prase query
			with the relative score
		"""
		tokens = Preprocessor.perform_preprocess(query)

		if len(tokens) < 2:
			return {'Error': 'The query must contain at least two tokens'}

		answers = []
		for i, token in enumerate(tokens):
			
			p1 = self.positional_trie.search(token)
			j = i + 1

			while j < len(tokens):

				p2 = self.positional_trie.search(tokens[j])

				if len(p1) > len(p2):
					p1, p2 = p2, p1
					k = i - j
				else:
					k = j - i
				
				answer = self.__compute_positional_intersect(p1, p2, k)
				answers.append(answer)
				j += 1

		r = {}
		for lis in answers:
			for ele in lis:
				if ele in r.keys():
					r[ele] += 1
				else:
					r[ele] = 1

		# order the dictionary by value
		answers = {k: v for k, v in sorted(r.items(), key = lambda item: item[1], reverse = True)}

		# Sum of all values
		total = sum(answers.values())
		
		for key in answers.keys():
			answers[key] = (answers[key] / total)

		return answers
	
	def perform_author_query(self, query: str) -> List[int]:
		"""
			This function performs a query on the author trie.
			More specifically it computes the intersection of the posting lists
			of each token of the query.

			- query: The query to perform
			- return: The list of documents containing all the tokens of the query
		"""
		tokens = Preprocessor.perform_author_title_preprocess(query)
		posting_lists = []
		for token in tokens:
			posting_lists.append(self.author_trie.search(token))
		
		result_set = reduce(set.intersection, (set(arr) for arr in posting_lists))
		return list(result_set)

	def perform_title_query(self, query: str) -> List[int]:
		"""
			This function performs a query on the title trie.
			More specifically it computes the intersection of the posting lists
			of each token of the query.

			- query: The query to perform
			- return: The list of documents containing all the tokens of the query
		"""
		tokens = Preprocessor.perform_author_title_preprocess(query)
		posting_lists = []
		for token in tokens:
			posting_lists.append(self.title_trie.search(token))
		
		result_set = reduce(set.intersection, (set(arr) for arr in posting_lists))
		return list(result_set)
		
