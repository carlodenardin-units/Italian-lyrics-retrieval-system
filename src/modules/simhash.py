from hashlib import md5
from modules.preprocessor import Preprocessor

class Token:

	def __init__(self, hash_list, weight):
		self.hash_list = hash_list
		self.weight = weight

class Simhash:

	def compute_hash(self, token):
		"""
			This function calculates the md5 hash of a token and then
			converts it to binary.

			- token: The token we want to hash
			- return: The hashed token
		"""
		return bin(int(md5(token.encode('utf-8')).hexdigest(), 16))[2:]

	def compute_simhash(self, token_dict, b):
		"""
			This function calculates the Simhash value of a document.
			More specifically it sum or subtracts the weights of each bit
			for each token of the document. If the sum is positive then
			the bit is set to 1 otherwise it is set to 0.

			- token_dict: A dictionary containing all the tokens of the document (hash, weight)
		"""
		sum_hash = [0] * b
		for token in token_dict.values():
			sum_hash = [sum_hash + token.weight * hash_bit for sum_hash, hash_bit in zip(sum_hash, token.hash_list)]
		
		sum_hash = [1 if i > 0 else 0 for i in sum_hash]

		return sum_hash

	def compute_conversion(self, hash):
		"""
			This function converts the 0 in -1 in the word hash. This is useful
			to compute more efficiently the simhash value.

			- hash: The hash of a token
		"""
		return list(map(lambda bit: 1 if bit == '1' else -1, hash))


	def compute_weights(self, terms, b):
		"""
			This function computes the weight of each token of the document.
			More specifically it calculates the hash of each token and then
			create an instance of the Token class for each token and assign
			to it the hash_list of the token and the weight

			- terms: The list of tokens of the document
			- return: A dictionary containing all the tokens of the document (hash, weight)
		"""
		term_dict = {}
		for term in terms:
			if term not in term_dict:
				hash = self.compute_hash(term).zfill(b)
				hash_list = self.compute_conversion(hash)
				term_dict[term] = Token(hash_list, 0)
			term_dict[term].weight += 1
		return term_dict

	def perform_simhash(self, tokens, b = 128):
		"""
			This function computes the Simhash value of a document.
			First of all it computes the weight of each token of the document creating
			a dictionary of terms (hash, weight).
			Then it compute the Simhash value of the document.
		
			- tokens: The list of tokens of the document
			- b: The number of bits of the Simhash value
			- return: The Simhash value of the document
		"""
		token_dict = self.compute_weights(tokens, b)
		simhash = self.compute_simhash(token_dict, b)
		simhash_string =  ''.join(str(bit) for bit in simhash)
		return simhash_string