class Document:

	def __init__(self, id: int, title: str, author: str, lyrics: str):
		self.id = id
		self.title = title
		self.author = author
		self.lyrics = lyrics
		self.terms = []
	
	def __repr__(self):
		return "Document(id={}, title={}, author={}, lyrics={})".format(self.id, self.title, self.author, self.lyrics)