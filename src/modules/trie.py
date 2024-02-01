class TrieNode:

	def __init__(self):
		self.children = {}
		self.end = True
		self.positional_posting_list = {}

class Trie:
	
	def __init__(self):
		self.root = TrieNode()

	def insert(self, word, positional_posting_list):
		current = self.root
		for letter in word:
			if letter not in current.children:
				current.children[letter] = TrieNode()
			current = current.children[letter]
		current.end = True
		current.positional_posting_list = positional_posting_list

	def search(self, word):
		current = self.root
		for letter in word:
			current = current.children[letter]
		if current.end:
			return current.positional_posting_list
	
	def startsWith(self, prefix):
		current = self.root
		for letter in prefix:
			current = current.children[letter]
		return True

	