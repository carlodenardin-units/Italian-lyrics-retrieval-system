from bitarray import bitarray
from itertools import islice
from modules.utils import save_compressed_index

class Compress():

	def __init__(self, block_size: int = 4):
		self.block_size = block_size
	
	def compute_common_prefix(self, list: list[str]):
		"""
			Given a list of strings, it computes the common prefix of the list.
			
			- list: list of strings
			- return: common prefix of the list
		"""
		str1 = list[0]
		str2 = list[len(list) - 1]
		prefix = ""
		i, j = 0, 0
		while i < len(str1) and j < len(str2):
			if str1[i] != str2[j]:
				break
			prefix += str1[i]
			i += 1
			j += 1
		return prefix

	def compute_front_code(self, list: list[str]):
		"""
			Given a list of strings, it computes the front code of the list.

			- list: list of strings
			- return: front code of the list
		"""
		prefix = self.compute_common_prefix(list)

		result = str(len(prefix)) + prefix
		
		if prefix != "":
			for i in range(len(list)):
				result += str(len(list[i]) - len(prefix)) + list[i][len(prefix):]
		else:
			for i in range(len(list)):
				result += str(len(list[i])) + list[i]
		
		return result
	
	def compute_gaps(self, list: list[int]):
		"""
			Given a list of numbers, it computes the gaps between them.

			- list: list of numbers
			- return: list of gaps
		"""
		gaps = []
		gaps.append(list[0])
		for i in range(1, len(list)):
			gaps.append(list[i] - list[i-1])
		return gaps
	
	def compute_gamma(self, number: int):
		"""
			Calculates the gamma code of a number. The gamma code is composed by two parts:
			- unary code of the length of the binary representation of the number
			- binary representation of the number without the first digit

			- number: number to encode
			- return: gamma code of the number
		"""
		binary = bin(number)[3:]
		unary = '1' * len(binary) + '0'
		return unary + binary

	def encode(self, list: list[int]):
		"""
			Encodes a list of numbers using gamma code.

			- list: list of numbers
			- return: encoded list
		"""
		encoded_list = ''
		for number in list:
			encoded_list += self.compute_gamma(number)
		return encoded_list

	def compress_index(self, index):
		"""
			Compresses the index:
			- dictionary: compress the dictionary as a single string divided by
			blocks and in each block a front code is computed
			- posting lists: compress the posting lists using gamma code
			- pointers: save the length of the posting list and the pointer to the
			dictionary block and the pointer to the posting list

			- index: index to compress (lite index)
		"""
		compressed_pointers = ""
		compressed_dictionary = ""
		compressed_posting_lists = ""

		for i in range(0, len(index.keys()), self.block_size):

			terms = list(islice(index.keys(), i, i + self.block_size))
			
			block_pointer = len(compressed_dictionary)
			compressed_dictionary += self.compute_front_code(terms)

			for i, term in enumerate(terms):
				frequency = len(index[term])
				compressed_pointers += str(frequency) + ' '
				gaps = self.compute_gaps(index[term])
				encoded_gaps = self.encode(gaps)
				encoded_gaps_adjusted = encoded_gaps + ((8 - (len(encoded_gaps) % 8)) * '0') if len(encoded_gaps) % 8 != 0 else encoded_gaps
				compressed_pointers += str(len(compressed_posting_lists) // 8) + ' '
				compressed_posting_lists += encoded_gaps_adjusted

			compressed_pointers += str(block_pointer) + '\n'
		
		compressed_posting_lists = bitarray(compressed_posting_lists)

		save_compressed_index(compressed_dictionary, compressed_pointers, compressed_posting_lists)

"""
This is the decompression algorithm, it is not used in the project but it is
implemented for completeness.

class Decompress():

	def __init__(self, block_size: int = 4):
		self.block_size = block_size

	def compute_gamma_decode(self, bits: str, frequency: int):
		docs = []
		i = 0
		sum = 0
		while i < len(bits):
			j = i
			while bits[j] == '1':
				j += 1
			length = j - i			
			start = j + 1
			end = start + length
			offset = bits[start:end]
			binary = '1' + offset
			i = end
			sum += int(binary, 2)
			docs.append(sum)
			if len(docs) == frequency:
				break
		return docs
			
	def decompress_posting_list(self, compressed_posting_lists, pointers, next_pointers, frequencies):
		posting_lists = []
		for i in range(len(pointers)):
			if i < len(pointers) - 1:
				bits = compressed_posting_lists[int(pointers[i]) * 8: int(pointers[i + 1]) * 8]
				
			else:
				if next_pointers != []:
					bits = compressed_posting_lists[int(pointers[i]) * 8: int(next_pointers[0]) * 8]
				else:
					bits = compressed_posting_lists[int(pointers[i]) * 8:]
			posting_lists.append(self.compute_gamma_decode(bits, frequencies[i]))
		return posting_lists

	def decompress_terms(self, compressed_dictionary, pointer):
		terms = []
		i = pointer
		prefix = ""
		prefix_digits = 0

		# Check if the prefix is 0
		if compressed_dictionary[i] == '0':
			prefix_digits = 0
			i += 1 # Skip the prefix number
		else:
			# Check if the prefix is composed by 1 or 2 digits (cannot be more than 2)
			if compressed_dictionary[i + 1].isdigit():
				prefix_digits = int(compressed_dictionary[i] + compressed_dictionary[i + 1])
				i += 2 # Skip the prefix number
			else:
				prefix_digits = int(compressed_dictionary[i])
				i += 1 # Skip the prefix number
		
		if i < i + prefix_digits:
			prefix = compressed_dictionary[i: i + prefix_digits]

		# Iterate over the block
		j = i + prefix_digits
		while len(terms) < self.block_size and j < len(compressed_dictionary):
			if compressed_dictionary[j] == '0':
				terms.append(prefix)
				j += int(compressed_dictionary[j]) + 1
			else:
				if compressed_dictionary[j + 1].isdigit():
					digits = int(compressed_dictionary[j] + compressed_dictionary[j + 1])
					terms.append(prefix + compressed_dictionary[j + 2: j + 2 + digits])
					j += digits + 2
				else:
					digits = int(compressed_dictionary[j])
					terms.append(prefix + compressed_dictionary[j + 1: j + 1 + digits])
					j += digits + 1
		return terms

	def decompress(self):

		trie = TrieLite()

		compressed_dictionary = ""
		compressed_posting_lists = ""

		with open('compression/compressed_dictionary.txt', 'r') as file:
			compressed_dictionary = file.read()
		
		with open('compression/compressed_posting_lists.bin', 'rb') as file:
			bits = bitarray()
			bits.fromfile(file)
			compressed_posting_lists = bits.to01()

		with open('compression/compressed_pointers.txt', 'r') as file:
			lines = file.readlines()
			for i, line in enumerate(lines):

				frequencies = line.split(' ')[1:5] = line.split(' ')[0:8:2]
				pointers = line.split(' ')[1:8:2]

				# Get the next pointer which is after the term pointer and \n
				if i < len(lines) - 1:
					next_pointers = lines[i + 1].split(' ')[1:2]
				else :
					next_pointers = []

				posting_lists = self.decompress_posting_list(compressed_posting_lists, pointers, next_pointers, [int(f) for f in frequencies])

				term_pointer = int(line.split(' ')[8])
				terms = self.decompress_terms(compressed_dictionary, term_pointer)

				for i, term in enumerate(terms):
					trie.insert(term, set(posting_lists[i]))
		
		return trie
"""	
				