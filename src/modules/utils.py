"""
	This file contains functions used to save the indexes and other informations
"""

def save_compressed_index(compressed_dictionary, compressed_pointers, compressed_posting_lists):
	with open('../compression/compressed_dictionary.txt', 'w') as file:
			file.write(compressed_dictionary)
		
	with open('../compression/compressed_pointers.txt', 'w') as file:
		file.write(compressed_pointers)

	with open('../compression/compressed_posting_lists.bin', 'wb') as file:
		compressed_posting_lists.tofile(file)

def save_dataset_info(document_info, average_length):
	with open('../index/documents_info.txt', 'w') as file:
			file.write(document_info)

	with open('../index/avglen.txt', 'w') as file:
		file.write(average_length)

def save_index(path, sorted_terms, dictionary):
	with open(path, 'w') as f:
		for term in sorted_terms:
			docs_id = ""
			for key in dictionary[term]:
				docs_id += f' {key}'
			f.write(f'{term}{docs_id}\n')

def save_positional_index(path, sorted_terms, dictionary):
	with open(path, 'w') as f:
		for term in sorted_terms:
			f.write(f'{term}: {dictionary[term]}\n')




