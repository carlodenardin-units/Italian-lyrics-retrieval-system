from itertools import islice
from modules.index import Indexer
from modules.query import Query

import ast

print("Loading the indexes... (this may take a while)")

author_trie, title_trie, positional_trie = Indexer.load_indexes()

with open('../index/documents_info.txt', 'r') as f:
	document_info = ast.literal_eval(f.read())

with open('../index/avglen.txt', 'r') as f:
	avglen = float(f.read())

query_engine = Query(author_trie, title_trie, positional_trie)

print("Which type of query do you want to perform? (a = author, t = title, l = lyrics)")

query_type = input()

while True:
	assert query_type in ['a', 't', 'l'], "Invalid query type."

	print(f"Enter your [{query_type}] query: (for phrase query on lyrics, use double quotes)")
	query = input()

	results = {}

	if query_type == 'a':
		print(query_engine.perform_author_query(query))
	elif query_type == 't':
		print(query_engine.perform_title_query(query))
	elif query_type == 'l':
		if query[0] == '"' and query[-1] == '"':
			results = query_engine.perform_phrase_query(query)
		else:
			results = query_engine.perform_okapi_bm25(query, document_info, avglen)
	else:
		print("Invalid query type.")

	for key, value in islice(results.items(), 5):
		print(f'{key} -> {value}')

	print("Do you want to perform another query? (y/n)")
	choice = input()
	if choice == 'n':
		break
	elif choice == 'y':
		print("Which type of query do you want to perform? (a = author, t = title, l = lyrics)")
		query_type = input()
	else:
		print("Invalid choice.")
		exit()