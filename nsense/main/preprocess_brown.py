import sys

from nsense.dataset import extract_corpus_from_zip, preprocess_corpus

if __name__ == "__main__":
	data_dir = sys.argv[1]
	corpus = extract_corpus_from_zip(data_dir)
	corpus = preprocess_corpus(corpus)
	print(list(corpus))
