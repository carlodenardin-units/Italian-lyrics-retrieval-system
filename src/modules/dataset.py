from modules.document import Document
from modules.preprocessor import *
from modules.simhash import Simhash
from tqdm import tqdm

import os

def extract_document_number(filename):
	return int(''.join(filter(str.isdigit, filename)))

class Dataset:

	def __init__(self):
		self.N = 0
		self.documents = []

	def __len__(self):
		return self.N

	def __repr__(self):
		return "Dataset(n={}, avg_len={})".format(self.N, self.len / self.N if self.N > 0 else self.len)

	def load_dataset(self, path: str):
		file_list = os.listdir(path)
		file_list_sorted = sorted(file_list, key = extract_document_number)

		for i, file in enumerate(file_list_sorted):
			with open(path + file, "r", encoding = "utf-8") as f:
				content = f.readlines()
				author = content[0].strip('\n')
				title = content[1].strip('\n')
				lyrics_lines = content[2:]
				lyrics = ""
				for line in lyrics_lines:
					lyrics += line.strip('\n') + " "
				self.documents.append(Document(i, title, author, lyrics))

		self.N = len(self.documents)

	def remove_duplicates(self):
		simhash = Simhash()
		dict = {}
		for document in self.documents:
			if document.author not in dict:
				dict[document.author] = []
			dict[document.author].append(document)

		for author in tqdm(dict, desc = "Removing duplicates"):
			documents = dict[author]
			unique_songs = {}
			for document in documents:
				tokens = Preprocessor.perform_preprocess(document.lyrics)
				hash = simhash.perform_simhash(tokens)
				if hash not in unique_songs:
					unique_songs[hash] = document.id
				else:
					self.documents.remove(document)
